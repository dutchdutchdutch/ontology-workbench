# 00 Sources: bistro

What goes here: the raw pulls and the record of what was pulled. The only folder in the project
that step 00 writes, and the only step that reads from the network.

| File | Required | How it gets here |
|---|---|---|
| `manifest.md` | yes | Step 00 writes it. Scaffold: `_manifest.template.md`. |
| `raw/<source>/*` | per source | Step 00 writes one folder per source, one file per item, unchanged. |

Sources are named `drive`, `linear-docs`, `linear-issues`, `code`, `glossary`, or the key of an
external source. Which ones exist comes from [../project.yaml](../project.yaml). A source with
`external: true` has no `raw/` folder; the manifest lists it under "Inventoried externally" and a
human pastes its inventory into `../01-terms/`.

`raw/code/` holds pull request titles and branch names from git, one file per PR. Never source
files. The names engineers give their work stand in for the code's vocabulary.

Contract: [../../../factory/steps/00-sources/CONTEXT.md](../../../factory/steps/00-sources/CONTEXT.md)
