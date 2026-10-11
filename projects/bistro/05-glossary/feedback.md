---
project: bistro
step: 05-glossary
published_from: v2
---

# Feedback: bistro

What people said while using the glossary for real work, and where each item went. One row per
item. Rows are never removed. The stage moves to `adopted` only when no row is open.

| # | from | term | what they said | disposition | note |
|---|---|---|---|---|---|
| 1 | Priya | `Reservation` | "Can the glossary say booking? It's what the code says." | declined | The authority order settles the name. Booking stays in `also_called`, marked internal only |
| 2 | Rosa | `Course` | "Bar snacks come out whenever. Are they a course?" | | Open. Likely a ruling: a snack outside any course |

Disposition is empty while the row is open, then one of: `ruling NNN` (the meaning changed; the
ruling is in `../decisions/` and the next draft carries it), `edit` (wording only; changed here,
same stage), `declined` (the reason goes in note).
