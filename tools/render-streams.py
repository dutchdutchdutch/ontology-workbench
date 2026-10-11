#!/usr/bin/env python3
"""Render a project's value streams as a lens over the step 06 ontology picture.

Usage:
  tools/render-streams.py <project>                  render every stream in 07-streams/
  tools/render-streams.py <project> --stream money   render every stream, report only this one
  tools/render-streams.py <project> --skip "<why>"   write 07-streams/skipped.md instead

A stream is a lens, never a layout. The picture is step 06's picture: this script reads
`06-ontology/ontology-data.js` as it stands and copies its terms, frames, numbering and edges
unchanged. Whatever scope step 06 was rendered at, core or all, step 07 shows the same terms.
What a stream adds is a second set of edges: money, or data, or care, moving between terms that
the glossary already defines. A stream edge is not a relation and does not pretend to be one.
Money often runs against the sentence a definition makes, which is why it is drawn apart.

The stream file is authored by a person, in `projects/<p>/07-streams/<name>.md`. It is the one
input here that is not derived from the glossary, and it is a hypothesis until somebody signs it.
Every flow carries its evidence, and the script checks that every term it names has an entry.

This script reads the glossary the same way step 06 does and invents no node, edge or definition.
A term named in a stream file with no glossary entry is reported as unresolved: that is a finding
for step 05, never an error here.
"""
import importlib.util
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Step 06 owns the parser and the layout. Import it rather than copying it, so the two pictures
# cannot drift apart. It guards its own main(), so importing runs nothing.
_spec = importlib.util.spec_from_file_location("render_ontology", ROOT / "tools" / "render-ontology.py")
ro = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ro)

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
HEADING = re.compile(r"^### (.+)$", re.M)

# The roles a term can hold in a stream, in the order money meets them. A stream file may use any
# of these and no others; an unknown role is a typo, and the script says so rather than guessing.
ROLES = ["funder", "approver", "gate", "claim", "conduit", "unit", "meter", "clock", "trigger",
         "earner", "leak", "repair"]

# The keys a flow may carry. `from` and `kind` are required; everything else is optional, and an
# empty value is a fact too (a flow with no `to` says the value lands somewhere the glossary has
# no entry for, such as the tax office).
FLOW_KEYS = ["from", "to", "kind", "via", "trigger", "rate", "timing", "gate", "approved_by",
             "bypasses", "confidence", "evidence", "note"]

# The flow keys that point at another term rather than carrying a value of their own.
LINK_KEYS = ("from", "to", "via", "trigger", "rate", "timing", "gate", "approved_by", "bypasses")


def is_process_file(path):
    """True when the file's front matter holds `process:`. Streams have `stream:` or none."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---", 4)
    return end > 0 and re.search(r"^process:", text[4:end], re.M) is not None


def first_link(v):
    """The term inside [[...]], or the bare string, or "" for an empty value."""
    if not v:
        return ""
    m = WIKILINK.search(str(v))
    return m.group(1).strip() if m else str(v).strip()


def is_term(v):
    """True when the value points at a glossary entry. A bare word is a literal, not a term.

    `rate: "[[Menu item]]"` names an entry and must resolve. `rate: statutory` names the law,
    which a glossary does not define and should not. Only the first kind is checked or linked."""
    return bool(v) and "[[" in str(v)


def fenced_yaml(block):
    """The first ```yaml ... ``` block inside a chunk of markdown, parsed flat."""
    m = re.search(r"```yaml\n(.*?)```", block, re.S)
    return ro.parse_flat_yaml(m.group(1).split("\n")) if m else {}


def read_ontology(path):
    """Step 06's four data blocks, exactly as tools/render-ontology.py wrote them."""
    text = path.read_text(encoding="utf-8")
    blocks = {}
    for name in ("meta", "entities", "subgraphs", "relationships"):
        m = re.search(r"^const " + name + r" = (.*?);\n(?=\nconst |\Z)", text, re.S | re.M)
        if not m:
            raise SystemExit(f"{path}: no `const {name}` block. Re-run step 06.")
        blocks[name] = json.loads(m.group(1))
    return blocks["meta"], blocks["entities"], blocks["subgraphs"], blocks["relationships"]


def parse_stream(path):
    """A stream file: its flows, its roles, and the terms it names.

    Flows are `### ` headings with a yaml block, the same shape as a glossary entry, so a reader
    who can read one can read the other. Roles are one yaml block under `## Roles`.
    """
    text = path.read_text(encoding="utf-8")
    name = path.stem

    roles, bad_roles = {}, []
    if "## Roles" in text:
        section = text.split("## Roles", 1)[1].split("\n## ", 1)[0]
        for role, value in fenced_yaml(section).items():
            if role not in ROLES:
                bad_roles.append(role)
                continue
            items = value if isinstance(value, list) else [value]
            for term in (first_link(i) for i in items):
                if term:
                    roles[term] = role

    # `## Trace` names the flow keys the lens keeps saturated. With no section, every link counts.
    trace, bad_trace = list(LINK_KEYS), []
    if "## Trace" in text:
        section = text.split("## Trace", 1)[1].split("\n## ", 1)[0]
        value = fenced_yaml(section).get("trace", [])
        keys = value if isinstance(value, list) else [value]
        bad_trace = [k for k in keys if k not in LINK_KEYS]
        trace = [k for k in keys if k in LINK_KEYS] or trace

    # `## Base` lets one stream build on another: `extends` names it, `label` names this one.
    base = {}
    if "## Base" in text:
        base = fenced_yaml(text.split("## Base", 1)[1].split("\n## ", 1)[0])

    flows, reach = [], []
    chunks = re.split(r"\n(?=### )", text)
    for chunk in chunks:
        h = HEADING.match(chunk)
        if not h:
            continue
        f = fenced_yaml(chunk)
        # A reach row: a term one stated link from the stream, joined by an approval or a
        # submission. The renderer checks the link against the glossary, not the file.
        if "term" in f:
            reach.append({"term": first_link(f["term"]), "kind": f.get("kind", ""),
                          "link": f.get("link", ""), "evidence": f.get("evidence", "")})
            continue
        if "from" not in f:
            continue
        flow = {"label": h.group(1).strip(), "literals": []}
        for k in FLOW_KEYS:
            v = f.get(k, "")
            if k in LINK_KEYS:
                flow[k] = first_link(v)
                if flow[k] and not is_term(v):
                    flow["literals"].append(k)
            else:
                flow[k] = v or ""
        flows.append(flow)

    named = set(roles) | {r["term"] for r in reach}
    for fl in flows:
        for k in LINK_KEYS:
            if fl.get(k) and k not in fl["literals"]:
                named.add(fl[k])
    return {"name": name, "label": base.get("label") or f"Flow of {name}", "roles": roles,
            "extends": base.get("extends", ""), "reach": reach,
            "ownTrace": "## Trace" in text,
            "flows": flows, "named": named, "badRoles": bad_roles,
            "trace": trace, "badTrace": bad_trace}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    project = argv[1]
    proj = ROOT / "projects" / project
    if not proj.is_dir():
        print(f"no project at {proj}", file=sys.stderr)
        return 1
    out = proj / "07-streams"
    out.mkdir(exist_ok=True)

    if "--skip" in argv:
        why = argv[argv.index("--skip") + 1]
        (out / "skipped.md").write_text(f"reason: {why}\ndate: {date.today().isoformat()}\n",
                                        encoding="utf-8")
        print(f"07-streams skipped: {why}")
        return 0

    glossary = proj / "05-glossary" / "glossary.md"
    if not glossary.exists():
        print(f"no glossary at {glossary}. Run step 05 first.", file=sys.stderr)
        return 1

    wanted = argv[argv.index("--stream") + 1] if "--stream" in argv else None
    # A process file (front matter holds `process:`) shares the folder and is step 07's other
    # kind of file; tools/render-processes.py reads those. This script reads only streams.
    files = sorted(p for p in out.glob("*.md")
                   if not p.name.startswith("_") and p.name not in ("README.md", "skipped.md")
                   and not is_process_file(p))
    # Every stream is written, because the page reads one data file. --stream narrows the report.
    if wanted and wanted not in [p.stem for p in files]:
        print(f"no stream `{wanted}` in {out}.", file=sys.stderr)
        return 1
    if not files:
        print(f"no stream files in {out}. Write one first.", file=sys.stderr)
        return 1

    streams = [parse_stream(p) for p in files]
    by_name = {s["name"]: s for s in streams}
    for s in streams:
        if not s["extends"]:
            continue
        b = by_name.get(s["extends"])
        if not b:
            print(f"{s['name']}: extends `{s['extends']}`, which has no file.", file=sys.stderr)
            return 1
        s["flows"] = b["flows"] + s["flows"]
        s["roles"] = {**b["roles"], **s["roles"]}
        s["named"] = b["named"] | s["named"]
        if not s["ownTrace"]:
            s["trace"] = b["trace"]
    entries = ro.parse_glossary(glossary.read_text(encoding="utf-8"))
    all_terms = [e["term"] for e in entries]
    known = set(all_terms)

    named = set().union(*(s["named"] for s in streams))
    unresolved = sorted(t for t in named if t not in known)

    # The picture is step 06's, read from its output and never rebuilt, so the two pages show the
    # same terms under the same numbers. A stream term step 06 does not draw is a finding: either
    # the stream reaches past the picture, or step 06 should be rendered at a wider scope.
    onto = proj / "06-ontology" / "ontology-data.js"
    if not onto.exists():
        print(f"no step 06 picture at {onto}. Run tools/render-ontology.py {project} first.",
              file=sys.stderr)
        return 1
    meta, entities, subgraphs, relationships = read_ontology(onto)
    scope = meta.get("scope", "?")
    drawn = {e["name"] for e in entities.values()}
    off_picture = sorted(t for t in named if t in known and t not in drawn)
    stale = glossary.stat().st_mtime > onto.stat().st_mtime

    # The layout keys the glossary term to a slug. Streams speak in terms, so translate once here
    # and let the page speak only in slugs, exactly as the ontology data does.
    key = {e["name"]: k for k, e in entities.items()}

    # Reach is one stated link, no more. The link must be a relation (a depends-on fallback states
    # nothing), and its other end must be a term the stream traces. A row that fails is dropped
    # from the picture and reported, because the glossary, not the stream file, decides the hops.
    for s in streams:
        traced = {key[fl[k]] for fl in s["flows"] for k in s["trace"]
                  if fl.get(k) and fl[k] in key and k not in fl["literals"]}
        s["reachOut"], s["reachDropped"] = [], []
        for r in s["reach"]:
            t = key.get(r["term"])
            if not t:
                s["reachDropped"].append((r["term"], "not on the step 06 picture"))
                continue
            links = [rel for rel in relationships if rel["kind"] == "relation"
                     and t in (rel["from"], rel["to"])
                     and (rel["to"] if rel["from"] == t else rel["from"]) in traced]
            if not links:
                s["reachDropped"].append((r["term"], "no stated relation to a traced money term"))
                continue
            # Only the relation the row quotes is lit. "Party pays Server" is a real link too,
            # but it is money, not the order the row is about.
            said = " ".join(WIKILINK.sub(r"\1", r["link"]).split())
            links = [rel for rel in links
                     if " ".join(WIKILINK.sub(r"\1", rel["rel"]).split()) in said]
            if not links:
                s["reachDropped"].append((r["term"], "its `link` sentence matches no stated relation"))
                continue
            s["reachOut"].append({"node": t, "term": r["term"], "kind": r["kind"],
                                  "link": WIKILINK.sub(r"\1", r["link"]),
                                  "evidence": r["evidence"],
                                  "rels": [rel["id"] for rel in links]})

    out_js = {}
    for s in streams:
        out_js[s["name"]] = {
            "label": s["label"],
            "roles": {key[t]: r for t, r in s["roles"].items() if t in key},
            "trace": s["trace"],
            "reach": s["reachOut"],
            "flows": [
                {**{k: fl[k] for k in ("label", "kind", "confidence", "evidence", "note",
                                       "literals")},
                 **{k: key.get(fl[k], "") for k in LINK_KEYS},
                 **{k + "Term": fl[k] for k in LINK_KEYS}}
                for fl in s["flows"]
            ],
        }

    meta["streams"] = {s["name"]: {"label": s["label"], "flows": len(s["flows"]),
                                   "nodes": len(s["roles"])} for s in streams}
    meta["streamUnresolved"] = unresolved
    meta["streamOffPicture"] = off_picture
    meta["generatedFrom"] = (f"projects/{project}/05-glossary/glossary.md and "
                             f"{len(files)} stream file(s) in 07-streams/")
    meta["title"] = f"{project} value streams"
    meta["subtitle"] = ("The step 06 picture, with a value stream laid over it. A lens marks who "
                        "carries the value and moves nothing. If the lens and the glossary "
                        "disagree, the glossary wins.")

    ro.write_js(out / "stream-data.js", meta, entities, subgraphs, relationships)
    # write_js stamps step 06's name on the file, which is wrong here. Fix the one line.
    p = out / "stream-data.js"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "tools/render-ontology.py", "tools/render-streams.py", 1), encoding="utf-8")
    with p.open("a", encoding="utf-8") as fh:
        fh.write("\nconst streams = " + json.dumps(out_js, ensure_ascii=False, indent=2) + ";\n")

    shutil.copyfile(ROOT / "tools" / "stream-visualizer.html", out / "value-streams.html")
    skipped = out / "skipped.md"
    if skipped.exists():
        skipped.unlink()

    # The report. Same shape as step 06's: what was drawn, then the findings.
    print(f"step 06 picture, scope {scope}: {len(drawn)} of {len(entries)} entries, "
          f"{len(subgraphs)} categories, {len(relationships)} glossary edges")
    if stale:
        print("  WARNING: the glossary is newer than the step 06 picture. Re-run step 06 first.")
    for s in streams:
        if wanted and s["name"] != wanted:
            continue
        counts = {}
        for r in s["roles"].values():
            counts[r] = counts.get(r, 0) + 1
        print(f"\n  {s['name']}: {len(s['flows'])} flows, {len(s['roles'])} nodes")
        print("    roles: " + ", ".join(f"{r} {counts[r]}" for r in ROLES if r in counts))
        by_conf = {}
        for fl in s["flows"]:
            by_conf.setdefault(fl.get("confidence") or "unmarked", []).append(fl["label"])
        for c in ("stated", "inferred", "assumed", "unmarked"):
            if c in by_conf:
                print(f"    {c}: {len(by_conf[c])}")
                for lbl in by_conf[c]:
                    if c != "stated":
                        print(f"      - {lbl}")
        if s["badRoles"]:
            print(f"    UNKNOWN ROLES (typo?): {', '.join(s['badRoles'])}")
        print(f"    trace: {', '.join(s['trace'])}")
        if s["extends"]:
            print(f"    extends: {s['extends']}")
        if s["reach"]:
            print(f"    reach, one link away: {len(s['reachOut'])} of {len(s['reach'])}")
            for r in s["reachOut"]:
                print(f"      + {r['term']}  ({r['kind']})  {r['link']}")
            for term, why in s["reachDropped"]:
                print(f"      - {term}: dropped, {why}")
        if s["badTrace"]:
            print(f"    UNKNOWN TRACE KEYS (typo?): {', '.join(s['badTrace'])}")
        missing = [fl["label"] for fl in s["flows"] if not fl.get("evidence")]
        if missing:
            print(f"    NO EVIDENCE, so not a row yet: {'; '.join(missing)}")

    if off_picture:
        print(f"\n  named by a stream, not on the step 06 picture: {len(off_picture)}")
        for t in off_picture:
            print(f"      - {t}")
    if unresolved:
        print(f"\n  unresolved, a finding for step 05: {len(unresolved)}")
        for t in unresolved:
            print(f"      - {t}")

    # The other half of the check, and the one a reviewer can act on: terms one hop from the
    # stream. The glossary links them to something the stream places, but the stream leaves them
    # out. Each is a question: does this carry value too, or is the boundary right here?
    placed = set().union(*(s["named"] for s in streams))
    cat_of = {e["term"]: (e["fields"].get("category") or e["section"]) for e in entries}
    neighbours = {}
    for e in entries:
        links = set()
        for k in ("relations", "depends_on"):
            for item in e["fields"].get(k, []) or []:
                m = ro.WIKILINK.search(str(item)) if hasattr(ro, "WIKILINK") else WIKILINK.search(str(item))
                if m:
                    links.add(m.group(1).strip())
        for other in links:
            if e["term"] in placed and other not in placed and other in known:
                neighbours.setdefault(other, set()).add(e["term"])
            if other in placed and e["term"] not in placed:
                neighbours.setdefault(e["term"], set()).add(other)
    if neighbours:
        print(f"\n  one hop from the stream, not placed: {len(neighbours)}")
        for t in sorted(neighbours):
            via = ", ".join(sorted(neighbours[t])[:3])
            print(f"      - {t}  ({cat_of.get(t, '?')})  touches: {via}")

    print(f"\nwrote {p.relative_to(ROOT)} and {(out / 'value-streams.html').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
