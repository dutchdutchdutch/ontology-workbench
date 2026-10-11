#!/usr/bin/env python3
"""Render a project's published glossary as ontology data for tools/ontology-visualizer.html.

Usage:
  tools/render-ontology.py <project>                 render 05-glossary/glossary.md into 06-ontology/
  tools/render-ontology.py <project> --core          render only the entries marked core: true
  tools/render-ontology.py <project> --workflows     render only the entries with a workflow: key,
                                                     framed by workflow instead of by category
  tools/render-ontology.py <project> --relations-only  drop the depends-on fallback edges
  tools/render-ontology.py <project> --skip "<why>"  write 06-ontology/skipped.md instead

Two kinds of edge come out. A `relations:` item is a stated relation and carries the verb the
definition uses; its kind is "relation". A `depends_on:` item with no relation already linking
the pair is a fallback, labelled "depends on"; its kind is "depends". The page draws the second
dashed and muted, because a picture where every line reads "depends on" is a grouping, not an
ontology. `--relations-only` drops the fallback edges entirely.

The script also reports every entry whose definition wikilinks a term it states no relation for.
That is a finding for step 05, never an error here: it means the verb is still in the prose.

`--core` and `--workflows` narrow the view. Each is a filter on one key the glossary already
holds, and nothing else: no node, edge or definition is invented or changed. The scope is written
into the data file and shown under the title, so a reader always knows whether they are looking
at all of the glossary or part of it.

Every scope frames by `category:`, the taxonomy step 05 publishes. A workflow is a lens laid over
that layout, never a second layout: `meta.workflows` carries each sequence in order, every node
carries its own `workflow` positions, and the page highlights the members in place. `--workflows`
narrows the nodes to those that carry the key; it does not reframe them. An edge whose target is
outside the view is reported as out of scope, never as an unresolved link.

The frames run left to right in the glossary's category order, the reading order step 05
publishes. That is the default and a starting point. A project may set `ontology: layout:
shortest` in its project.yaml, and the script then places the frames in the order that makes the
lines shortest in total, starting from the reading order and keeping it on a tie. `pin_left:`
fixes named frames at the left first. Or it may list `ontology: frame_order:` by hand, one item
per column; an item "A + B" stacks frame B under frame A in the same column. Only the frames move: a node keeps its row inside its frame and
its category's colour, and no node, edge or category changes. `meta.layout` records the order
used and both total lengths.

A line can carry a kind (`relation_kinds:`, factory/rules/relation-kinds.md). The kind then
decides the line's flow, and the edge carries it as `relKind`; with no kind, the flow is read from
the verb as before. Every relation line the picture cannot read as written (no link, text after the
link, two links) is printed, because a dropped line used to vanish without a word. The canvas
draws one line per written relation, one direction, one label.

Every render also writes `ontology-machine.json`, the lens for agents: every entry whatever the
scope, each line with its kind, the reverse of each kinded line marked generated, and the open
question-pack relations from the draft's verification queue marked unconfirmed. A view, never a
source; none of it reaches the canvas.

Reads only: the `### ` headings, the fenced yaml block in each entry, and the definition, which
the entry format fixes as the blockquote under the heading. Nothing else. If a fact you need is
only in prose, add a key to the entry (factory/rules/entry-format.md); do not parse here.

A glossary written before the blockquote rule (2026-09-20) put the definition in the first
paragraph after the yaml block. Both shapes still parse, so old drafts keep rendering.

Standard library only. No PyYAML: the entry format keeps keys flat, so a tiny parser is enough.
"""
import itertools
import json
import math
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Ten, because six wrapped at a seventh category and drew two frames the same cyan. Ten
# covers a large glossary; past that the wrap returns, and a picture with eleven
# frames has a bigger problem than its colours.
PALETTE = ["#00f5d4", "#c084fc", "#2ec4b6", "#ff9f1c", "#ff4d6d", "#64748b",
           "#38bdf8", "#a3e635", "#f472b6", "#fbbf24"]
FRAME_W, FRAME_GAP, FRAME_X0, FRAME_Y0 = 310, 80, 40, 60
NODE_DX, NODE_DY, NODE_Y0 = 20, 130, 100
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def split_inline_list(v):
    items, buf, quote = [], "", None
    for ch in v:
        if quote:
            buf += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            buf += ch
        elif ch == ",":
            items.append(unquote(buf))
            buf = ""
        else:
            buf += ch
    if buf.strip():
        items.append(unquote(buf))
    return items


def parse_flat_yaml(lines):
    """key: scalar | key: [a, b] | key:\\n  - a\\n  - b. No nesting."""
    data, key = {}, None
    for raw in lines:
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                data[key] = []
            elif val.startswith("[") and val.endswith("]"):
                data[key] = split_inline_list(val[1:-1])
            elif val in ("true", "false"):
                data[key] = val == "true"
            else:
                data[key] = unquote(val)
        elif line.strip().startswith("- ") and key is not None:
            if not isinstance(data[key], list):
                data[key] = []
            data[key].append(unquote(line.strip()[2:]))
    return data


def first_paragraph_after_block(body):
    """The pre-2026-09-20 entry shape: definition is the first paragraph after the yaml block."""
    k = 0
    while k < len(body) and not body[k].strip().startswith("```yaml"):
        k += 1
    while k < len(body) and not body[k].strip() == "```":
        k += 1
    k += 1
    while k < len(body) and not body[k].strip():
        k += 1
    para = []
    while k < len(body) and body[k].strip() and not body[k].startswith("#"):
        para.append(body[k].strip())
        k += 1
    return " ".join(para)


def parse_glossary(text):
    """Yield entries: term, fields, definition, section (enclosing ## heading)."""
    entries, section = [], None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            section = line[3:].strip()
        elif line.startswith("### "):
            term = line[4:].strip()
            # the entry runs to the next heading of any level
            j = i + 1
            body = []
            while j < len(lines) and not lines[j].startswith("### ") and not lines[j].startswith("## "):
                body.append(lines[j])
                j += 1

            # the yaml block, wherever it sits in the entry
            block, k = [], 0
            while k < len(body):
                if body[k].strip().startswith("```yaml"):
                    k += 1
                    while k < len(body) and not body[k].strip().startswith("```"):
                        block.append(body[k])
                        k += 1
                k += 1
            fields = parse_flat_yaml(block)

            # the definition: the blockquote (entry-format.md), or, for a glossary written
            # before that rule, the first paragraph after the yaml block
            quote = [ln.strip()[2:].strip() for ln in body if ln.strip().startswith("> ")]
            if quote:
                definition = " ".join(quote)
            else:
                definition = first_paragraph_after_block(body)

            entries.append({"term": term, "fields": fields, "definition": definition, "section": section})
            i = j
            continue
        i += 1
    return entries


def slug(term):
    return re.sub(r"[^A-Za-z0-9]", "", term) or "T"


def strip_links(text):
    return WIKILINK.sub(r"\1", text)


WORKFLOW = re.compile(r"^(.*?)\s+(\d+)$")


def workflows_of(entry):
    """[('meal', 1)] from workflow: ["meal 1"]. A term may sit in two sequences."""
    out = []
    for item in entry["fields"].get("workflow", []) or []:
        m = WORKFLOW.match(str(item).strip())
        out.append((m.group(1).strip(), int(m.group(2))) if m else (str(item).strip(), 0))
    return out


def workflow_of(entry):
    """The first ('meal', 1), or None. Kept for the scope filter."""
    wf = workflows_of(entry)
    return wf[0] if wf else None


# How a relation's verb maps to the direction things actually move.
#
# A relation is written subject verb object, always, because that is the sentence the entry's own
# definition makes. The picture wants a second thing the sentence does not give: which way the
# work flows. "A station reads a ticket" is subject to object as a sentence, and ticket to
# station as a flow, because reading takes something in. Drawing it as outgoing shows a station
# emitting tickets, which is backwards, and it hides the feedback loop the glossary now states.
#
# Three classes, because the graph holds three kinds of claim:
#   consumes   the subject takes the object in. Flow runs object to subject.
#   produces   the subject makes, drives or acts on the object. Flow runs subject to object.
#   structure  neither. Containment, kind, requirement. No flow at all.
#
# Verbs are free text by design, so this matches on stems and reports whatever it could not place
# rather than guessing quietly. The shared verb list is in factory/rules/entry-format.md.
# A passive verb is not automatically consuming. The test is whether the verb's result lands in
# the subject. Making a reservation fixes its time and table, so the maker's decision flows in and
# the verb consumes. Inspecting a course leaves the course unchanged, so the inspector is the one
# taking something in, and the flow runs subject to agent, which is the producing direction. Same for
# discussing, and for using. Grammar does not decide this; what moves does.
# The generic verbs: the ones that mean the same thing in any domain. A verb that only makes
# sense inside one product does not belong here; it goes in that project's `verbs:` block in
# projects/<p>/project.yaml, which is where every project-specific value lives.
#
# "X is <verb>ed by Y" is NOT automatically consuming, and getting that wrong is the easy mistake.
# The test is where the verb's result lands. When the agent brings the subject into being or fixes
# its value, the result lands in the subject and the verb consumes: "is set by", "is created by",
# "is granted by". When the subject already exists and the agent merely takes it in, the result
# lands in the agent, so the subject flows outward and the verb produces: "is used by", "is read
# by", "is received by". A ticket read by a station gives its contents to the station; the station
# does not flow into the ticket. Those produce-side passives are absent from this list on purpose, because
# `produces` is the fallback. See the verb table in factory/rules/entry-format.md.
GENERIC_CONSUMES = (
    "reads", "uses",
    "is built from", "built from",
    "is derived from", "derived from",
    "is produced by", "produced by",
    "is performed by", "performed by",
    "is an instance of", "instance of",
    "is selected by", "selected by",
    "is chosen by", "chosen by",
    "is reported by", "reported by",
    "is set by", "set by",
    "is confirmed by", "confirmed by",
    "is created by", "created by",
    "is made by", "made by",
    "is run by", "run by",
    "is written by", "written by",
    "is recorded by", "recorded by",
    "is issued by", "issued by",
    "is delivered by", "delivered by",
    "is granted by", "granted by",
    "is offered by", "offered by",
    "is paid by", "paid by",
    "is charged by", "charged by",
    "is filled by", "filled by",
    "is matched by", "matched by",
    "is measured by", "measured by",
    "is triggered by", "triggered by",
    "is identified by", "identified by",
    "is generated from", "generated from",
    "is earned by", "earned by",
)
GENERIC_STRUCTURE = (
    "contains", "is part of", "is a kind of", "is made of", "is inside", "is on",
    "holds", "carries", "includes", "employs", "lists", "listed in", "listed on", "named on",
    "requires", "is required by", "belongs to", "spans", "counts", "is a property of",
    "is an attribute of", "happens before", "outlives", "is compared with", "may be",
    "is shared across", "is tied to", "is for one", "is held by", "is inside one",
)

# The relation kinds, factory/rules/relation-kinds.md: kind -> (inverse, flow). A kind on a line
# decides its flow, and the verb is not read. These are generic by rule, the same in any product;
# a project's own extras live in its project.yaml (`relation_kinds:`), never here.
KINDS = {
    "is_a": ("has_kind", "structure"), "aspect_of": ("has_aspect", "structure"),
    "contains": ("part_of", "structure"), "identifies": ("identified_by", "structure"),
    "holds": ("held_by", "structure"), "employs": ("employed_by", "structure"),
    "requires": ("required_by", "structure"), "blocks": ("blocked_by", "structure"),
    "governs": ("governed_by", "produces"), "authorizes": ("authorized_by", "produces"),
    "follows": ("precedes", "structure"), "performs": ("performed_by", "produces"),
    "serves": ("served_by", "produces"), "creates": ("created_by", "produces"),
    "becomes": ("became_from", "produces"), "verifies": ("verified_by", "produces"),
    "pays": ("paid_by", "produces"), "bills": ("billed_by", "produces"),
    "feeds": ("fed_by", "produces"), "measures": ("measured_by", "produces"),
    "concerns": ("concerned_by", "produces"),
}
TYPES = ("role", "organisation", "entity", "document", "credential", "identifier", "rule",
         "metric", "action", "event", "state", "surface")


def load_project_verbs(project):
    """The `verbs:` block of projects/<p>/project.yaml: consumes, structure, produces.

    Project verbs win over the generic ones, because a product is allowed to mean something
    particular by a word. `produces` is the default flow, so listing a verb there is how a
    project overrides a generic classification it disagrees with.
    """
    out = {"consumes": [], "structure": [], "produces": []}
    path = ROOT / "projects" / project / "project.yaml"
    if not path.exists():
        return out
    inside, key = False, None
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if re.match(r"^verbs:\s*$", line):
            inside, key = True, None
            continue
        if inside and not line.startswith(" "):
            break
        if not inside:
            continue
        m = re.match(r"^\s+(consumes|structure|produces):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                out[key] = [v.lower() for v in split_inline_list(val[1:-1]) if v]
            continue
        if key and line.strip().startswith("- "):
            out[key].append(unquote(line.strip()[2:]).lower())
    return out


def load_project_kinds(project):
    """The `relation_kinds:` block of projects/<p>/project.yaml: a project's extra kinds.

    One line per kind, `name: { inverse: x, flow: y }`. An extra with no inverse or no valid flow
    is reported and left out, because a kind the picture cannot place is worse than none.
    """
    out = {}
    path = ROOT / "projects" / project / "project.yaml"
    if not path.exists():
        return out
    inside = False
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if re.match(r"^relation_kinds:\s*$", line):
            inside = True
            continue
        if inside and not line.startswith(" "):
            break
        if not inside:
            continue
        m = re.match(r"^\s+([a-z_]+):\s*\{(.*)\}\s*$", line)
        if not m:
            print(f"  project.yaml relation_kinds: cannot read {line.strip()!r}", file=sys.stderr)
            continue
        opts = dict((unquote(k), unquote(v)) for k, _, v in
                    (p.partition(":") for p in split_inline_list(m.group(2))))
        inv, flow = opts.get("inverse", ""), opts.get("flow", "")
        if not inv or flow not in ("produces", "consumes", "structure"):
            print(f"  project.yaml relation_kinds: {m.group(1)} needs an inverse and a flow "
                  f"(produces, consumes or structure)", file=sys.stderr)
            continue
        out[m.group(1)] = (inv, flow)
    return out


# The inverses whose agent only takes the subject in, and leaves it as it was. Their result lands
# in the agent, so they produce, like the passive "is checked by" family in entry-format.md.
# An expo who inspects a course takes the answer in, so the course flows to the expo.
TAKES_IN = ("verified_by", "measured_by")


def kind_table(project):
    """Every kind and every inverse form -> {inverse, flow}. An inverse consumes, except that a
    structure kind stays structure (containment read from the other side still moves nothing), and
    an inverse in TAKES_IN produces (checking or measuring lands in the agent)."""
    table = {}
    for k, (inv, flow) in {**KINDS, **load_project_kinds(project)}.items():
        table[k] = {"inverse": inv, "flow": flow}
        inv_flow = "structure" if flow == "structure" else ("produces" if inv in TAKES_IN else "consumes")
        table[inv] = {"inverse": k, "flow": inv_flow}
    return table


def as_list(v):
    if v is None or v == "":
        return []
    return [str(x) for x in v] if isinstance(v, list) else [str(v)]


LINE = re.compile(r"^(.*?)\s*\[\[([^\]]+)\]\]\s*$")


def relation_lines(entry, kinds):
    """Every `relations:` line of one entry, read the way the picture reads it.

    Walks the list by index, so item N of `relation_kinds:` stays with line N even when a line
    cannot be read. A line is drawn when it ends in a wikilink; its object is that last link, as
    it always was. `problem` says what is wrong with a line: no link or text after the link (the
    line is dropped), or two links (drawn to the last one). A line `is a kind of [[X]]` with no
    kind is read as `is_a`, marked inferred.
    """
    f = entry["fields"]
    rels, given = as_list(f.get("relations")), f.get("relation_kinds")
    given = as_list(given) if given is not None else None
    out = []
    for i, item in enumerate(rels):
        links = WIKILINK.findall(item)
        m = LINE.match(item)
        line = {"index": i, "raw": item, "verb": None, "object": None, "kind": None,
                "inferred": False, "problem": None, "badKind": None}
        if not links:
            line["problem"] = "no link; dropped"
        elif not m:
            line["problem"] = "text after the link; dropped"
        else:
            line["verb"] = m.group(1).strip() or "relates to"
            line["object"] = m.group(2).strip()
            if len(links) > 1:
                line["problem"] = f"{len(links)} links; drawn to the last, [[{line['object']}]]"
        k = given[i].strip() if given is not None and i < len(given) else ""
        if k and k in kinds:
            line["kind"] = k
        elif k:
            line["badKind"] = k
        elif line["verb"] and line["verb"].lower().startswith("is a kind of"):
            line["kind"], line["inferred"] = "is_a", True
        out.append(line)
    return out


def coverage(entries, kinds):
    """What the glossary holds and what it still lacks. A report, never a gate."""
    by_type, lines, kinded, linked = {}, 0, 0, set()
    for e in entries:
        t = e["fields"].get("type") or "(none)"
        by_type[t] = by_type.get(t, 0) + 1
        for ln in relation_lines(e, kinds):
            lines += 1
            if ln["kind"] and not ln["inferred"]:
                kinded += 1
            if ln["object"]:
                linked.add(e["term"])
                linked.add(ln["object"])
    standalone = [e["term"] for e in entries if e["term"] not in linked]
    return {"entries": len(entries), "byType": dict(sorted(by_type.items())),
            "untyped": sum(n for t, n in by_type.items() if t not in TYPES),
            "relationLines": lines, "linesWithKind": kinded, "linesWithoutKind": lines - kinded,
            "standalone": len(standalone), "standaloneTerms": standalone}


def load_project_layout(project):
    """The `ontology:` block of projects/<p>/project.yaml: `layout:` and `frame_order:`.

    `layout: reading` (the default) keeps the glossary's category order. `layout: shortest`
    searches for the frame order with the shortest total line length. `pin_left:` fixes the
    frames it names at the left, in that order, and the search places the rest. `frame_order:`
    names a whole order by hand and wins over all of it; categories it leaves out follow in
    reading order. `show_structure: true` starts the page with the structure lines on; the
    default is off (factory/steps/06-ontology/CONTEXT.md, "How the page reads, for people").
    """
    out = {"layout": "reading", "frame_order": [], "pin_left": [], "show_structure": False}
    path = ROOT / "projects" / project / "project.yaml"
    if not path.exists():
        return out
    inside, key = False, None
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if re.match(r"^ontology:\s*$", line):
            inside, key = True, None
            continue
        if inside and not line.startswith(" "):
            break
        if not inside:
            continue
        m = re.match(r"^\s+(layout|frame_order|pin_left|show_structure):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if key == "show_structure":
                out["show_structure"] = val.lower() == "true"
            elif key == "layout":
                out["layout"] = unquote(val) or "reading"
            elif val.startswith("[") and val.endswith("]"):
                out[key] = [v for v in split_inline_list(val[1:-1]) if v]
            continue
        if key in ("frame_order", "pin_left") and line.strip().startswith("- "):
            out[key].append(unquote(line.strip()[2:]))
    return out


STACK_GAP = 60


def frame_x(pos):
    return FRAME_X0 + pos * (FRAME_W + FRAME_GAP)


def frame_h(n):
    return 60 + n * NODE_DY


def place(columns, sizes):
    """{category: (x, y)} for frames laid out as columns, each column stacked top to bottom."""
    out = {}
    for ci, col in enumerate(columns):
        y = FRAME_Y0
        for c in col:
            out[c] = (frame_x(ci), y)
            y += frame_h(sizes[c]) + STACK_GAP
    return out


def total_length(columns, rows, edges, sizes):
    """Sum of straight-line lengths of every drawn edge, with the frames laid out as `columns`.

    `rows` maps a node to (category, row). An edge inside one frame costs the same in every
    layout; it is counted anyway, to report a true total.
    """
    p = place(columns, sizes)
    s = 0.0
    for a, b in edges:
        (ca, ra), (cb, rb) = rows[a], rows[b]
        (xa, ya), (xb, yb) = p[ca], p[cb]
        s += math.hypot(xa - xb, (ya + ra * NODE_DY) - (yb + rb * NODE_DY))
    return s


def shortest_order(reading, rows, edges, sizes, pinned=()):
    """The frame order with the least total line length. Ties keep the reading order.

    `pinned` frames stay at the left in the order given; only the frames after them move.

    Up to eight frames, every order is tried. Past that the count explodes (eleven frames is
    forty million orders), so a local search starts from the reading order and applies the best
    single move, lifting one frame and dropping it elsewhere, until no move shortens the lines.
    """
    pinned = [c for c in pinned if c in reading]
    free = [c for c in reading if c not in pinned]
    best = pinned + free
    best_len = total_length([[c] for c in best], rows, edges, sizes)
    if len(free) <= 8:
        for perm in itertools.permutations(free):
            perm = pinned + list(perm)
            n = total_length([[c] for c in perm], rows, edges, sizes)
            if n < best_len - 1e-6:
                best, best_len = list(perm), n
        return best, best_len
    improved = True
    while improved:
        improved = False
        cand, cand_len = best, best_len
        for i in range(len(pinned), len(best)):
            for k in range(len(pinned), len(best)):
                if i == k:
                    continue
                trial = best[:i] + best[i + 1:]
                trial.insert(k, best[i])
                n = total_length([[c] for c in trial], rows, edges, sizes)
                if n < cand_len - 1e-6:
                    cand, cand_len = trial, n
        if cand is not best:
            best, best_len, improved = cand, cand_len, True
    return best, best_len


def verb_table(project):
    """Project verbs first, then the generic ones, so a project wins where the two disagree."""
    p = load_project_verbs(project)
    return {
        "produces": tuple(p["produces"]),
        "consumes": tuple(p["consumes"]) + GENERIC_CONSUMES,
        "structure": tuple(p["structure"]) + GENERIC_STRUCTURE,
    }


def flow_of(rel, table):
    """'consumes', 'produces' or 'structure' for one verb phrase.

    `produces` is checked first although it is also the fallback. A verb listed there is a
    project saying "not consuming, whatever the generic list thinks", and that has to beat the
    match below it. Everything unmatched falls through to produces, and the script prints what
    fell through so a wrong guess is visible rather than silent.
    """
    # The wikilink comes out first, because a verb phrase can wrap one: "is a [[Party]] with no"
    # is the stem "is a with no" with a term dropped into the middle of it. Matching the raw
    # string would need the term in the stem, which would make every stem project-specific.
    v = re.sub(r"\s+", " ", WIKILINK.sub("", rel)).strip().lower()
    for stem in table["produces"]:
        if v.startswith(stem) or f" {stem}" in v:
            return "produces"
    for stem in table["consumes"]:
        if v.startswith(stem) or f" {stem}" in v:
            return "consumes"
    for stem in table["structure"]:
        if v.startswith(stem):
            return "structure"
    return "produces"


def build(entries, project, scope="all", all_terms=None, relations_only=False, full=None):
    table = verb_table(project)
    kinds = kind_table(project)
    keys, seen = {}, {}
    for e in entries:
        base = slug(e["term"])
        k, n = base, 2
        while k in seen:
            k, n = f"{base}{n}", n + 1
        seen[k] = True
        keys[e["term"]] = k

    # Every scope frames by `category:`, the taxonomy step 05 already publishes. A workflow is a
    # lens laid over that layout, not a second layout: meta.workflows carries the sequences and
    # the page highlights their members in place. See DESIGN-NOTES.md.
    categories = []
    for e in entries:
        cat = e["fields"].get("category") or e["section"] or "Uncategorised"
        e["category"] = cat
        if cat not in categories:
            categories.append(cat)

    subgraphs, entities, counts = [], {}, {c: 0 for c in categories}
    for ci, cat in enumerate(categories):
        n = sum(1 for e in entries if e["category"] == cat)
        subgraphs.append({
            "id": f"G{ci + 1}", "title": f"{ci + 1:02d} / {cat}",
            "x": FRAME_X0 + ci * (FRAME_W + FRAME_GAP), "y": FRAME_Y0,
            "w": FRAME_W, "h": 60 + n * NODE_DY, "color": PALETTE[ci % len(PALETTE)],
            "category": cat,
        })
    cat_of, row_of = {}, {}
    for e in entries:
        ci = categories.index(e["category"])
        j = counts[e["category"]]
        counts[e["category"]] += 1
        cat_of[keys[e["term"]]], row_of[keys[e["term"]]] = e["category"], j
        f = e["fields"]
        core = f.get("core") is True
        typ = f.get("type", "")
        sub = ", ".join(x for x in [typ, "core" if core else "", f.get("status", "")] if x)
        lines = relation_lines(e, kinds)
        parent = lambda kind: next((ln["object"] for ln in lines
                                    if ln["kind"] == kind and ln["object"]), None)
        entities[keys[e["term"]]] = {
            "name": e["term"], "sub": sub, "domain": f"{ci + 1:02d} / {e['category']}",
            "code": f"{ci + 1}.{j + 1}", "icon": "★" if core else "·",
            "x": FRAME_X0 + ci * (FRAME_W + FRAME_GAP) + NODE_DX, "y": NODE_Y0 + j * NODE_DY,
            "color": PALETTE[ci % len(PALETTE)],
            "fullDef": strip_links(e["definition"]),
            "workflow": [{"name": n, "position": pos} for n, pos in workflows_of(e)],
            # For the panel's Machine detail and for agents. The canvas reads none of these.
            "type": typ, "status": f.get("status", ""), "core": core,
            "alsoCalled": as_list(f.get("also_called")),
            "notConfused": [strip_links(x) for x in as_list(f.get("not_to_be_confused_with"))],
            "rulings": as_list(f.get("rulings")),
            "isA": parent("is_a"), "aspectOf": parent("aspect_of"),
        }

    relationships, unresolved, out_of_scope, rid = [], [], [], 0
    linked = set()
    known = set(all_terms) if all_terms else set(keys)

    unreadable = []

    def add(frm, to_term, rel, kind, line=None):
        nonlocal rid
        if to_term not in keys:
            # a term with no entry anywhere is a gap; one the scope filtered out is not
            target = out_of_scope if to_term in known else unresolved
            target.append({"from": frm, "to": to_term, "rel": rel, "kind": kind})
            return
        rid += 1
        r = {"id": f"r{rid}", "from": keys[frm], "to": keys[to_term], "rel": rel, "kind": kind,
             "flow": "structure" if kind == "depends" else flow_of(rel, table)}
        if line and line["kind"]:
            # The kind decides the flow. An inferred kind (`is a kind of` with none written)
            # leaves the flow to the verb, so an old glossary draws exactly as it did.
            r["relKind"] = line["kind"]
            if line["inferred"]:
                r["relKindInferred"] = True
            else:
                r["flow"] = kinds[line["kind"]]["flow"]
        relationships.append(r)
        linked.add((frm, to_term))

    for e in entries:
        lines = relation_lines(e, kinds)
        given = e["fields"].get("relation_kinds")
        if given is not None and len(as_list(given)) != len(lines):
            unreadable.append({"term": e["term"], "line": "relation_kinds:",
                               "problem": f"{len(as_list(given))} kinds for {len(lines)} lines"})
        for ln in lines:
            if ln["problem"]:
                unreadable.append({"term": e["term"], "line": ln["raw"], "problem": ln["problem"]})
            if ln["badKind"]:
                unreadable.append({"term": e["term"], "line": ln["raw"],
                                   "problem": f"kind {ln['badKind']!r} is not in the table; flow read from the verb"})
            if ln["object"]:
                add(e["term"], ln["object"], ln["verb"], "relation", ln)
    # Fallbacks come after every stated relation, and only for a pair no relation joins from either
    # side. "Party contains Guest" already links the two, so Guest's depends_on on Party draws
    # no second, dashed line.
    for e in entries if not relations_only else []:
        for item in e["fields"].get("depends_on", []) or []:
            m = WIKILINK.search(item)
            if not m:
                continue
            other = m.group(1).strip()
            if (e["term"], other) not in linked and (other, e["term"]) not in linked:
                add(e["term"], other, "depends on", "depends")

    # Frame order. The reading order from the glossary is the default; a project may ask for the
    # order with the shortest lines, or name one. Only x moves: rows, colours and edges stay.
    layout_cfg = load_project_layout(project)
    rows = {k: (cat_of[k], row_of[k]) for k in cat_of}
    edges = [(r["from"], r["to"]) for r in relationships]
    sizes = {c: sum(1 for e in entries if e["category"] == c) for c in categories}
    reading_len = total_length([[c] for c in categories], rows, edges, sizes)
    columns = [[c] for c in categories]
    mode = layout_cfg["layout"]
    if layout_cfg["frame_order"]:
        # An item names one column. "A + B" stacks B under A in that column.
        columns, placed = [], set()
        for item in layout_cfg["frame_order"]:
            col = []
            for c in (s.strip() for s in item.split(" + ")):
                if c in categories and c not in placed:
                    col.append(c)
                    placed.add(c)
                else:
                    print(f"  project.yaml ontology.frame_order: no category {c!r} in this view",
                          file=sys.stderr)
            if col:
                columns.append(col)
        columns += [[c] for c in categories if c not in placed]
        mode = "frame_order"
    elif mode == "shortest":
        for c in layout_cfg["pin_left"]:
            if c not in categories:
                print(f"  project.yaml ontology.pin_left: no category {c!r} in this view",
                      file=sys.stderr)
        order, _ = shortest_order(categories, rows, edges, sizes, layout_cfg["pin_left"])
        columns = [[c] for c in order]
    elif mode != "reading":
        print(f"  project.yaml ontology.layout: unknown value {mode!r}, using reading order",
              file=sys.stderr)
        mode = "reading"
    order = [c for col in columns for c in col]
    pos = {c: i for i, c in enumerate(order)}
    xy = place(columns, sizes)
    for g in subgraphs:
        c = g["category"]
        g["x"], g["y"] = xy[c]
        g["title"] = f"{pos[c] + 1:02d} / {c}"
    subgraphs.sort(key=lambda g: pos[g["category"]])
    for k, ent in entities.items():
        c = cat_of[k]
        ent["x"] = xy[c][0] + NODE_DX
        ent["y"] = xy[c][1] + (NODE_Y0 - FRAME_Y0) + row_of[k] * NODE_DY
        ent["domain"] = f"{pos[c] + 1:02d} / {c}"
        ent["code"] = f"{pos[c] + 1}.{row_of[k] + 1}"
    layout = {"mode": mode, "order": order, "columns": columns, "readingOrder": categories,
              "pinLeft": [c for c in layout_cfg["pin_left"] if c in categories] if mode == "shortest" else [],
              "length": round(total_length(columns, rows, edges, sizes)),
              "readingLength": round(reading_len)}

    # A definition that wikilinks a term but states no relation for it: the verb is still in the
    # prose. A finding for step 05 (factory/rules/entry-format.md), never an error here.
    missing_relations = []
    for e in entries:
        stated = set()
        for item in e["fields"].get("relations", []) or []:
            m = WIKILINK.search(str(item))
            if m:
                stated.add(m.group(1).strip())
        if e["fields"].get("status") == "gap":
            continue  # a question has no subject to hang a verb on
        for m in WIKILINK.finditer(e["definition"]):
            target = m.group(1).strip()
            if target != e["term"] and target not in stated:
                missing_relations.append({"from": e["term"], "to": target})

    if scope == "core":
        title = f"{project} ontology: core terms"
        subtitle = (f"The {len(entries)} terms marked core in 05-glossary/glossary.md, the same "
                    f"set as core-terms.md. A view of the glossary; if they disagree, the "
                    f"glossary wins.")
        group_label = "Functional domains"
    elif scope == "workflows":
        subtitle = (f"The {len(entries)} terms with a workflow key in 05-glossary/glossary.md, "
                    f"framed by category like every other view. Use the workflow lens to read one "
                    f"sequence in order. A view of the glossary; if they disagree, the glossary "
                    f"wins.")
        title = f"{project} ontology: terms in a workflow"
        group_label = "Functional domains"
    else:
        title = f"{project} ontology"
        subtitle = "A view of 05-glossary/glossary.md. If they disagree, the glossary wins."
        group_label = "Functional domains"

    # The sequences, ordered by position, for the page's workflow lens.
    workflows = {}
    for e in entries:
        for name, pos in workflows_of(e):
            workflows.setdefault(name, []).append(
                {"key": keys[e["term"]], "term": e["term"], "position": pos})
    for name in workflows:
        workflows[name].sort(key=lambda w: (w["position"], w["term"]))

    meta = {
        "project": project, "title": title, "subtitle": subtitle, "scope": scope,
        "groupLabel": group_label,
        "generatedFrom": f"projects/{project}/05-glossary/glossary.md",
        "generatedAt": date.today().isoformat(),
        "entries": len(entries), "edges": len(relationships),
        "relationEdges": sum(1 for r in relationships if r["kind"] == "relation"),
        "dependsEdges": sum(1 for r in relationships if r["kind"] == "depends"),
        "relationsOnly": relations_only,
        "unresolved": unresolved, "outOfScope": out_of_scope,
        "missingRelations": missing_relations,
        "workflows": workflows,
        "layout": layout,
        # Which line switches start on. Consuming and producing always; structure only where the
        # project's `ontology: show_structure: true` asks for it.
        "linesOn": {"consumes": True, "produces": True, "structure": layout_cfg["show_structure"]},
        "unreadable": unreadable,
        "kinds": kinds,
        "coverage": coverage(full or entries, kinds),
    }
    if layout["mode"] == "shortest":
        meta["subtitle"] += (" Frames are placed to shorten the lines; the reading order is in "
                             "core-terms.md.")
    elif layout["mode"] == "frame_order":
        meta["subtitle"] += (" Frames are in an order set in project.yaml; the reading order is in "
                             "core-terms.md.")
    return meta, entities, subgraphs, relationships


def write_js(path, meta, entities, subgraphs, relationships):
    j = lambda v: json.dumps(v, ensure_ascii=False, indent=2)
    path.write_text(
        f"// Generated by tools/render-ontology.py from {meta['generatedFrom']} on {meta['generatedAt']}.\n"
        f"// Do not edit. Change the glossary and regenerate.\n\n"
        f"const meta = {j(meta)};\n\nconst entities = {j(entities)};\n\n"
        f"const subgraphs = {j(subgraphs)};\n\nconst relationships = {j(relationships)};\n",
        encoding="utf-8",
    )


QUEUE_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s+`([a-z_]+)`\s+\[\[([^\]]+)\]\]\s*\|(.*)\|\s*$")


def front_matter(text):
    """The `key: value` lines between the opening `---` pair, or {}."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    block = []
    for ln in lines[1:]:
        if ln.strip() == "---":
            return parse_flat_yaml(block)
        block.append(ln)
    return {}


def unconfirmed(project, version):
    """Draft relations nobody has answered yet, from the question packs in the verification queue
    of the draft this glossary was published from. A row is `| # | Subject `kind` [[Object]] |
    question | answer |`; it is open while the answer cell is empty. These are guesses, carried
    for agents as unconfirmed, never as meaning."""
    if not version:
        return []
    path = ROOT / "projects" / project / "04-draft" / str(version) / "verification-queue.md"
    if not path.exists():
        return []
    # The pack is the heading one level above the table's own heading ("Draft relations to
    # confirm"), so each item names the pack it came from.
    out, heads, pack = [], {}, None
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.startswith("#"):
            level = len(ln) - len(ln.lstrip("#"))
            heads = {k: v for k, v in heads.items() if k < level}
            heads[level] = ln.lstrip("#").strip()
            above = [k for k in heads if k < level]
            pack = heads[max(above)] if above else heads[level]
            continue
        m = QUEUE_ROW.match(ln)
        if not m:
            continue
        cells = [c.strip() for c in m.group(5).split("|")]
        if cells and cells[-1]:
            continue  # answered: an answer becomes a ruling, then a line in the glossary
        out.append({"subject": m.group(2).strip(), "kind": m.group(3), "object": m.group(4).strip(),
                    "question": cells[0] if len(cells) > 1 else "", "pack": pack,
                    "row": int(m.group(1)), "status": "unconfirmed",
                    "source": f"projects/{project}/04-draft/{version}/verification-queue.md"})
    return out


def machine(entries, project, text):
    """The machine lens: every entry, every line with its kind, both directions.

    A view for agents, never a source. The reverse of a line is generated from its kind's
    inverse and marked so; a line with no kind gets no reverse, because guessing one is the
    thing the kinds exist to stop. Nothing here is drawn on the canvas.
    """
    kinds = kind_table(project)
    for e in entries:
        e.setdefault("category", e["fields"].get("category") or e["section"] or "Uncategorised")
    names = {e["term"] for e in entries}
    out, by_term = [], {}
    for e in entries:
        f = e["fields"]
        lines = relation_lines(e, kinds)
        rec = {
            "term": e["term"], "type": f.get("type", ""), "status": f.get("status", ""),
            "category": e["category"], "core": f.get("core") is True,
            "definition": strip_links(e["definition"]),
            "alsoCalled": as_list(f.get("also_called")),
            "notConfusedWith": [strip_links(x) for x in as_list(f.get("not_to_be_confused_with"))],
            "dependsOn": [strip_links(x) for x in as_list(f.get("depends_on"))],
            "rulings": as_list(f.get("rulings")),
            "isA": next((ln["object"] for ln in lines if ln["kind"] == "is_a" and ln["object"]), None),
            "aspectOf": next((ln["object"] for ln in lines
                              if ln["kind"] == "aspect_of" and ln["object"]), None),
            "relations": [],
        }
        for ln in lines:
            if not ln["object"]:
                continue
            r = {"verb": ln["verb"], "kind": ln["kind"], "object": ln["object"],
                 "flow": kinds[ln["kind"]]["flow"] if ln["kind"] and not ln["inferred"] else None,
                 "direction": "written"}
            if ln["inferred"]:
                r["kindInferred"] = True
            rec["relations"].append(r)
        out.append(rec)
        by_term[e["term"]] = rec
    for rec in list(out):
        for r in [r for r in rec["relations"] if r["direction"] == "written"]:
            if r["kind"] and r["object"] in by_term:
                inv = kinds[r["kind"]]["inverse"]
                by_term[r["object"]]["relations"].append({
                    "verb": None, "kind": inv, "object": rec["term"],
                    "flow": kinds[inv]["flow"], "direction": "generated",
                    "fromLine": f"{rec['term']} {r['verb']} [[{r['object']}]]"})
    version = front_matter(text).get("published_from")
    meta = {
        "project": project, "generatedFrom": f"projects/{project}/05-glossary/glossary.md",
        "publishedFrom": version, "generatedAt": date.today().isoformat(),
        "note": ("A view of the glossary for agents. Never a source: regenerated, never edited. "
                 "Lines marked generated are the reverse of a written line, built from its kind. "
                 "Items under unconfirmed are guesses no expert has confirmed yet."),
        "kinds": kinds, "coverage": coverage(entries, kinds),
        "unresolved": sorted({r["object"] for rec in out for r in rec["relations"]
                              if r["object"] not in names}),
    }
    return {"meta": meta, "entries": out, "unconfirmed": unconfirmed(project, version)}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    project = argv[1]
    scope = "all"
    if "--core" in argv[2:]:
        scope = "core"
    if "--workflows" in argv[2:]:
        scope = "workflows"
    relations_only = "--relations-only" in argv[2:]
    pdir = ROOT / "projects" / project
    out = pdir / "06-ontology"
    if not pdir.is_dir():
        print(f"no such project: {pdir}", file=sys.stderr)
        return 1
    out.mkdir(exist_ok=True)
    glossary = pdir / "05-glossary" / "glossary.md"

    reason = None
    if len(argv) >= 4 and argv[2] == "--skip":
        reason = argv[3]
    elif not glossary.exists():
        reason = "no glossary yet"
    if reason:
        if (out / "ontology.html").exists():
            print(f"{out / 'ontology.html'} exists; a rendered picture cannot also be skipped. "
                  f"Remove the rendered files first if you mean it.", file=sys.stderr)
            return 1
        (out / "skipped.md").write_text(
            f"---\nstep: 06-ontology\nreason: {reason}\ndate: {date.today().isoformat()}\n---\n\n"
            f"Step 06 was considered on {date.today().isoformat()} and not run: {reason}.\n"
            f"Re-run `tools/render-ontology.py {project}` when it is wanted.\n",
            encoding="utf-8",
        )
        print(f"wrote {out / 'skipped.md'} (reason: {reason})")
        return 0

    text = glossary.read_text(encoding="utf-8")
    entries = parse_glossary(text)
    if not entries:
        print(f"{glossary}: no `### ` entries found", file=sys.stderr)
        return 1
    full = list(entries)
    all_terms = [e["term"] for e in entries]
    if scope == "core":
        entries = [e for e in entries if e["fields"].get("core") is True]
        if not entries:
            print(f"{glossary}: --core given, but no entry is marked `core: true`", file=sys.stderr)
            return 1
    elif scope == "workflows":
        entries = [e for e in entries if workflow_of(e)]
        if not entries:
            print(f"{glossary}: --workflows given, but no entry has a `workflow:` key",
                  file=sys.stderr)
            return 1
    meta, entities, subgraphs, relationships = build(entries, project, scope, all_terms,
                                                     relations_only, full)
    write_js(out / "ontology-data.js", meta, entities, subgraphs, relationships)
    lens = machine(parse_glossary(text), project, text)
    (out / "ontology-machine.json").write_text(
        json.dumps(lens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(ROOT / "tools" / "ontology-visualizer.html", out / "ontology.html")
    skipped = out / "skipped.md"
    if skipped.exists():
        skipped.unlink()
    print(f"scope {scope}: {len(entries)} entries, {len(subgraphs)} categories, "
          f"{len(relationships)} edges -> {out}")
    print(f"  {meta['relationEdges']} stated relations, {meta['dependsEdges']} depends-on "
          f"fallbacks" + (" (dropped by --relations-only)" if relations_only else ""))
    byflow, guessed = {}, set()
    for r in relationships:
        if r["kind"] == "relation":
            byflow.setdefault(r["flow"], set()).add(r["rel"])
            # a kind decides its own flow; only a line read from its verb can be a wrong guess
            if r["flow"] == "produces" and ("relKind" not in r or r.get("relKindInferred")):
                guessed.add(r["rel"])
    print("  verb flow: " + ", ".join(
        f"{k} {len(v)}" for k, v in sorted(byflow.items())) + "  (consumes = drawn object to subject)")
    if guessed:
        print("  read as producing from the verb, check any that are not: "
              + ", ".join(sorted(guessed)))
    lay = meta["layout"]
    if lay["mode"] == "reading":
        print(f"  frames: reading order, total line length {lay['length']}")
    else:
        saved = lay["readingLength"] - lay["length"]
        pct = 100 * saved / lay["readingLength"] if lay["readingLength"] else 0
        print(f"  frames: {lay['mode']}, total line length {lay['length']} against "
              f"{lay['readingLength']} in reading order ({pct:.0f}% shorter)")
        print("  order: " + " | ".join(" + ".join(col) for col in lay["columns"]))
    cov = meta["coverage"]
    print(f"  kinds: {cov['linesWithKind']} of {cov['relationLines']} lines carry one; "
          f"{cov['standalone']} of {cov['entries']} entries stand alone. "
          f"Machine lens: ontology-machine.json, {len(lens['unconfirmed'])} unconfirmed")
    if meta["unreadable"]:
        print(f"{len(meta['unreadable'])} relation lines the picture cannot read as written "
              f"(one verb, one object, link last; factory/rules/relation-kinds.md):")
        for u in meta["unreadable"]:
            print(f"  {u['term']}: {u['line']!r}: {u['problem']}")
    if meta["missingRelations"]:
        print(f"{len(meta['missingRelations'])} definitions link a term with no relation for it "
              f"(the verb is still in the prose; a finding for step 05):")
        for mr in meta["missingRelations"]:
            print(f"  {mr['from']} -> {mr['to']}")
    if meta["unresolved"]:
        print("linked, not defined (no entry with that heading):")
        for u in meta["unresolved"]:
            print(f"  {u['from']} --{u['rel']}--> {u['to']}")
    if meta["outOfScope"]:
        print(f"{len(meta['outOfScope'])} edges point at a term this scope leaves out "
              f"(defined, just not drawn here)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
