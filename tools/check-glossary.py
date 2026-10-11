#!/usr/bin/env python3
"""Check a glossary against the entry rules, and report how complete it is.

Usage:
  tools/check-glossary.py <project>                       check 05-glossary/glossary.md
  tools/check-glossary.py <project> --file <path>         check another file, such as a draft
  tools/check-glossary.py <project> --coverage <out.md>   also write the coverage as markdown

Two lists come out, because the glossary is built version over version
(factory/rules/entry-format.md, "Built version over version"):

  errors     something written down breaks a rule. The next version fixes it. Exit code 1.
  warnings   findings worth a look: a hierarchy with one child, a mirror pair, a depends_on loop.

Coverage is neither. A line with no kind, an entry with no relation, an untyped entry: each is
counted and reported, never an error. No step stops because coverage is low.

The rules checked live in factory/rules/entry-format.md and factory/rules/relation-kinds.md.
Reads only what tools/render-ontology.py reads, plus the raw text of each yaml block, because a
leading-zero code is only visible before a parser has turned it into a number.

Standard library only.
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("render_ontology", ROOT / "tools" / "render-ontology.py")
ro = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ro)

TAG = re.compile(r"\s*\([^)]*\)\s*$")
# A bare list item or scalar that starts with a zero: `[062, x]` or `code: 062`.
LEADING_ZERO = re.compile(r"(?:^|[\[,])\s*(0\d+)\s*(?=[,\]]|$)")


def base(alias):
    """The alias without its marker: `walk-in (floor)` -> `walk-in`."""
    return TAG.sub("", alias).strip().lower()


def raw_blocks(text):
    """{term: [yaml lines]} from the raw text, before any parsing."""
    out, term, inside = {}, None, False
    for ln in text.splitlines():
        if ln.startswith("### "):
            term, inside = ln[4:].strip(), False
            out[term] = []
        elif ln.startswith("## "):
            term = None
        elif term and ln.strip().startswith("```yaml"):
            inside = True
        elif term and inside and ln.strip().startswith("```"):
            inside = False
        elif term and inside:
            out[term].append(ln)
    return out


def cycles(graph):
    """Strongly connected groups of more than one node, or a node that points at itself."""
    index, low, stack, on, out, n = {}, {}, [], set(), [], [0]

    def visit(v):
        index[v] = low[v] = n[0]
        n[0] += 1
        stack.append(v)
        on.add(v)
        for w in graph.get(v, ()):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            group = []
            while True:
                w = stack.pop()
                on.discard(w)
                group.append(w)
                if w == v:
                    break
            if len(group) > 1 or v in graph.get(v, ()):
                out.append(sorted(group))

    sys.setrecursionlimit(10000)
    for v in list(graph):
        if v not in index:
            visit(v)
    return out


def check(project, text):
    kinds = ro.kind_table(project)
    entries = ro.parse_glossary(text)
    names = {e["term"]: e for e in entries}
    lower = {t.lower(): t for t in names}
    errors, warnings = [], []
    err = lambda t, msg: errors.append((t, msg))
    warn = lambda t, msg: warnings.append((t, msg))

    lines_of = {e["term"]: ro.relation_lines(e, kinds) for e in entries}
    alias_owner = {}
    for e in entries:
        t, f = e["term"], e["fields"]
        typ = f.get("type")
        if typ and typ not in ro.TYPES:
            err(t, f"type {typ!r} is not one of the twelve")
        given = f.get("relation_kinds")
        if given is not None and len(ro.as_list(given)) != len(lines_of[t]):
            err(t, f"relation_kinds: has {len(ro.as_list(given))} items for {len(lines_of[t])} relations")
        for ln in lines_of[t]:
            if ln["problem"]:
                err(t, f"relation {ln['raw']!r}: {ln['problem']} (one verb, one object, link last)")
            if ln["badKind"]:
                err(t, f"relation {ln['raw']!r}: kind {ln['badKind']!r} is not one of the 21, an "
                       f"inverse, or a project extra")
        for a in ro.as_list(f.get("also_called")):
            if a.count("(") != a.count(")"):
                err(t, f"alias {a!r} has unbalanced brackets; a comma split it. Quote it or drop the comma")
                continue
            b = base(a)
            if b == t.lower():
                err(t, f"alias {a!r} is the entry's own name")
            elif b in lower:
                err(t, f"alias {a!r} is the name of another entry, {lower[b]}. If people say it "
                       f"and mean this, put [[{lower[b]}]] in not_to_be_confused_with: instead")
            key = a.strip().lower()
            if key in alias_owner and alias_owner[key] != t:
                err(t, f"alias {a!r} is also on {alias_owner[key]}; a shared word needs a context tag on each")
            alias_owner.setdefault(key, t)

    # Leading zeros, from the raw text. `rulings:` is left out: ruling ids are read as text by
    # every script, and the published entry shape writes them bare.
    for t, block in raw_blocks(text).items():
        for ln in block:
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", ln)
            if not m or m.group(1) == "rulings":
                continue
            val = m.group(2).strip()
            val = val[1:-1] if val.startswith("[") and val.endswith("]") else val
            for z in LEADING_ZERO.finditer(val):
                err(t, f"{m.group(1)}: {z.group(1)} starts with a zero; a YAML reader takes it as a "
                       f"number. Quote it: \"{z.group(1)}\"")

    # The hierarchy.
    parent = {}
    for t, lines in lines_of.items():
        for ln in lines:
            if ln["kind"] == "is_a" and ln["object"]:
                parent.setdefault(t, []).append(ln["object"])
    for group in cycles(parent):
        err(group[0], "is_a cycle: " + " -> ".join(group + [group[0]]))
    children = {}
    for c, ps in parent.items():
        for p in ps:
            children.setdefault(p, []).append(c)
    for p, cs in sorted(children.items()):
        if len(cs) == 1:
            warn(p, f"is_a parent with one child ({cs[0]}): is the child a state or an alias?")
        elif len(cs) > 12:
            warn(p, f"is_a parent with {len(cs)} children: is a level missing between them?")
        pt = names[p]["fields"].get("type") if p in names else None
        for c in cs:
            ct = names[c]["fields"].get("type")
            if pt and ct and ct != pt and ct != "state":
                warn(c, f"type {ct!r} differs from its parent {p} ({pt!r}); a child shares its parent's type")

    # Mirror pairs: one fact stated from both sides. Kinds make it certain; without them it is a
    # pair to read by eye, because two lines that say different things both stay.
    stated = {}
    for t, lines in lines_of.items():
        for ln in lines:
            if ln["object"]:
                stated.setdefault((t, ln["object"]), []).append(ln)
    for (a, b), lns in sorted(stated.items()):
        if a >= b or (b, a) not in stated:
            continue
        for x in lns:
            for y in stated[(b, a)]:
                if x["kind"] and y["kind"] and kinds[x["kind"]]["inverse"] == y["kind"]:
                    warn(a, f"mirror: {a} {x['verb']} [[{b}]] and {b} {y['verb']} [[{a}]] state one "
                            f"fact; keep the active line")
                elif not (x["kind"] and y["kind"]):
                    warn(a, f"check by eye: {a} {x['verb']} [[{b}]] and {b} {y['verb']} [[{a}]]; "
                            f"a mirror if they say the same thing")

    # depends_on loops: a reading order cannot be followed round a loop.
    deps = {e["term"]: [ro.strip_links(d) for d in ro.as_list(e["fields"].get("depends_on"))]
            for e in entries}
    for group in cycles(deps):
        warn(group[0], "depends_on loop: " + ", ".join(group))
    for e in entries:
        if not e["fields"].get("type"):
            warn(e["term"], "no type")

    return entries, errors, warnings, ro.coverage(entries, kinds)


def coverage_md(project, source, cov, errors, warnings):
    rows = [("Entries", cov["entries"]),
            ("Entries with no valid type", cov["untyped"]),
            ("Relation lines", cov["relationLines"]),
            ("Lines with a kind", cov["linesWithKind"]),
            ("Lines without a kind", cov["linesWithoutKind"]),
            ("Stand-alone entries (no relation either way)", cov["standalone"]),
            ("Errors (rules broken)", len(errors)),
            ("Warnings (findings)", len(warnings))]
    out = [f"# Coverage: {project}", "",
           f"From `{source}`, by `tools/check-glossary.py`. A report, never a gate: see \"Built "
           f"version over version\" in `factory/rules/entry-format.md`.", "",
           "| Measure | Count |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in rows]
    out += ["", "## Entries by type", "", "| Type | Entries |", "|---|---|"]
    out += [f"| `{t}` | {n} |" for t, n in cov["byType"].items()]
    if cov["standaloneTerms"]:
        out += ["", "## Stand-alone entries", "", ", ".join(cov["standaloneTerms"])]
    return "\n".join(out) + "\n"


def main(argv):
    if len(argv) < 2 or argv[1].startswith("-"):
        print(__doc__)
        return 2
    project = argv[1]
    args = argv[2:]
    opt = lambda name: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else None
    path = Path(opt("--file")) if opt("--file") else ROOT / "projects" / project / "05-glossary" / "glossary.md"
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 1
    entries, errors, warnings, cov = check(project, path.read_text(encoding="utf-8"))
    try:
        source = path.resolve().relative_to(ROOT)
    except ValueError:
        source = path
    print(f"{source}: {cov['entries']} entries")
    print(f"  coverage: {cov['linesWithKind']} of {cov['relationLines']} lines carry a kind; "
          f"{cov['standalone']} {'entry stands' if cov['standalone'] == 1 else 'entries stand'} alone; {cov['untyped']} without a valid type")
    print(f"  by type: " + ", ".join(f"{t} {n}" for t, n in cov["byType"].items()))
    if errors:
        print(f"{len(errors)} errors (a rule is broken; fix in the next version):")
        for t, msg in errors:
            print(f"  {t}: {msg}")
    if warnings:
        print(f"{len(warnings)} warnings (findings; not errors):")
        for t, msg in warnings:
            print(f"  {t}: {msg}")
    if not errors:
        print("no errors")
    out = opt("--coverage")
    if out:
        Path(out).write_text(coverage_md(project, source, cov, errors, warnings), encoding="utf-8")
        print(f"wrote {out}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
