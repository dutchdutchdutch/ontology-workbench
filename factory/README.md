# factory: the method

Everything here is stable across projects. Nothing here is project-specific and nothing here
changes during a run. Project work lives in [../projects/](../projects/).

## Rules

One file per rule set. Step contracts link to these; they never restate them.

| File | What it is | Who reads it |
|---|---|---|
| [rules/evidence.md](rules/evidence.md) | No quote, no row. The inventory row, frequency bands, homonyms, synonyms, gaps, external inventories. | Steps 00 to 03, and anyone running a prompt. Read first. |
| [rules/classification.md](rules/classification.md) | Rows to concepts, the five classes, suspect and confirmed, the canonical-name rule. | Steps 02, 03 and 04. |
| [rules/entry-format.md](rules/entry-format.md) | The glossary entry in two shapes: the draft's, with its evidence, and the published one, which is the term, the definition and the keys. The twelve types and their tests, the is-a test, building version over version. Plus wikilinks and the cap. | Steps 04 and 05, and the render script. |
| [rules/relation-kinds.md](rules/relation-kinds.md) | The 21 relation kinds, their inverses and flows, one object per line, the mirror rule, and how a project adds its own. | Steps 04 to 06, and every script that reads relations. |
| [rules/core-selection.md](rules/core-selection.md) | Core by dependency. What the core is for, how it grows round over round, the category order both published files share, dependency order, the backlog stages. | Step 05. |
| [rules/prose-style.md](rules/prose-style.md) | Conclusions first, no em dashes, plain words, tables. | Anyone writing for a reader. |

Read order for someone new: `evidence.md`, then the contract for the step they are working on.

## Steps

One contract per step, same numbers as the project folders. Each has a purpose, a precondition
read from the filesystem, inputs, process, outputs, the human checkpoint, the status signal, and
where to go next.

| Step | Contract |
|---|---|
| 00 Sources | [steps/00-sources/CONTEXT.md](steps/00-sources/CONTEXT.md) |
| 01 Terms | [steps/01-terms/CONTEXT.md](steps/01-terms/CONTEXT.md) |
| 02 Delta | [steps/02-delta/CONTEXT.md](steps/02-delta/CONTEXT.md) |
| 03 Merge | [steps/03-merge/CONTEXT.md](steps/03-merge/CONTEXT.md) |
| 04 Draft | [steps/04-draft/CONTEXT.md](steps/04-draft/CONTEXT.md) |
| 05 Glossary | [steps/05-glossary/CONTEXT.md](steps/05-glossary/CONTEXT.md) |
| 06 Ontology | [steps/06-ontology/CONTEXT.md](steps/06-ontology/CONTEXT.md) |
| 07 Streams | [steps/07-streams/CONTEXT.md](steps/07-streams/CONTEXT.md) |
| 08 Publish | [steps/08-publish/CONTEXT.md](steps/08-publish/CONTEXT.md) |
| decisions | [steps/decisions/CONTEXT.md](steps/decisions/CONTEXT.md) |

## Prompts

[steps/01-terms/prompts/](steps/01-terms/prompts/README.md) holds one prompt per source type:
issue tracker, document store, code repository. Step 01 applies the matching one to `raw/`. When
a tool has no connector, a human copies the same file, runs it inside the tool, and pastes the
table back as an inventory. The README there says how.

## Template

[../_templates/project/](../_templates/project/) is the blank project. `tools/new-project.sh <name>`
copies it to `projects/<name>/`. Its README files link back here and restate nothing.

Back to [../CLAUDE.md](../CLAUDE.md).
