# Step 01: Terms

Turn each source into an inventory of the terms it uses, one inventory per source. This step
reads files and writes files. It never touches the network, it never reads anything written by
steps 02 to 06, and it never reads a glossary.

This step records what people wrote. It does not compare sources, and it does not choose between
names. Comparing is step 02's job. Choosing is step 04's job.

## Precondition

`projects/<p>/00-sources/manifest.md` exists and lists at least one source that is either pulled
(items in `raw/<source>/`) or inventoried externally. One source is enough; a single early
document with a glossary inside it is a valid run.

## Inputs

- `projects/<p>/00-sources/manifest.md`: which sources exist, and which are external.
- `projects/<p>/00-sources/raw/<source>/*`: the pulls. For a pulled source, nothing else is
  evidence.
- `projects/<p>/project.yaml`: `disciplines:` for the discipline column, `audiences:` for the
  scope test, `seed_terms:`, each source's `cutoff`, and `type:` for an external source.
- `projects/<p>/01-terms/review.md`, when it exists: the reviewer's list of expected terms.
- [prompts/](prompts/README.md): one prompt per source type. The same text a human runs inside a
  tool the pipeline cannot reach.
- [../../rules/evidence.md](../../rules/evidence.md): the row, the bands, the flags.

## Process

Done by Claude, or by a human inside an external tool. Two passes.

### Full pass (default)

1. **Pick the prompt per source.**

   | Source | Prompt |
   |---|---|
   | `drive`, `linear-docs`, any document store | [prompts/document-store.md](prompts/document-store.md) |
   | `linear-issues`, any issue tracker | [prompts/issue-tracker.md](prompts/issue-tracker.md) |
   | `code` | [prompts/code-repository.md](prompts/code-repository.md) |
   | a source with `external: true` in `project.yaml` | the file its `type:` names |

2. **Fill the placeholders** from `project.yaml` and the manifest: `<project>`, `<scope>`,
   `<cutoff date>`, `<seed terms>` (from `seed_terms:`, else empty), `<row target>` (40 to 80
   unless the source is tiny), `<disciplines>`, `<audiences>`.
3. **Apply the prompt to `raw/<source>/`.** Read every item. The prompt is the whole instruction.
   One thing differs when Claude runs it: the link in "example quote + link" is the item's own
   link from the manifest, or the `raw/` path when the item has none.
4. **Write the inventory.** One file per source: the front matter below, the nine-column table,
   then a `## Seen, not quoted` section, then an `## Out of scope` section.
5. **External sources.** Do not write an inventory for them. The manifest says which prompt the
   human ran and where the paste is. Check the pasted file has the front matter, the nine columns,
   a `## Seen, not quoted` section and an `## Out of scope` section. A row without a quote moves
   under the first. Say what was checked in the run summary.

### Review pass

Invoked as "re-run step 01 with the review". Runs when `01-terms/review.md` holds a row with
status `missing`.

1. For each `missing` row, re-read `raw/<source>/` for that term and its obvious variants.
2. Already under `## Out of scope` in that inventory: the lead has overruled the audience test for
   it. Move it into the table with the quote it already carries, update `rows:`, set the review
   row to `found`. No new search is needed.
3. Quote found: add the row to `inventory-<source>.md`, update `rows:`, set the review row to
   `found`.
4. No quote: list the term under `## Seen, not quoted` in that inventory, with where it was
   looked for. Set the review row to `not quoted`.
5. External source: Claude cannot look. Leave the row `missing` and write in its note: "external:
   re-run `prompts/<type>.md` with this term under seed terms". The human resolves the row after
   pasting.

Rules:

- No quote, no row. A row without a quote is never deleted. It moves under `## Seen, not quoted`
  at the bottom of the same inventory.
- The audience test decides scope, and `audiences:` in `project.yaml` names the groups. A term
  stays in the table when two or more of them need to share its meaning. A term only one of them
  uses is that group's own extension, and it moves under `## Out of scope` with its quote. Never
  deleted. The two sections answer different questions: `## Seen, not quoted` means no evidence,
  `## Out of scope` means evidence but only one audience. A term never goes in both.
- Frequency is a band, never a count.
- Never merge two senses. Never resolve a synonym. Never map a code name to a product name. Those
  are step 02's comparisons.
- The prompt text is the single source of truth for the row shape. Do not restate its rules here
  or in an inventory header.
- This step reads nothing from `02-delta/` onwards, and no glossary, published or otherwise.

## Outputs

In `projects/<p>/01-terms/`:

| File | Required | What it is |
|---|---|---|
| `inventory-<source>.md` | one per source | The term table, then `## Seen, not quoted`, then `## Out of scope`. Front matter below. |
| `review.md` | yes, before step 02 | The lead writes it: the terms expected and not seen, with a status each, and `reviewed:` filled with the date. Scaffold: `_review.template.md`. |

Front matter of an inventory:

```yaml
---
project: <name>
step: 01-terms
source: <source>
produced_by: claude          # or: external
tool: <name>                 # external only: the tool the prompt ran in
prompt: <type>.md            # which file in factory/steps/01-terms/prompts/
run: <YYYY-MM-DD>            # external: the date the table was pasted
rows: <n>
---
```

Source names: `drive`, `linear-docs`, `linear-issues`, `code`, or the key of an external source
in `project.yaml`. The file name is the source name; steps 02 and 03 count these files.

## Human checkpoint

The lead reads each inventory once and asks two questions.

1. Which terms did I expect to see here and do not? Each one goes into `01-terms/review.md` as a
   row: source, expected term, status `missing`.
2. Is anything under `## Out of scope` in the wrong place? The audience test is a judgement, and
   the lead overrules it. Bringing a term back is a row in `review.md` too, status `missing`. Its
   quote is already recorded, so the re-run only moves it.

Then this step is re-run with the review.

The lead does not remove rows. A term that looks too obvious to keep is exactly the one whose shared
understanding step 02 must check. Removing it hides the assumption, and unchecked assumptions
are where meanings drift apart.

When nothing is missing, `review.md` is still written, with the table empty and the line "Nothing
expected is missing."

The last act of the checkpoint is to sign it: fill `reviewed:` with today's date and `reviewer:`
with a name. That signature is what lets step 02 run. An unsigned `review.md` with an empty table
and a signed one with an empty table look the same on disk, and they are not the same thing.

## Status signal

Step 01 is done when at least one `projects/<p>/01-terms/inventory-*.md` exists,
`01-terms/review.md` exists with `reviewed:` set to a date, and no review row has status
`missing`.

## Next

[../02-delta/CONTEXT.md](../02-delta/CONTEXT.md), always. It runs, or it writes its own
`skipped.md`.
