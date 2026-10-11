# <Project name>

Copy of [_templates/project/](../../_templates/project/). Rename this heading to
the project's name and fill in the lines below. Everything project-specific goes in
[project.yaml](project.yaml) and nowhere else.

- Project: `<name>`
- Started: `<YYYY-MM-DD>`
- Current draft: `v<n>`
- Rulings: `<n>`

## Where things stand

Status is the filesystem. A step is done when its file exists. `tools/status.sh <name>` prints it.

| Step | Done when this exists | Contract |
|---|---|---|
| 00 Sources | `00-sources/manifest.md` | [../../factory/steps/00-sources/CONTEXT.md](../../factory/steps/00-sources/CONTEXT.md) |
| 01 Terms | `01-terms/inventory-*.md` and `review.md` | [../../factory/steps/01-terms/CONTEXT.md](../../factory/steps/01-terms/CONTEXT.md) |
| 02 Delta | `02-delta/delta-report.md`, or `skipped.md` | [../../factory/steps/02-delta/CONTEXT.md](../../factory/steps/02-delta/CONTEXT.md) |
| 03 Merge | `03-merge/inventory-merged.md`, or `skipped.md` | [../../factory/steps/03-merge/CONTEXT.md](../../factory/steps/03-merge/CONTEXT.md) |
| 04 Draft | `04-draft/v<n>/glossary.md` | [../../factory/steps/04-draft/CONTEXT.md](../../factory/steps/04-draft/CONTEXT.md) |
| 05 Glossary | `05-glossary/glossary.md` | [../../factory/steps/05-glossary/CONTEXT.md](../../factory/steps/05-glossary/CONTEXT.md) |
| 06 Ontology | `06-ontology/ontology.html`, or `skipped.md` | [../../factory/steps/06-ontology/CONTEXT.md](../../factory/steps/06-ontology/CONTEXT.md) |
| 07 Streams | `07-streams/value-streams.html` and a signed stream file, or `skipped.md`. Optional | [../../factory/steps/07-streams/CONTEXT.md](../../factory/steps/07-streams/CONTEXT.md) |
| 08 Publish | `08-publish/publish-log.md` with a `sent` date for every destination | [../../factory/steps/08-publish/CONTEXT.md](../../factory/steps/08-publish/CONTEXT.md) |
| decisions | one `NNN-<slug>.md` per ruling | [../../factory/steps/decisions/CONTEXT.md](../../factory/steps/decisions/CONTEXT.md) |

Files starting with `_` and ending in `.template.md` are blank scaffolds. Copy one, drop the
underscore and the `.template` part, and fill it in. A scaffold sitting untouched means the step
has not started.

Superseded files are never deleted. Move them to `_archive/` in this folder, named with the
version they came from: `glossary-v3.md`.

## Notes

Anything about this project that does not belong in a step file. Who to ask, what to avoid,
scheduling.
