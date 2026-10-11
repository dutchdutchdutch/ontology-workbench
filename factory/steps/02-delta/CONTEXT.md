# Step 02: Delta

Compare the inventories with each other and with the current glossary, and decide which suspect
flags are confirmed. This step finds disagreements. It does not fold tables; that is step 03. It
does not choose names; that is step 04. It also hosts drift mode, the scheduled check that runs
after a glossary is published.

The point: a term everyone assumes is understood is the one nobody checks. This step checks it.

## Precondition

`projects/<p>/01-terms/review.md` exists and holds no row with status `missing`. That is the gate:
what goes into this comparison has been looked at by a person.

Then one of:

- Two or more `01-terms/inventory-*.md` exist: run.
- One inventory, and `sources.glossary.path` is set in `project.yaml`: run. The cross-source
  sections are one line each.
- One inventory and no glossary: write `02-delta/skipped.md` with
  `reason: one inventory, no glossary`, the date, and the inventory name. Step 03 will also skip
  and step 04 reads the inventory directly. A second inventory later: re-run this step; it
  replaces `skipped.md`.

## Inputs

- `projects/<p>/01-terms/inventory-*.md`: all of them. An external inventory is treated like any
  other.
- `projects/<p>/01-terms/review.md`: recorded in the report header; its `not quoted` rows feed
  section 3.
- `projects/<p>/project.yaml`: `sources.glossary.path`, `authority_order`.
- The current glossary, when the path is set. Usually `projects/<p>/05-glossary/glossary.md`
  once one has been published.
- [../../rules/evidence.md](../../rules/evidence.md) and
  [../../rules/classification.md](../../rules/classification.md): the flags, and when a suspect
  flag is confirmed.
- [../../rules/prose-style.md](../../rules/prose-style.md): for the report.

## Process

Done by Claude. Two modes.

### Full mode (default)

Seven sections, always all present. An absent section cannot be told from a forgotten one.

1. **Same word, different meaning.** Across inventories, rows with the same term (case and plural
   ignored) whose inferred meanings cannot both be true of one thing. Table: term | source A
   meaning and quote | source B meaning and quote | flag in inventory | flag after delta.
   `homonym-suspect` becomes `homonym` when a second source shows the second sense. `overloaded`
   when the meanings overlap but differ in scope or precision. Otherwise the flag stays suspect.
2. **Different words, same meaning.** Across inventories, rows with different terms and the same
   inferred meaning, or where one lists the other under "variants seen". Same table shape.
   `synonym-suspect` becomes `synonym` when a second source uses both names for one thing. A
   customer-facing name against an internal one is noted as such, not resolved.
3. **Present in one source only.** Terms with a row in one inventory and none elsewhere. Table:
   term | source | discipline | note. A term the reviewer expected elsewhere, from `review.md`,
   is marked.
   Also `different relation`: one pair of terms, linked by both sources with different verbs, or
   linked by one and not the other. Read the verbs out of the quotes. Table: term A | term B |
   source A verb | source B verb | note. Step 04 needs this; `relations:` is written there.
4. **New terms.** Against the glossary, per source: inventory terms with no entry.
5. **Moved meaning.** Glossary entries whose definition no longer matches how a source now uses
   the word. Quote on each side.
6. **Code drift.** Names in the code inventory against the other inventories and the glossary.
   Mismatch types: `different name`, `abbreviation`, `plural-singular`, `missing from inventory`,
   `missing from glossary`.
7. **Unused glossary terms.** Entries no inventory uses.

When there is no glossary, sections 4 to 7 each say so in one line. When there is one inventory,
sections 1 to 3 each say so in one line.

### Drift mode

Invoked as "run step 02 in drift mode". For a scheduled check after the glossary is published.

- Inputs: `00-sources/raw/` and the current glossary only. Needs no `01-terms/` file and no
  `review.md`.
- Process: sections 4 to 7 only, read straight from `raw/`. No inventories are written. A source
  the manifest lists as inventoried externally is listed as "not checked: inventoried externally,
  re-run its prompt to refresh".
- Output: `02-delta/drift-report.md` and nothing else. A one-line verdict at the top: "no drift",
  or "drift in N terms", naming them.

Rules:

- The `flag after delta` column is the only place a flag changes. Step 03 copies it; it does not
  decide. A disagreement this report missed is fixed here, and step 03 is re-run.
- Do not resolve anything. No canonical name, no winner between a customer-facing name and an
  internal one.
- Every row in sections 1, 2, 5 and 6 carries the quote from each side. A decision without both
  quotes is a guess.
- This step reads nothing from `03-merge/`, `04-draft/`, `05-glossary/` or `06-ontology/`, except
  the published glossary named in `project.yaml`. Keep it that way; drift mode may be scheduled
  to run on its own elsewhere.

## Outputs

In `projects/<p>/02-delta/`:

| File | Required | What it is |
|---|---|---|
| `delta-report.md` | yes, full mode | Seven sections, always all present. Header: the inventories compared, the glossary compared against (or `none`), the review date, the run date. |
| `skipped.md` | when one inventory and no glossary | `reason:`, the date, the inventory name. |
| `drift-report.md` | drift mode only | Sections 4 to 7 plus a verdict line. |

Front matter of the report:

```yaml
---
project: <name>
step: 02-delta
run: <YYYY-MM-DD>
inventories: [drive, linear-docs, linear-issues, code]
against: none                 # or 05-glossary/glossary.md
review: 01-terms/review.md    # reviewed <YYYY-MM-DD>, <n> expected terms listed
---
```

## Human checkpoint

The lead reads sections 1 and 2 in full, and section 5 when a glossary exists. Any `flag after
delta` that looks wrong is changed here, in the cell, before step 03 runs. A wrong flag becomes a
wrong merged row, then a wrong entry, then a question an expert has to unpick.

## Status signal

Step 02 is done when `projects/<p>/02-delta/delta-report.md` exists, or when
`projects/<p>/02-delta/skipped.md` exists. Drift mode is done when `drift-report.md` exists; it
does not change the step's state.

## Next

[../03-merge/CONTEXT.md](../03-merge/CONTEXT.md)
