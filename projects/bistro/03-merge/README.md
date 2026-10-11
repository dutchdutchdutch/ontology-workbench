# 03 Merge: bistro

What goes here: the one table step 04 reads, and the list of rows that carry a conflict. Or, on a
single-source project, the record that this step was skipped.

| File | Required | How it gets here |
|---|---|---|
| `inventory-merged.md` | when two or more inventories exist | Step 03 writes it. |
| `conflicts.md` | with the merged inventory | Step 03 writes it. Every flagged row, with the evidence on each side. |
| `skipped.md` | when one inventory exists | Step 03 writes it: `reason:`, date, which inventory step 04 should read. |

Flags come from `../02-delta/delta-report.md`. Fix a wrong one there, not here, then re-run.

Contract: [../../../factory/steps/03-merge/CONTEXT.md](../../../factory/steps/03-merge/CONTEXT.md)
