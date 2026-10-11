# 02 Delta: <project>

What goes here: the comparison of the inventories with each other and with the current glossary,
or the record that there was nothing to compare. Needs `../01-terms/review.md` with no row marked
`missing`; that is the gate.

| File | Required | How it gets here |
|---|---|---|
| `delta-report.md` | when two or more inventories exist, or a glossary does | Step 02 writes it. Seven sections, always all present. The `flag after delta` column is where every flag decision lives. |
| `skipped.md` | when one inventory and no glossary | Step 02 writes it: `reason:`, date, the inventory name. |
| `drift-report.md` | drift mode only | Step 02 in drift mode writes only this. |

Contract: [../../../factory/steps/02-delta/CONTEXT.md](../../../factory/steps/02-delta/CONTEXT.md)
