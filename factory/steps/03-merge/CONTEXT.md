# Step 03: Merge

Fold the per-source inventories into one table, one row per term per sense, and list every row
that carries a flag. This step exists so step 04 reads one table, not four.

This step lines rows up and applies the flag decisions step 02 made. It does not decide which
name wins. That is step 04's job, with the rulings in view.

## Precondition

Two or more `projects/<p>/01-terms/inventory-*.md` exist, and `projects/<p>/02-delta/delta-report.md`
exists.

With exactly one inventory, this step does not run. It writes `03-merge/skipped.md` saying so,
naming the one inventory, and step 04 reads that inventory directly. The skip file is the audit
trail: it shows the step was considered, not forgotten. Re-running step 03 after a second
inventory appears replaces `skipped.md` with the real outputs.

## Inputs

- `projects/<p>/01-terms/inventory-*.md`: all of them. An external inventory is treated like any
  other.
- `projects/<p>/02-delta/delta-report.md`: sections "Same word, different meaning" and "Different
  words, same meaning", for the `flag after delta` column.
- [../../rules/evidence.md](../../rules/evidence.md): the row and the bands.
- [../../rules/classification.md](../../rules/classification.md): the flags.

## Process

Done by Claude.

1. **Line up the rows.** Rows from different inventories merge when the term matches (case and
   plural ignored) or when one lists the other's term under "variants seen". The surviving term is
   the one used in the most authoritative source, per the order in
   [../../rules/classification.md](../../rules/classification.md). The other terms move to
   "variants seen".
2. **Keep senses apart.** A row whose inferred meaning differs from the others under the same
   term keeps its own row. Never merge a row flagged `homonym` or `homonym-suspect`.
3. **Normalise.** The highest frequency band across sources wins. `source type` lists every source
   that had the term. `discipline or team` lists every discipline that used it.
4. **Apply the flag decisions.** Set each row's flag to the `flag after delta` value in
   `02-delta/delta-report.md`. A row the report does not mention keeps its inventory flag. Do not
   re-derive a flag here; a disagreement the report missed goes back to step 02.
5. **Write the conflict list.** Every row with a flag, grouped by flag, with the sources on each
   side and the quotes that show the disagreement. This is the reviewer's reading list, and the
   file step 04 reads for conflicts.

Rules:

- The merged table keeps the nine columns of the inventory row. No new columns.
- Every merged row still carries one verbatim quote with title and link. Pick the clearest one and
  keep the others' titles under the quote.
- Do not resolve anything. A conflict list that has already picked winners has hidden the evidence.
- The merged table is derived. A wrong flag is fixed in `02-delta/delta-report.md`, then this
  step is re-run. Never by hand in the merged table.

## Outputs

In `projects/<p>/03-merge/`:

| File | Required | What it is |
|---|---|---|
| `inventory-merged.md` | yes, when the step runs | One table. Header: the inventories merged, the run date, the row count, the flag definitions. |
| `conflicts.md` | yes, when the step runs | Every flagged row, grouped by flag, with the evidence on each side. |
| `skipped.md` | yes, when the step does not run | `reason:`, the date, and the name of the single inventory step 04 should read. |

## Human checkpoint

The lead reads `conflicts.md` once. Any `homonym` row that looks like a synonym, or the reverse, is
fixed in `02-delta/delta-report.md` and this step is re-run before step 04. A wrong flag here
becomes a wrong entry, and a wrong entry becomes a question the expert has to unpick.

## Status signal

Step 03 is done when `projects/<p>/03-merge/inventory-merged.md` exists, or when
`projects/<p>/03-merge/skipped.md` exists. Neither: not run yet.

## Next

[../04-draft/CONTEXT.md](../04-draft/CONTEXT.md)
