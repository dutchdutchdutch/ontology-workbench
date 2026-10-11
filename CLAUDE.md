# One-Vocabulary

Source-of-truth glossaries for product teams. One person, the lead, runs the workspace and signs
every checkpoint; domain experts rule on meaning. Nine steps: pull sources, inventory
each one, compare, merge, draft and review, publish the glossary and taxonomy, render the ontology,
lay value-stream and workflow lenses over it, and send it all to where people work.
This file routes only. The method lives in the step contracts. Open the one you need.

## Pipeline

`factory/steps/` holds the method. `projects/<name>/` holds the work, using the same numbers.
Each step has a `CONTEXT.md` with inputs, process, outputs, precondition and the human checkpoint.

| # | Step | Contract | Runs when | Output |
|---|---|---|---|---|
| 00 | Sources | [factory/steps/00-sources/CONTEXT.md](factory/steps/00-sources/CONTEXT.md) | always. The only step that touches the network | `00-sources/manifest.md`, `raw/` |
| 01 | Terms | [factory/steps/01-terms/CONTEXT.md](factory/steps/01-terms/CONTEXT.md) | at least one source in the manifest | `01-terms/inventory-<source>.md`, `review.md` |
| 02 | Delta | [factory/steps/02-delta/CONTEXT.md](factory/steps/02-delta/CONTEXT.md) | `review.md` exists with nothing missing. Compares when there is more than one inventory, or a glossary | `02-delta/delta-report.md` or `skipped.md`; `drift-report.md` in drift mode |
| 03 | Merge | [factory/steps/03-merge/CONTEXT.md](factory/steps/03-merge/CONTEXT.md) | more than one inventory exists | `03-merge/inventory-merged.md`, `conflicts.md` |
| 04 | Draft | [factory/steps/04-draft/CONTEXT.md](factory/steps/04-draft/CONTEXT.md) | always. Runs many times | `04-draft/vN/glossary.md`, `conflict-report.md`, `verification-queue.md`, `coverage.md` |
| 05 | Glossary | [factory/steps/05-glossary/CONTEXT.md](factory/steps/05-glossary/CONTEXT.md) | a draft at v2 or higher exists | `05-glossary/glossary.md`, `core-terms.md`, `about-core-terms.md`, `taxonomy.md`, `backlog.md`; `feedback.md` from `trial` on |
| 06 | Ontology | [factory/steps/06-ontology/CONTEXT.md](factory/steps/06-ontology/CONTEXT.md) | on request, once 05 exists | `06-ontology/ontology.html`, `ontology-machine.json` |
| 07 | Streams | [factory/steps/07-streams/CONTEXT.md](factory/steps/07-streams/CONTEXT.md) | optional, on request. Lenses once 06 exists; a process once 05 exists | `07-streams/<stream>.md`, `value-streams.html`; `<process>.md`, `processes.html` |
| 08 | Publish | [factory/steps/08-publish/CONTEXT.md](factory/steps/08-publish/CONTEXT.md) | 05 at `trial` or `adopted`, and a `publish:` block. The second network step | `08-publish/outbox/`, `publish-log.md` |

Rulings are inputs, never outputs: [factory/steps/decisions/CONTEXT.md](factory/steps/decisions/CONTEXT.md).
Step 04 replays every file in `projects/<p>/decisions/` before it writes a draft.
Every step ends with a human checkpoint. Never run the next step before it.

## Where projects live

[projects/](projects/): one folder per project. Start one with `tools/new-project.sh <name>`, which
copies [_templates/project/](_templates/project/), or copy that folder by hand. See [projects/README.md](projects/README.md).

## How to tell status

Status is the filesystem. No tracker, no status field. `tools/status.sh <p>` prints this table.

| This file exists | Then |
|---|---|
| `projects/<p>/00-sources/manifest.md` | sources pulled, or inventoried externally. Run 01 |
| `projects/<p>/01-terms/inventory-*.md` | one per source. Read them, write `review.md` |
| `projects/<p>/01-terms/review.md` | the step 01 checkpoint. Signed (`reviewed:` holds a date) with no `missing` row: run 02. A `missing` row: re-run 01 with the review. Unsigned: nobody has read the inventories yet |
| `projects/<p>/02-delta/delta-report.md` | compared, flags decided. Run 03 |
| `projects/<p>/02-delta/skipped.md` | 02 considered and skipped: one inventory, no glossary. Run 03 |
| `projects/<p>/02-delta/drift-report.md` | a drift check ran. Read it; it changes nothing else |
| `projects/<p>/03-merge/inventory-merged.md` | merged, run 04 |
| `projects/<p>/03-merge/skipped.md` | 03 considered and skipped, reason inside. Run 04 |
| `projects/<p>/04-draft/vN/glossary.md` | draft N exists. v1 = unreviewed. v2+ = at least one ruling applied |
| `projects/<p>/04-draft/vN/blocked-by-rulings.md` | draft N stopped: it would contradict a ruling. Resolve in `decisions/` |
| `projects/<p>/05-glossary/glossary.md` with `stage: review` | published. Reviewers sign off, the lead runs the swap test, then set `stage: trial` |
| `projects/<p>/05-glossary/glossary.md` with `stage: trial` | in use. Collect `feedback.md`; when no row is open, set `stage: adopted` |
| `projects/<p>/05-glossary/glossary.md` with `stage: adopted` | the team's vocabulary. Run 06 on request, 02 in drift mode on a schedule |
| `projects/<p>/06-ontology/ontology.html` | rendered. Regenerate after any 05 change |
| `projects/<p>/07-streams/<stream>.md` | a value stream drafted. A hypothesis until its `reviewed:` holds a date |
| `projects/<p>/07-streams/value-streams.html` | lenses rendered. Regenerate after any 05, 06 or stream-file change |
| `projects/<p>/07-streams/<process>.md` | a process drafted (front matter has `process:`). Same `reviewed:` rule |
| `projects/<p>/07-streams/processes.html` | processes rendered. Regenerate after any 05 or process-file change |
| `projects/<p>/08-publish/publish-log.md` | a row with an empty `sent` is staged, not out: send it, then `--sent`. A `from` older than the glossary means the copies out there are behind |

A `skipped.md` means the step was considered and passed through. `_*.template.md` files are unfilled scaffolds. Neither is work.

## Reference

- [quick-start-guide.html](quick-start-guide.html): the visual guide for a newcomer's first project. Update it when step 00 or `new-project.sh` changes.
- [DESIGN-NOTES.md](DESIGN-NOTES.md): why the workspace looks like this; add a note per new decision.
- [projects/bistro/](projects/bistro/): a fictional restaurant run through every step. Read it before starting a project.
- [factory/rules/](factory/rules/): the method, one file per rule set. Read [factory/rules/evidence.md](factory/rules/evidence.md) before writing any inventory row. Index: [factory/README.md](factory/README.md).
- [factory/steps/01-terms/prompts/README.md](factory/steps/01-terms/prompts/README.md): a tool with no connector. Copy the prompt for its type, run it inside the tool, paste the table back.
- [tools/](tools/): eight scripts and five renderer pages. What each does: [tools/README.md](tools/README.md).

## House rules

- Never edit a `factory/` file to fit one project, and never put project content in it. No project value lives outside `projects/<p>/project.yaml`.
- Only steps 00 and 08 touch the network: 00 brings words in, 08 sends the vocabulary out. Every
  other step reads files. No script touches the network; Claude does, through the connected servers.
- Nobody outside the workspace reads 05, 06 or 07 directly. They read the copies step 08 sends.
- The `code` source is git, not code: pull request titles and branch names, never source files. A proxy for the words engineers use.
- The glossary is the product. The ontology is a view of it. If they disagree, the glossary wins.
- One commit per step, step named in the message. No dates and no `-final` in filenames.
