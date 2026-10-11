---
project: <name>
pulled: <YYYY-MM-DD>
sources_pulled: [<drive, linear-docs, linear-issues, code, glossary>]
sources_external: [<key of each external source, or empty>]
---

# Manifest: <project>

| Source | Items | Folder |
|---|---|---|
| drive | `<n>` | `raw/drive/` |
| linear-docs | `<n>` | `raw/linear-docs/` |
| linear-issues | `<n>` | `raw/linear-issues/` |
| code | `<n>` PRs since `<YYYY-MM-DD>` | `raw/code/` |
| glossary | `<0 or 1>` | `raw/glossary/` |

## Items

| Source | Title | Link | Pulled |
|---|---|---|---|
| `<source>` | `<title>` | `<url>` | `<YYYY-MM-DD>` |

## Inventoried externally

One row per source the pipeline cannot reach. A human runs the prompt inside the tool and pastes
the table into `../01-terms/inventory-<source>.md`. Empty means every source was pulled.

| Source | Tool | Prompt | Inventory | Pasted |
|---|---|---|---|---|
| `<source>` | `<tool>` | `factory/steps/01-terms/prompts/<type>.md` | `../01-terms/inventory-<source>.md` | `<YYYY-MM-DD>` |

## Not pulled

One row per source that could not be reached, with what is needed to pull it. Empty means
everything in `project.yaml` was pulled.

| Source | Why not | What is needed |
|---|---|---|
