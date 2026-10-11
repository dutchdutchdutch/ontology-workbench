#!/usr/bin/env python3
"""Stage a project's published vocabulary for step 08, and keep the publish log.

Usage:
  tools/stage-publish.py <project>                          build 08-publish/outbox/, log one
                                                            staged row per destination
  tools/stage-publish.py <project> --sent <dest> "<receipt>"  mark the latest staged row for
                                                            <dest> as sent today
  tools/stage-publish.py <project> --verify <dest> <dir>    compare a local copy of what sits at
                                                            <dest> with what was last sent there

The outbox is the exact set of files that goes out: copies of step 05, 06 and 07 output, each with
a one-line "published copy, do not edit" note. The log, `08-publish/publish-log.md`, holds one row
per destination per send. A row with an empty `sent` cell is staged and not yet out.

This script never touches the network. Sending is done by Claude through the connected servers or
git, the same way step 00 pulls. `--verify` reads a folder someone already downloaded or cloned.

The destinations, the file list and the contact come from the `publish:` block of
projects/<p>/project.yaml. Nothing project-specific lives here.
"""
import hashlib
import importlib.util
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Step 06 owns the small yaml helpers. Import them rather than copying them.
_spec = importlib.util.spec_from_file_location("render_ontology", ROOT / "tools" / "render-ontology.py")
ro = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ro)

# What a name in `publish: files:` sends. Paths are relative to the project folder.
FILES = {
    "glossary": ["05-glossary/glossary.md"],
    "core-terms": ["05-glossary/core-terms.md"],
    "about-core-terms": ["05-glossary/about-core-terms.md"],
    "taxonomy": ["05-glossary/taxonomy.md"],
    "backlog": ["05-glossary/backlog.md"],
    "ontology": ["06-ontology/ontology.html", "06-ontology/ontology-data.js"],
    # The machine lens, for agents outside the workspace. JSON holds no comment, so it carries no
    # "published copy" note; the outbox README lists it with its hash like every other file.
    "ontology-machine": ["06-ontology/ontology-machine.json"],
    "streams": ["07-streams/value-streams.html", "07-streams/stream-data.js"],
    "processes": ["07-streams/processes.html", "07-streams/process-data.js"],
}

# Where a destination can be. The script only records the kind; Claude does the sending.
KINDS = ("drive", "repo", "folder")

# A glossary is sent only once people use it. `review` is still being read.
SENDABLE = ("trial", "adopted")

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOG_HEADER = "| # | staged | sent | from | stage | destination | fingerprint | receipt |"


def load_publish(project):
    """The `publish:` block: folder, contact, files, destinations ("kind where" per line)."""
    out = {"folder": "", "contact": "", "files": [], "destinations": []}
    path = ROOT / "projects" / project / "project.yaml"
    inside, key = False, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if re.match(r"^publish:\s*$", line):
            inside, key = True, None
            continue
        if inside and not line.startswith(" "):
            break
        if not inside:
            continue
        m = re.match(r"^\s+(folder|contact|files|destinations):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if key in ("folder", "contact"):
                out[key] = ro.unquote(val)
            elif val.startswith("[") and val.endswith("]"):
                out[key] = [v for v in ro.split_inline_list(val[1:-1]) if v]
            continue
        if key in ("files", "destinations") and line.strip().startswith("- "):
            out[key].append(ro.unquote(line.strip()[2:]))
    dests = []
    for d in out["destinations"]:
        kind, _, where = d.partition(" ")
        dests.append({"kind": kind.strip(), "where": where.strip(), "name": f"{kind.strip()}:{where.strip()}"})
    out["destinations"] = dests
    return out


def header_of(path):
    """The YAML front matter of a markdown file, flat, or {}."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    lines = [ln.split(" #", 1)[0] for ln in text[4:end].splitlines()]
    return ro.parse_flat_yaml(lines) if end > 0 else {}


def stamp(text, suffix, note):
    """The file with a one-line published-copy note, placed where each format allows it."""
    if suffix == ".md":
        line = f"> {note}\n\n"
        if text.startswith("---\n"):
            end = text.find("\n---\n", 4)
            if end > 0:
                cut = end + len("\n---\n")
                return text[:cut] + "\n" + line + text[cut:].lstrip("\n")
        return line + text
    if suffix == ".html":
        line = f"<!-- {note} -->\n"
        if text.lower().startswith("<!doctype"):
            first, _, rest = text.partition("\n")
            return first + "\n" + line + rest
        return line + text
    if suffix == ".js":
        return f"// {note}\n" + text
    return text


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(folder):
    """One short hash for a folder of published files. README.md is left out: it carries the
    fingerprint, so it cannot be part of it."""
    h = hashlib.sha256()
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.name != "README.md":
            h.update(p.name.encode() + b"\0" + sha(p).encode() + b"\n")
    return h.hexdigest()[:12]


def read_log(path):
    """Header lines and the table rows, each a list of cells."""
    if not path.exists():
        return None, []
    head, rows = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and not line.startswith(LOG_HEADER) and not re.match(r"^\|[-| ]+\|$", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif not line.startswith("|"):
            head.append(line)
    return head, rows


def write_log(path, project, head, rows):
    if head is None:
        head = [f"# Publish log: {project}", "",
                "One row per destination per send. Written by `tools/stage-publish.py`; Claude",
                "fills `sent` and `receipt` after each send with `--sent`. A row with an empty `sent`",
                "cell is staged and not yet out. `superseded` means a newer staging replaced it",
                "before it was sent. Rows are never removed.", ""]
    while head and not head[-1].strip():
        head.pop()
    body = [LOG_HEADER, "|---|---|---|---|---|---|---|---|"]
    body += ["| " + " | ".join(r) + " |" for r in rows]
    path.write_text("\n".join(head + [""] + body) + "\n", encoding="utf-8")


def stage(project, proj, cfg):
    glossary = proj / "05-glossary" / "glossary.md"
    if not glossary.exists():
        return fail("no published glossary. Run step 05 first.")
    hdr = header_of(glossary)
    stage_, source = hdr.get("stage", ""), hdr.get("published_from", "")
    if stage_ not in SENDABLE:
        return fail(f"05-glossary/glossary.md is at stage `{stage_ or 'none'}`. Step 08 sends a "
                    f"glossary at {' or '.join(SENDABLE)} only. Reviewers read it in place.")
    if not cfg["destinations"]:
        return fail("project.yaml has no `publish: destinations:`. Name at least one.")
    bad = [d["name"] for d in cfg["destinations"] if d["kind"] not in KINDS or not d["where"]]
    if bad:
        return fail(f"unknown or empty destination(s): {', '.join(bad)}. "
                    f"Write `- <kind> <where>`, kind one of {', '.join(KINDS)}.")
    names = cfg["files"] or ["glossary", "core-terms", "about-core-terms", "taxonomy"]
    unknown = [n for n in names if n not in FILES]
    if unknown:
        return fail(f"unknown name(s) in `publish: files:`: {', '.join(unknown)}. "
                    f"Known: {', '.join(FILES)}.")

    # Each picture must be newer than what it was drawn from, or it would send a stale view.
    problems = []
    for n in names:
        for rel in FILES[n]:
            if not (proj / rel).exists():
                problems.append(f"{n}: {rel} does not exist")
    onto = proj / "06-ontology" / "ontology.html"
    if "ontology" in names and onto.exists() and glossary.stat().st_mtime > onto.stat().st_mtime:
        problems.append("ontology: older than glossary.md. Re-run tools/render-ontology.py")
    lens = proj / "06-ontology" / "ontology-machine.json"
    if "ontology-machine" in names and lens.exists() and glossary.stat().st_mtime > lens.stat().st_mtime:
        problems.append("ontology-machine: older than glossary.md. Re-run tools/render-ontology.py")
    # Step 07 holds two kinds of authored file. Both are hypotheses until signed, and each page
    # must be newer than every file it was drawn from.
    authored = sorted(p for p in (proj / "07-streams").glob("*.md")
                      if not p.name.startswith("_") and p.name not in ("README.md", "skipped.md"))
    procs = [p for p in authored if "process" in header_of(p)]
    streams = [p for p in authored if p not in procs]
    for name, files_, page, extra, script in (
            ("streams", streams, proj / "07-streams" / "value-streams.html",
             proj / "06-ontology" / "ontology-data.js", "tools/render-streams.py"),
            ("processes", procs, proj / "07-streams" / "processes.html",
             glossary, "tools/render-processes.py")):
        if name not in names:
            continue
        unsigned = [p.name for p in files_ if not DATE.match(str(header_of(p).get("reviewed", "")).strip())]
        if unsigned:
            problems.append(f"{name}: not reviewed, so still a hypothesis: {', '.join(unsigned)}")
        newest = max([p.stat().st_mtime for p in files_] + [extra.stat().st_mtime if extra.exists() else 0])
        if page.exists() and newest > page.stat().st_mtime:
            problems.append(f"{name}: older than one of its files. Re-run {script}")
    if problems:
        return fail("nothing staged:\n  " + "\n  ".join(problems))

    today = date.today().isoformat()
    contact = cfg["contact"] or "the glossary owner"
    note = (f"Published copy of the {project} vocabulary, draft {source}, stage {stage_}, published "
            f"{today}. Do not edit it here: it is replaced on every publish. Send changes to {contact}.")

    out = proj / "08-publish" / "outbox"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for n in names:
        for rel in FILES[n]:
            src = proj / rel
            (out / src.name).write_text(stamp(src.read_text(encoding="utf-8"), src.suffix, note),
                                        encoding="utf-8")
    fp = fingerprint(out)

    files = sorted(p for p in out.iterdir() if p.is_file())
    readme = [f"# {project} vocabulary: published copy", "",
              f"Published from draft `{source}` at stage `{stage_}` on {today}. Fingerprint `{fp}`.", "",
              "Every file here is generated. Do not edit any of them: the next publish replaces the",
              f"whole folder. Send a correction to {contact}; it becomes a feedback row or a ruling",
              "and comes back in the next publish.", "",
              "Start with `core-terms.md`. Open `ontology.html` in a browser for the picture." if
              "core-terms" in names else "Start with `glossary.md`.", "",
              "| File | sha256 |", "|---|---|"]
    readme += [f"| `{p.name}` | `{sha(p)[:16]}` |" for p in files]
    (out / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    log = proj / "08-publish" / "publish-log.md"
    head, rows = read_log(log)
    dest_names = {d["name"] for d in cfg["destinations"]}
    for r in rows:
        if len(r) >= 8 and r[5] in dest_names and not r[2]:
            r[2] = "superseded"
    n0 = max([int(r[0]) for r in rows if r and r[0].isdigit()] + [0])
    for i, d in enumerate(cfg["destinations"], 1):
        rows.append([str(n0 + i), today, "", source, stage_, d["name"], fp, ""])
    write_log(log, project, head, rows)

    print(f"staged {len(files)} file(s) from {source} at stage {stage_}, fingerprint {fp}")
    for p in files:
        print(f"  {p.relative_to(ROOT)}")
    print(f"logged {len(cfg['destinations'])} staged row(s) in {log.relative_to(ROOT)}:")
    for d in cfg["destinations"]:
        print(f"  {d['name']}  into folder `{cfg['folder'] or '(root)'}`")
    print("\nNext: send the outbox to each destination, then mark each with "
          f"tools/stage-publish.py {project} --sent <destination> \"<receipt>\"")
    return 0


def mark_sent(project, proj, dest, receipt):
    log = proj / "08-publish" / "publish-log.md"
    head, rows = read_log(log)
    if head is None:
        return fail("no publish-log.md. Stage first.")
    for r in reversed(rows):
        if len(r) >= 8 and r[5] == dest and not r[2]:
            r[2], r[7] = date.today().isoformat(), receipt.replace("|", "/")
            write_log(log, project, head, rows)
            print(f"row {r[0]}: {dest} sent {r[2]}, fingerprint {r[6]}")
            return 0
    return fail(f"no staged row for `{dest}` waiting to be sent.")


def verify(project, proj, dest, folder):
    log = proj / "08-publish" / "publish-log.md"
    _, rows = read_log(log)
    sent = [r for r in rows if len(r) >= 8 and r[5] == dest and DATE.match(r[2])]
    if not sent:
        return fail(f"nothing has been sent to `{dest}` yet.")
    want, folder = sent[-1][6], Path(folder)
    if not folder.is_dir():
        return fail(f"no folder at {folder}.")
    got = fingerprint(folder)
    if got == want:
        print(f"{dest}: matches row {sent[-1][0]}, sent {sent[-1][2]} from {sent[-1][3]}, fingerprint {got}")
        return 0
    print(f"{dest}: DRIFTED. The copy there is {got}, the log says {want} (row {sent[-1][0]}).")
    # Name the files, when the outbox still holds what was sent.
    readme = proj / "08-publish" / "outbox" / "README.md"
    if readme.exists() and fingerprint(readme.parent) == want:
        listed = dict(re.findall(r"^\| `([^`]+)` \| `([0-9a-f]+)` \|$",
                                 readme.read_text(encoding="utf-8"), re.M))
        here = {p.name for p in folder.iterdir() if p.is_file() and p.name != "README.md"}
        for name in sorted(set(listed) | here):
            p = folder / name
            if name not in here:
                print(f"  missing there: {name}")
            elif name not in listed:
                print(f"  added there:   {name}")
            elif not sha(p).startswith(listed[name]):
                print(f"  edited there:  {name}")
    return 1


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
    if "--sent" in argv:
        i = argv.index("--sent")
        if len(argv) < i + 3:
            return fail('usage: --sent <destination> "<receipt>"')
        return mark_sent(project, proj, argv[i + 1], argv[i + 2])
    if "--verify" in argv:
        i = argv.index("--verify")
        if len(argv) < i + 3:
            return fail("usage: --verify <destination> <local folder>")
        return verify(project, proj, argv[i + 1], argv[i + 2])
    return stage(project, proj, load_publish(project))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
