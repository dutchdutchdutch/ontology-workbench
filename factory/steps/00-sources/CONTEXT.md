# Step 00: Sources

Pull every source the project names, once, into files. This is the only step in the pipeline that
reads from the network; step 08, at the end, only sends. Everything after it reads what this step wrote, which is what makes every
later step cheap to re-run.

This step copies. It does not read for meaning. Reading for meaning is step 01's job.

## Precondition

`projects/<p>/project.yaml` names at least one source under `sources:`. Nothing else is needed.
A source marked `external: true` counts. This step always runs when asked; re-running it replaces
`raw/` and rewrites the manifest.

## Inputs

- `projects/<p>/project.yaml`: the `sources:` block. Drive folder id, Linear workspace and team
  key, code repository and PR cutoff, path to an existing glossary. For an external source:
  `external: true`, `type`, `tool`, `link`.
- The Linear MCP server and the Google Drive MCP server, when connected.
- `gh` for pull requests and branch names, when the code source is set.

## Process

Done by Claude, using the connected servers. For each source in `project.yaml`:

1. **Skip external sources.** A source with `external: true` is not pulled. Write it into
   `manifest.md` under "Inventoried externally" with the tool, the link, and the prompt file
   `factory/steps/01-terms/prompts/<type>.md`. A human runs that prompt inside the tool and
   pastes the result into `01-terms/inventory-<name>.md`; the how is in
   [../01-terms/prompts/README.md](../01-terms/prompts/README.md).
2. **Check the server is connected.** If it is not, do not guess at content. Write the source into
   `manifest.md` under "Not pulled" with what is needed to pull it (which server, which id), and
   continue with the next source. Stop at the end and say which sources are missing.
3. **Pull.** Drive: every document, slide deck, sheet and wireframe under the folder id, modified
   since the cutoff, as text. Linear docs: every document in the workspace. Linear issues: title,
   description and linked PR titles and branch names for every issue in the team since the
   cutoff. Code: PR titles and branch names since `pr_cutoff`, nothing else. An existing glossary:
   the file as is.
4. **Write raw.** One folder per source under `raw/`: `raw/drive/`, `raw/linear-docs/`,
   `raw/linear-issues/`, `raw/code/`, `raw/glossary/`. One file per item, named by the item's own
   id or slug, with a first line giving title, link and pulled date. No summarising, no cleaning.
5. **Write the manifest.** One row per item: source, title, link, pulled date. A count per source
   at the top. Three sections: "Items", "Inventoried externally", "Not pulled". The last two say
   in one line when they are empty.

Rules:

- Never write content you did not pull. An empty `raw/` folder with a "Not pulled" row is
  correct. A plausible reconstruction is not.
- Keep the item's own title and link. Every inventory row will cite them.
- Do not filter. Deciding what matters is step 01's job; a pull that filters hides evidence.
- An external source has no `raw/` folder. Its evidence is the quote and link on each pasted row.
- The `code` source is git, not code. Pull the names engineers give their work: pull request
  titles and branch names. Never pull source files, diffs or file trees. The names are a proxy
  for the code's vocabulary. Reading the code itself is out of scope for this version.

## Outputs

In `projects/<p>/00-sources/`:

| File | Required | What it is |
|---|---|---|
| `manifest.md` | yes | What was pulled, from where, when. Counts per source. "Inventoried externally" and "Not pulled" sections. |
| `raw/<source>/*` | yes, per pulled source | The pulls, one file per item, unchanged. |

## Human checkpoint

The lead reads the manifest's counts and the "Not pulled" section. A source with a count that looks
low (three drive documents from a company with a year of history) is a permissions problem, not a
small company. Fix access, re-run, then go on. Ten minutes here saves an inventory built on a
third of the evidence. An "Inventoried externally" row is not a problem; a "Not pulled" row is.

## Status signal

Step 00 is done when `projects/<p>/00-sources/manifest.md` exists and its "Not pulled" section is
empty or accepted by the lead.

## Next

[../01-terms/CONTEXT.md](../01-terms/CONTEXT.md)
