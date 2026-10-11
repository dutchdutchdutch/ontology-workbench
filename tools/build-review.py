#!/usr/bin/env python3
"""Build a review package: the key terms, the ontology, the value streams and the processes, as
one folder a stakeholder can open with no tools, plus a zip of it to send.

Usage:
  tools/build-review.py <project>

Writes `projects/<p>/08-publish/review/` (replaced on every build) and
`projects/<p>/08-publish/<p>-review.zip`. The folder holds `index.html`, the landing page, and
one page per view, each next to its data file:

  index.html        the four doors, the status, how to review, where to send corrections
  key-terms.html    the core entries of 05-glossary/glossary.md, by category, with search
  ontology.html     the step 06 picture, as rendered
  value-streams.html the step 07 lenses, when any stream was rendered
  processes.html    the step 07 processes, when any process was rendered

This is not step 08's publish. A review package goes out before `trial`, to people, so it has no
stage gate and writes no log row. Its one gate is freshness: a picture older than what it was drawn
from would show reviewers something the glossary no longer says, so the script stops instead.
Unsigned streams and processes are included and marked as drafts.

Copies are never edited by hand. The data files gain one line, `const reviewHome = ...`, which the
pages read to show a link back to the index. Nothing else in them changes.
"""
import html
import importlib.util
import json
import re
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("render_ontology", ROOT / "tools" / "render-ontology.py")
ro = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ro)

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    return ro.parse_flat_yaml([ln.split(" #", 1)[0] for ln in text[4:end].splitlines()])


def project_values(project):
    """display_name, and who receives corrections: publish.contact, else the first person."""
    text = (ROOT / "projects" / project / "project.yaml").read_text(encoding="utf-8")
    display = re.search(r"^display_name:\s*(.+?)\s*(#.*)?$", text, re.M)
    contact = re.search(r"^publish:\s*$.*?^\s+contact:\s*(.+?)\s*(#.*)?$", text, re.M | re.S)
    person = re.search(r"^people:.*?name:\s*([^,}]+)", text, re.M | re.S)
    who = (contact.group(1) if contact else person.group(1) if person else "the glossary owner").strip()
    return (display.group(1).strip() if display else project), ro.unquote(who)


def key_terms(glossary):
    """The core entries, by category in reading order, with definitions as safe HTML. A wikilink
    to another core term becomes a link to its entry; a link to anything else stays plain text,
    because the page holds only the core."""
    entries = ro.parse_glossary(glossary.read_text(encoding="utf-8"))
    kinds = ro.kind_table(glossary.parent.parent.name)
    core = [e for e in entries if e["fields"].get("core") is True]
    core_names = {e["term"] for e in core}
    slug = lambda s: "t-" + ro.slug(s).lower()

    def def_html(text):
        out, pos = [], 0
        for m in ro.WIKILINK.finditer(text):
            out.append(html.escape(text[pos:m.start()], quote=False))
            name = m.group(1).strip()
            out.append(f'<a href="#{slug(name)}">{html.escape(name)}</a>' if name in core_names
                       else html.escape(name))
            pos = m.end()
        out.append(html.escape(text[pos:], quote=False))
        return "".join(out)

    cats, order = {}, []
    for e in core:
        c = e["fields"].get("category") or e["section"] or "Other"
        if c not in cats:
            cats[c] = []
            order.append(c)
        also = e["fields"].get("also_called") or []
        cats[c].append({
            "term": e["term"], "slug": slug(e["term"]), "type": e["fields"].get("type", ""),
            "core": True, "def": def_html(e["definition"]), "plain": ro.strip_links(e["definition"]),
            "also": [str(a) for a in (also if isinstance(also, list) else [also])],
            "status": e["fields"].get("status", ""),
            "isA": next((ln["object"] for ln in ro.relation_lines(e, kinds)
                         if ln["kind"] == "is_a" and ln["object"]), None),
        })
    # Reading order is the order the categories first appear in the glossary, which step 05 sets.
    section_order = []
    for e in entries:
        c = e["fields"].get("category") or e["section"] or "Other"
        if c in cats and c not in section_order:
            section_order.append(c)
    return [{"name": c, "entries": cats[c]} for c in section_order], len(core), len(entries)


def read_js_const(path, name):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^const " + name + r" = (.*?);\n(?=\n?const |\Z)", text, re.S | re.M)
    return json.loads(m.group(1)) if m else None


def fail(msg):
    print(msg, file=sys.stderr)
    return 1


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    project = argv[1]
    proj = ROOT / "projects" / project
    if not proj.is_dir():
        return fail(f"no project at {proj}")
    glossary = proj / "05-glossary" / "glossary.md"
    if not glossary.exists():
        return fail("no published glossary. Run step 05 first.")
    hdr = front_matter(glossary)
    display, contact = project_values(project)

    onto_page, onto_data = proj / "06-ontology" / "ontology.html", proj / "06-ontology" / "ontology-data.js"
    s07 = proj / "07-streams"
    stream_page, stream_data = s07 / "value-streams.html", s07 / "stream-data.js"
    proc_page, proc_data = s07 / "processes.html", s07 / "process-data.js"
    authored = sorted(p for p in s07.glob("*.md")
                      if not p.name.startswith("_") and p.name not in ("README.md", "skipped.md")) if s07.is_dir() else []
    procs = [p for p in authored if "process" in front_matter(p)]
    streams = [p for p in authored if p not in procs]

    problems = []
    if not onto_page.exists():
        problems.append("no step 06 picture. Run tools/render-ontology.py " + project + " --core")
    elif glossary.stat().st_mtime > onto_page.stat().st_mtime:
        problems.append("the ontology is older than the glossary. Run tools/render-ontology.py " + project + " --core")
    if stream_page.exists() and max([p.stat().st_mtime for p in streams] + [onto_data.stat().st_mtime]) > stream_page.stat().st_mtime:
        problems.append("the value streams are older than a stream file or the ontology. Run tools/render-streams.py " + project)
    if proc_page.exists() and max([p.stat().st_mtime for p in procs] + [glossary.stat().st_mtime]) > proc_page.stat().st_mtime:
        problems.append("the processes are older than a process file or the glossary. Run tools/render-processes.py " + project)
    if problems:
        return fail("nothing built:\n  " + "\n  ".join(problems))

    out = proj / "08-publish" / "review"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    home = f"\nconst reviewHome = {json.dumps({'href': 'index.html', 'label': display + ' review'})};\n"
    today = date.today().isoformat()

    def copy(page, data, name):
        shutil.copyfile(page, out / name)
        (out / data.name).write_text(data.read_text(encoding="utf-8") + home, encoding="utf-8")

    unsigned = lambda files: sum(1 for p in files if not DATE.match(str(front_matter(p).get("reviewed", "")).strip()))
    items = []

    cats, n_core, n_all = key_terms(glossary)
    gmeta = {"project": display, "title": f"{display} key terms", "count": n_core, "allCount": n_all,
             "publishedFrom": hdr.get("published_from", ""), "stage": hdr.get("stage", ""),
             "generatedFrom": f"projects/{project}/05-glossary/glossary.md"}
    (out / "glossary-data.js").write_text("// Generated by tools/build-review.py. Do not edit.\nconst glossaryData = "
                                          + json.dumps({"meta": gmeta, "categories": cats}, ensure_ascii=False, indent=1)
                                          + ";\n" + home, encoding="utf-8")
    shutil.copyfile(ROOT / "tools" / "glossary-visualizer.html", out / "key-terms.html")
    items.append({"key": "terms", "href": "key-terms.html", "title": "Key terms",
                  "what": "The words we use for the business, each with one meaning. Only the core: the smallest set a new person must learn first.",
                  "stats": f"{n_core} terms in {len(cats)} categories. Specialists review the full {n_all} separately.", "draft": ""})

    copy(onto_page, onto_data, "ontology.html")
    ometa = read_js_const(onto_data, "meta") or {}
    n_drawn = len(read_js_const(onto_data, "entities") or {})
    items.append({"key": "ontology", "href": "ontology.html", "title": "Ontology",
                  "what": "The same key terms as a map: how each one connects to the others. Click a term to see what it feeds and what feeds it.",
                  "stats": f"{n_drawn} terms, the same set as the key terms.", "draft": ""})

    if stream_page.exists():
        copy(stream_page, stream_data, "value-streams.html")
        smeta = (read_js_const(stream_data, "meta") or {}).get("streams", {})
        labels = [v["label"] for v in smeta.values()]
        u = unsigned(streams)
        items.append({"key": "streams", "href": "value-streams.html", "title": "Value streams",
                      "what": "Where value comes from and where it goes, laid over the map: who passes what to whom, through what, and when.",
                      "stats": f"{len(labels)} stream{'s' if len(labels) != 1 else ''}: " + "; ".join(labels),
                      "draft": "draft" if u else ""})

    if proc_page.exists():
        copy(proc_page, proc_data, "processes.html")
        pdata = read_js_const(proc_data, "processData") or {}
        titles = [p["title"] for p in pdata.get("processes", {}).values()]
        u = unsigned(procs)
        items.append({"key": "processes", "href": "processes.html", "title": "Processes",
                      "what": f"Who does what, in what order, for the work that repeats. People, AI agents and the {display} team, step by step.",
                      "stats": f"{len(titles)} process{'es' if len(titles) != 1 else ''}: " + "; ".join(titles),
                      "draft": "draft" if u else ""})

    rmeta = {"project": project, "display": display, "contact": contact, "built": today, "allCount": n_all,
             "publishedFrom": hdr.get("published_from", ""), "stage": hdr.get("stage", "")}
    (out / "review-data.js").write_text("// Generated by tools/build-review.py. Do not edit.\nconst reviewData = "
                                        + json.dumps({"meta": rmeta, "items": items}, ensure_ascii=False, indent=1) + ";\n",
                                        encoding="utf-8")
    shutil.copyfile(ROOT / "tools" / "review-index.html", out / "index.html")

    # The zip unpacks to one folder named for the project, so nothing lands loose on a desktop.
    z = proj / "08-publish" / f"{project}-review.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out.iterdir()):
            zf.write(p, f"{project}-review/{p.name}")

    print(f"built {out.relative_to(ROOT)}: {', '.join(i['title'] for i in items)}")
    print(f"  key terms: {n_core} of {n_all}; glossary from {hdr.get('published_from')} at stage {hdr.get('stage')}")
    for i in items:
        if i["draft"]:
            print(f"  {i['title']}: marked on the index as {i['draft']}")
    print(f"  corrections go to {contact}")
    print(f"zipped {z.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
