#!/usr/bin/env python3
"""Render a project's processes: who does what, in what order, keyed to the glossary.

Usage:
  tools/render-processes.py <project>                  render every process in 07-streams/
  tools/render-processes.py <project> --process <name> render every process, report only this one

A process is a picture of work, not of concepts. Lanes are who does it, columns are the order,
boxes are the activities. It is not drawn over the step 06 ontology picture, because an activity
is not a term and the lanes and the order are the point. What ties it to the vocabulary is that
every box names the glossary terms it uses, and the page shows the glossary's own definition for
each. This script checks every term against `05-glossary/glossary.md` and invents no definition.
A term named in a process file with no glossary entry is reported as unresolved: a finding for
step 05, never an error here.

The process file is authored by a person, in `projects/<p>/07-streams/<name>.md`, and is told
apart from a value stream file by `process:` in its front matter. It is a hypothesis until
somebody signs it (`reviewed:` holds a date).
"""
import html
import importlib.util
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Step 06 owns the glossary parser and the small yaml helpers. Import, never copy.
_spec = importlib.util.spec_from_file_location("render_ontology", ROOT / "tools" / "render-ontology.py")
ro = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ro)

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
HEADING = re.compile(r"^### (.+)$", re.M)
LANE_KINDS = ("people", "ai", "team")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def front_matter(text):
    """The flat YAML between the first two `---` lines, comments stripped, or {}."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    lines = [ln.split(" #", 1)[0] for ln in text[4:end].splitlines()]
    return ro.parse_flat_yaml(lines), text[end + 4:]


def section(text, name):
    """The body of `## <name>`, up to the next `## `, or ""."""
    m = re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def fenced(block):
    m = re.search(r"```yaml\n(.*?)```", block, re.S)
    return m.group(1) if m else ""


def inline_map(s):
    """`{ label: "A & b", who: "c", kind: people }` as a dict. One level, no nesting."""
    out = {}
    s = s.strip()
    if s.startswith("{") and s.endswith("}"):
        s = s[1:-1]
    for m in re.finditer(r'([A-Za-z_][A-Za-z0-9_]*)\s*:\s*("([^"]*)"|\'([^\']*)\'|([^,}]*))', s):
        key = m.group(1)
        val = m.group(3) if m.group(3) is not None else m.group(4) if m.group(4) is not None else m.group(5)
        out[key] = (val or "").strip()
    return out


def parse_lanes(block):
    """`floor: { label: ..., who: ..., kind: team }`, one lane per line, in file order."""
    lanes = []
    for raw in fenced(block).splitlines():
        line = raw.split(" #", 1)[0].strip()
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(\{.*\})\s*$", line)
        if not m:
            continue
        d = inline_map(m.group(2))
        lanes.append({"id": m.group(1), "label": d.get("label", m.group(1)),
                      "who": d.get("who", ""), "kind": d.get("kind", "people")})
    return lanes


def parse_edges(value):
    """`[checker]`, `[{ to: a, label: "x" }, { to: b }]`, or a `- ` list already split.

    An edge is {to, label}. The yaml helpers split inline lists on commas, which breaks inside
    braces, so braces are taken out first and the bare ids after.
    """
    if value is None:
        return []
    items = value if isinstance(value, list) else [value]
    text = ", ".join(str(i) for i in items)
    edges = []
    for m in re.finditer(r"\{[^}]*\}", text):
        d = inline_map(m.group(0))
        if d.get("to"):
            edges.append({"to": d["to"], "label": d.get("label", "")})
    rest = re.sub(r"\{[^}]*\}", "", text)
    for tok in rest.split(","):
        tok = ro.unquote(tok.strip())
        if tok:
            edges.append({"to": tok, "label": ""})
    return edges


def parse_box_yaml(block):
    """The box yaml, with `next` and `when_needed` kept raw so parse_edges can read the braces."""
    raw = fenced(block)
    data = ro.parse_flat_yaml(raw.splitlines())
    for key in ("next", "when_needed"):
        m = re.search(r"^" + key + r":\s*(.*)$", raw, re.M)
        if m:
            val = m.group(1).strip()
            if val.startswith("[") and val.endswith("]"):
                val = val[1:-1]
            data[key] = parse_edges(val) if val else parse_edges(data.get(key))
    return data


def detail_html(chunk):
    """The prose after the yaml block, as paragraphs. Wikilinks become term links."""
    after = chunk.split("```", 2)
    prose = after[2] if len(after) == 3 else ""
    paras = [p.strip() for p in re.split(r"\n\s*\n", prose) if p.strip()]
    out = []
    for p in paras:
        if p.startswith("#"):
            break
        safe = html.escape(" ".join(p.split()), quote=False)
        safe = re.sub(r"\[\[([^\]]+)\]\]",
                      lambda m: f'<a class="term" data-term="{html.escape(m.group(1))}">{html.escape(m.group(1))}</a>',
                      safe)
        safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
        safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
        out.append(f"<p>{safe}</p>")
    return "".join(out)


def parse_process(path):
    text = path.read_text(encoding="utf-8")
    fm, body = front_matter(text)
    name = str(fm.get("process") or path.stem)
    lanes = parse_lanes(section(body, "Lanes"))
    steps = ro.parse_flat_yaml(fenced(section(body, "Steps")).splitlines()).get("steps", [])
    steps = steps if isinstance(steps, list) else [steps]
    one_line = " ".join(section(body, "In one line").split())

    boxes, problems = [], []
    for chunk in re.split(r"\n(?=### )", section(body, "Boxes")):
        h = HEADING.match(chunk)
        if not h:
            continue
        f = parse_box_yaml(chunk)
        quote = " ".join(ln.strip()[2:].strip() for ln in chunk.splitlines() if ln.strip().startswith("> "))
        box = {
            "id": str(f.get("id") or ro.slug(h.group(1))),
            "title": h.group(1).strip(),
            "card": quote,
            "step": int(f["step"]) if str(f.get("step", "")).isdigit() else 0,
            "lane": str(f.get("lane", "")),
            "humanMoment": f.get("human_moment") is True,
            "tag": str(f.get("tag", "")),
            "terms": [m.group(1).strip() for t in (f.get("terms") or []) for m in [WIKILINK.search(str(t))] if m],
            "next": f.get("next") if isinstance(f.get("next"), list) else [],
            "whenNeeded": f.get("when_needed") if isinstance(f.get("when_needed"), list) else [],
            "detail": detail_html(chunk),
        }
        boxes.append(box)

    # Paths: the same process at rising levels of trouble. Each is a subset of the boxes; the
    # page dims what is outside it. Same shape as a box: heading, blockquote, yaml, prose.
    paths = []
    for chunk in re.split(r"\n(?=### )", section(body, "Paths")):
        h = HEADING.match(chunk)
        if not h:
            continue
        f = ro.parse_flat_yaml(fenced(chunk).splitlines())
        ids = f.get("boxes") or []
        paths.append({
            "id": str(f.get("id") or ro.slug(h.group(1))),
            "label": h.group(1).strip(),
            "when": " ".join(ln.strip()[2:].strip() for ln in chunk.splitlines() if ln.strip().startswith("> ")),
            "share": str(f.get("share", "")),
            "boxes": [str(i) for i in (ids if isinstance(ids, list) else [ids])],
            "detail": detail_html(chunk),
        })

    lane_ids = {l["id"] for l in lanes}
    box_ids = {b["id"] for b in boxes}
    for l in lanes:
        if l["kind"] not in LANE_KINDS:
            problems.append(f"lane {l['id']}: kind `{l['kind']}` is not one of {', '.join(LANE_KINDS)}")
    for b in boxes:
        if b["lane"] not in lane_ids:
            problems.append(f"box {b['id']}: lane `{b['lane']}` is not in ## Lanes")
        if not 1 <= b["step"] <= len(steps):
            problems.append(f"box {b['id']}: step {b['step']} is not 1 to {len(steps)}")
        for e in b["next"] + b["whenNeeded"]:
            if e["to"] not in box_ids:
                problems.append(f"box {b['id']}: edge to `{e['to']}`, which is no box")
    for pth in paths:
        for i in pth["boxes"]:
            if i not in box_ids:
                problems.append(f"path {pth['id']}: box `{i}` does not exist")
        if not pth["boxes"]:
            problems.append(f"path {pth['id']}: names no box")
    for b in boxes:
        if not b["terms"]:
            problems.append(f"box {b['id']}: names no glossary term, so nothing ties it to the vocabulary")
    dup = [i for i in box_ids if sum(1 for b in boxes if b["id"] == i) > 1]
    for i in dup:
        problems.append(f"box id `{i}` is used twice")

    reviewed = str(fm.get("reviewed", "")).strip()
    h1 = re.search(r"^# (.+)$", body, re.M)
    return {
        "name": name,
        "title": str(fm.get("title") or (h1.group(1).strip() if h1 else name)),
        "cadence": str(fm.get("cadence", "")),
        "target": str(fm.get("target", "")),
        "source": str(fm.get("source", "")),
        "reviewed": reviewed if DATE.match(reviewed) else "",
        "oneLine": one_line,
        "lanes": lanes,
        "steps": [str(s) for s in steps],
        "boxes": boxes,
        "paths": paths,
        "problems": problems,
        "file": path.name,
    }


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
    glossary = proj / "05-glossary" / "glossary.md"
    if not glossary.exists():
        print(f"no glossary at {glossary}. Run step 05 first.", file=sys.stderr)
        return 1

    files = []
    for p in sorted(out.glob("*.md")):
        if p.name.startswith("_") or p.name in ("README.md", "skipped.md"):
            continue
        fm, _ = front_matter(p.read_text(encoding="utf-8"))
        if "process" in fm:
            files.append(p)
    if not files:
        print(f"no process file in {out}. Copy _process.template.md and write one.", file=sys.stderr)
        return 1
    wanted = argv[argv.index("--process") + 1] if "--process" in argv else None

    processes = [parse_process(p) for p in files]
    if wanted and wanted not in [pr["name"] for pr in processes]:
        print(f"no process `{wanted}` in {out}.", file=sys.stderr)
        return 1

    entries = ro.parse_glossary(glossary.read_text(encoding="utf-8"))
    by_term = {e["term"]: e for e in entries}
    named = sorted({t for pr in processes for b in pr["boxes"] for t in b["terms"]}
                   | {m.group(1).strip() for pr in processes for b in pr["boxes"]
                      for m in re.finditer(r'data-term="([^"]+)"', b["detail"])})
    named = [html.unescape(t) for t in named]
    unresolved = sorted(t for t in named if t not in by_term)
    terms = {}
    for t in named:
        e = by_term.get(t)
        if e:
            terms[t] = {"name": t, "fullDef": ro.strip_links(e["definition"]),
                        "category": e["fields"].get("category") or e["section"] or "",
                        "core": e["fields"].get("core") is True,
                        "type": e["fields"].get("type", ""), "status": e["fields"].get("status", ""),
                        "alsoCalled": ro.as_list(e["fields"].get("also_called"))}

    meta = {
        "project": project,
        "title": f"{project} processes",
        "generatedFrom": f"projects/{project}/05-glossary/glossary.md and {len(files)} process file(s) in 07-streams/",
        "generatedBy": "tools/render-processes.py",
        "generated": date.today().isoformat(),
        "definitionsFrom": f"projects/{project}/05-glossary/glossary.md",
        "unresolved": unresolved,
    }
    data = {"meta": meta, "processes": {pr["name"]: {k: v for k, v in pr.items() if k != "problems"}
                                        for pr in processes}, "terms": terms}
    js = out / "process-data.js"
    js.write_text("// Generated by tools/render-processes.py. Do not edit; change the process file "
                  "or the glossary and render again.\nconst processData = "
                  + json.dumps(data, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    shutil.copyfile(ROOT / "tools" / "process-visualizer.html", out / "processes.html")

    for pr in processes:
        if wanted and pr["name"] != wanted:
            continue
        print(f"{pr['name']}: {len(pr['boxes'])} boxes, {len(pr['steps'])} steps, {len(pr['lanes'])} lanes"
              f"{', signed ' + pr['reviewed'] if pr['reviewed'] else ', unsigned'}")
        for pth in pr["paths"]:
            print(f"  path {pth['id']}: {len(pth['boxes'])} of {len(pr['boxes'])} boxes"
                  f"{', ' + pth['share'] if pth['share'] else ''}")
        edges = sum(len(b["next"]) + len(b["whenNeeded"]) for b in pr["boxes"])
        print(f"  edges: {edges}; boxes with a longer explanation: "
              f"{sum(1 for b in pr['boxes'] if b['detail'])} of {len(pr['boxes'])}")
        for p in pr["problems"]:
            print(f"  PROBLEM: {p}")
    print(f"terms named: {len(named)}, resolved: {len(terms)}")
    if unresolved:
        print(f"unresolved, a finding for step 05: {len(unresolved)}")
        for t in unresolved:
            print(f"  - {t}")
    print(f"wrote {js.relative_to(ROOT)} and {(out / 'processes.html').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
