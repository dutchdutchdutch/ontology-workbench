---
project: <name>
step: 01-terms
reviewed: <YYYY-MM-DD>          # the date you read the inventories. Step 02 does not run until this is a date
reviewer: <name>
inventories: [<drive, linear-docs, linear-issues, code>]
---

# Review: <project>

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
| `<source>` | `<term>` | missing | |

Status is `missing`, `found` or `not quoted`. Step 02 runs only when no row says `missing`.
When nothing is missing, leave the table empty and write: Nothing expected is missing.

Last, sign it: put today's date in `reviewed:` and your name in `reviewer:`. An unsigned file with
an empty table and a signed file with an empty table look the same on disk. The signature is the
difference between "I read these and they are fine" and "nobody has looked yet".
