---
project: bistro
step: 01-terms
reviewed: 2026-09-03
reviewer: Theo
inventories: [drive, linear-issues, code]
---

# Review: bistro

Three questions, one table.

1. Which terms did I expect to see and do not? A row below, status `missing`. A re-run of step 01
   adds the row when it finds a quote, and lists the term under "Seen, not quoted" in the
   inventory when it does not. Rows are never removed from an inventory.
2. Is anything under "Out of scope" in the wrong place? That list holds terms with a quote that
   only one audience uses. The test is a judgement and you overrule it. A row below, status
   `missing`, brings the term back using the quote it already carries.
3. For each term you would call core, does a quote say how it relates to another term? Step 04
   writes `relations:` out of those verbs, and it can only use the ones a quote carries. A "no"
   here is a note in the table, not a `missing` row: it does not hold step 02 up, it tells step
   04 where the picture will be thin.

| source | expected term | status | note |
|---|---|---|---|
| drive | turn | found | The first run put it under "Out of scope" as a floor-only word. Overruled: the kitchen plans prep on how many turns we expect, and the app will report turns. The re-run moved it into the table with the quote it already had. |
| linear-issues | tip | not quoted | Looked for again. No issue mentions tips; the app does not handle them yet. Listed under "Seen, not quoted". The drive quote is enough. |
| drive | family meal | found | Question 3: no quote links family meal to any other term. Expect it to stand alone in step 04. |

Signed 2026-09-03 by Theo. The re-run with this review finished the same day; no row is `missing`.
