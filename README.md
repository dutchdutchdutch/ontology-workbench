# One-Vocabulary

A workflow for building source-of-truth glossaries for product teams, and drawing them as an
ontology. Plain folders and markdown files, a few small scripts, nothing to install.

The idea: stop the drift that comes from loose readings of a product's key terms. AI does not know
your domain, although it acts as if it does, confidently. Agents need to be told what the key terms
mean, and people need to be reminded. This workflow finds the key terms, checks that they are
clearly defined, and checks that they are used the same way in shared drive documents, in Linear
or Jira issues, and in git (pull request titles and branch names: a proxy for the code, not the
code itself).

It is built to be run by [Claude Code](https://claude.com/claude-code): `CLAUDE.md` routes the
agent to one step contract at a time, and a person signs off at the end of every step.

## See it first

[projects/bistro/](projects/bistro/) is a worked example: a fictional restaurant, run through every
step. Restaurants are full of everyday words that mean something else everywhere else. A cover is
a guest counted, a ticket is the kitchen's copy of an order, the check is the bill, "86" means sold
out, and a server is a person, not a computer. The sample shows the method catching each clash
between the floor, the kitchen and the app, and settling it.

Try it in five minutes, from this folder:

```bash
tools/status.sh bistro                  # every step, and what to do next
python3 tools/check-glossary.py bistro  # the glossary against the entry rules
open projects/bistro/06-ontology/ontology.html   # macOS; elsewhere open the file in a browser
```

New here and want your own project? Open [quick-start-guide.html](quick-start-guide.html) in a
browser. It walks through creating a project and pulling its sources, one screen, no jargon.

## What you need

- bash, perl (for `tools/new-project.sh`) and Python 3.9 or later. The scripts use the Python
  standard library only. macOS and most Linux systems have all three.
- Claude Code, to run the steps. Steps 00 and 08 use its connectors for Google Drive and Linear,
  and the GitHub CLI (`gh`) for pull requests. A tool with no connector can be inventoried by
  hand: see [factory/steps/01-terms/prompts/](factory/steps/01-terms/prompts/).

## What is here

| Folder | What it holds |
|---|---|
| `quick-start-guide.html` | The visual getting-started guide. Open it in a browser. |
| `CLAUDE.md` | The router. Claude reads this first. Keep it short. |
| `factory/` | The method. `rules/` (one file per rule set) and `steps/` (one `CONTEXT.md` contract per step). Reference only, no project work. |
| `_templates/project/` | The blank project that `tools/new-project.sh` copies. Same depth as a project, so its links resolve before and after copying. |
| `projects/` | The work. One folder per product, or per major domain inside one, with the same step numbers as `factory/steps/`. `projects/bistro/` is the worked example. |
| `tools/` | Eight scripts and five pages: create a project, read its status, check a glossary, render the pictures, build a review package, stage a publish. See [tools/README.md](tools/README.md). |
| `DESIGN-NOTES.md` | Why the workspace looks like this. Add a note per new decision. |
| `LICENSE` | MIT. |

## Run a project, end to end

The steps below use `my-bistro`: the bistro example started again from an empty folder. Each step
names the file to compare against in the finished example, [projects/bistro/](projects/bistro/).
For your own product, swap in its name.

1. **Create the folder.** In a terminal, from this directory: `tools/new-project.sh my-bistro`. It
   copies the template and puts the name and date into `projects/my-bistro/project.yaml`. No
   terminal: make the folder `projects/my-bistro/` by hand, copy everything inside `_templates/project/` into it, and put
   the name and today's date into `project.yaml` yourself.
2. **Fill `project.yaml`.** The drive folder, the Linear workspace and team key, the git repo and
   PR cutoff, an existing glossary if there is one, and who may rule. Example: [project.yaml](projects/bistro/project.yaml).
3. **Step 00, pull sources.** The only step that reads from the network. Writes `00-sources/raw/` and
   `00-sources/manifest.md`. If a source is not reachable, the manifest says so and the step stops.
   The `code` source is git, not code: step 00 reads pull request titles and branch names, never the
   source files. Those names are a proxy for the words engineers use. Reading the code itself may
   come later; it is out of scope for this version. Example: [00-sources/manifest.md](projects/bistro/00-sources/manifest.md).
4. **Step 01, inventory each source.** One `01-terms/inventory-<source>.md` per source, every row
   with a verbatim quote. Read them and write `01-terms/review.md`: the terms you expected and do
   not see. Re-run step 01 with it. Nothing missing: still write the file, it is the gate. Example:
   [01-terms/](projects/bistro/01-terms/), where the review brought "turn" back from out of scope.
5. **Step 02, compare.** Writes `02-delta/delta-report.md`: the sources against each other and
   against the current glossary, and which suspect flags are confirmed. One inventory and no
   glossary: writes `skipped.md`. Example: [02-delta/delta-report.md](projects/bistro/02-delta/delta-report.md),
   where "server" turns out to mean a person on the floor and a computer in the app.
6. **Step 03, merge.** With two or more inventories, writes `03-merge/inventory-merged.md` and
   `conflicts.md`, with the flags step 02 decided. With one, writes `03-merge/skipped.md` saying
   why, and step 04 uses the single inventory. Example: [03-merge/conflicts.md](projects/bistro/03-merge/conflicts.md).
7. **Step 04, draft.** Replays every ruling in `decisions/`, then writes `04-draft/v1/glossary.md`,
   `conflict-report.md` and `verification-queue.md`. If a ruling would be contradicted, it writes
   `blocked-by-rulings.md` instead and stops. Example: [04-draft/v1/verification-queue.md](projects/bistro/04-draft/v1/verification-queue.md),
   four questions for the experts.
8. **Review.** The domain experts answer the verification queue. Each answer becomes one file in
   `decisions/`, in their own words. Then run step 04 again: it cuts `v2`. Example: [decisions/](projects/bistro/decisions/),
   four rulings, and [04-draft/v2/](projects/bistro/04-draft/v2/).
9. **Repeat 7 and 8** until the queue holds no core term.
10. **Step 05, publish.** Writes `05-glossary/glossary.md`, `core-terms.md`,
   `about-core-terms.md`, `taxonomy.md` and `backlog.md`. This is the deliverable. A published
   entry is the term, its definition and its keys; the evidence stays in the draft. Check every
   definition for precision before signing off. Example: [05-glossary/core-terms.md](projects/bistro/05-glossary/core-terms.md),
   twelve words to learn first.
11. **Step 06, render, on request.** `tools/render-ontology.py my-bistro` turns the glossary's own
    fields into `06-ontology/ontology.html`. Regenerate after any change to step 05. Example:
    [06-ontology/ontology.html](projects/bistro/06-ontology/ontology.html).
12. **Step 07, lenses, optional.** Write a value stream in `07-streams/<stream>.md`: money, data or
    results moving between terms the glossary defines. `tools/render-streams.py my-bistro` lays it over
    the step 06 picture, next to the workflow lens, as `07-streams/value-streams.html`. A named
    reviewer signs each stream file before it goes anywhere. Example: [07-streams/money.md](projects/bistro/07-streams/money.md)
    and [07-streams/order-to-table.md](projects/bistro/07-streams/order-to-table.md).
13. **Step 08, send it out.** Once the glossary is at `trial`, `tools/stage-publish.py my-bistro` stages
    the files in `08-publish/outbox/` and logs one row per destination named in `project.yaml`.
    Claude sends the outbox to the shared drive and the code repository, then marks each row sent.
    People read those copies, never the project folders. Example:
    [08-publish/publish-log.md](projects/bistro/08-publish/publish-log.md).

Later: when the sources move on, run step 02 in drift mode. It reads the current glossary and the
raw pulls and writes only `02-delta/drift-report.md`.

A tool the pipeline cannot reach (no connector allowed): copy the prompt for its type from
`factory/steps/01-terms/prompts/`, run it inside the tool, and paste the table into
`01-terms/inventory-<source>.md`. The rest of the pipeline treats it like any other inventory.

## Resume, or re-run one step

`tools/status.sh my-bistro` prints which step files exist and what to do next. Every step reads files
written by earlier steps and nothing else, so re-running step 03 costs a minute, not another crawl.
Edit any step output by hand between steps; they are plain markdown.

## Rules worth knowing

- **Status is the filesystem.** A step is done when its output file exists. There is no tracker.
- **Rulings are inputs.** They live in `decisions/`, one file each, and step 04 replays all of them.
- **Only steps 00 and 08 touch the network.** Step 00 reads from it, step 08 sends to it. Every
  other step reads files.
- **Code is a proxy.** The pipeline reads pull request titles and branch names from git, not the
  source. It needs the names engineers give their work, not the work itself.
- **The glossary wins.** The ontology is a view of the glossary. If they disagree, fix the glossary.
- **Nothing is deleted.** Superseded files move to an `_archive/` folder.

Details for any step: open its `CONTEXT.md`. Start at [CLAUDE.md](CLAUDE.md).
