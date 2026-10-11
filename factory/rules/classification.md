# Classification rules

How inventory rows become concepts, and what class each concept gets. Used by step 02 when it
decides flags, by step 03 when it applies them, and by step 04 when it clusters. One page.

The point: the class tells the reviewer what kind of decision a term needs, before they read the
definition.

---

## From rows to concepts

A concept is a set of inventory rows that name the same thing. Rows join a concept when the term
matches (case and plural ignored) or when one row lists the other's term under "variants seen".
A row whose sense differs from the rest of the cluster stays out and starts its own concept, even
when the word is the same.

Never merge a row flagged `homonym` or `homonym-suspect` into another row's concept.

## The five classes

| Class | Meaning | Test | What the reviewer decides |
|---|---|---|---|
| `CLEAN` | One name, one meaning, across sources. | No flag on any row, and the inferred meanings agree. | Nothing. Skim only. |
| `SYNONYM` | One meaning, several names. | Two or more rows with different terms and the same inferred meaning. | Which name is canonical. The others go under "Also called". |
| `HOMONYM` | One name, several meanings. | Two or more rows with the same term and inferred meanings that cannot both be true of one thing. | A distinct name per sense. Each sense gets its own entry. |
| `OVERLOADED` | Roughly one meaning, but sources define it at different scope or precision. | Same term, meanings that overlap but differ in what they include. An agent reading one source and writing against another would drift. | The precise boundary. These rows are the ones most likely to produce wrong code or wrong copy. |
| `UNNAMED` | A thing people describe but do not name. | The concept appears in quotes and code, but no row has a stable term for it. | Whether it needs a name, and what. |

A concept can carry two classes: `HOMONYM` on the name and `SYNONYM` on one of its senses is
common. Record both.

## Suspect and confirmed

Inventory rows carry `-suspect` flags because one source cannot confirm a split or a match. Step
02 decides these in `02-delta/delta-report.md`, in the `flag after delta` column. Step 03 copies
them into the merged table and never re-derives them:

- `homonym-suspect` becomes `homonym` when a second source shows the second sense.
- `synonym-suspect` becomes `synonym` when a second source uses both names for one thing.
- A suspect flag with no confirmation stays suspect and goes to the verification queue in step 04.
  It is not dropped.

## Canonical name, when a ruling has not said

Step 04 proposes a canonical name for each `SYNONYM` concept. Apply these in order, and say in the
entry which rule decided:

1. The name used in the most authoritative written source. `project.yaml` may name it; by default
   Linear docs, then drive documents, then issues, then code.
2. The name most disciplines already share.
3. The shortest.

A proposed name is a proposal. It goes to the verification queue when the rule's result looks
wrong, and a ruling in `decisions/` overrides it every time.

---

Related: [evidence.md](evidence.md) · [entry-format.md](entry-format.md) ·
[../steps/02-delta/CONTEXT.md](../steps/02-delta/CONTEXT.md) ·
[../steps/03-merge/CONTEXT.md](../steps/03-merge/CONTEXT.md) ·
[../steps/04-draft/CONTEXT.md](../steps/04-draft/CONTEXT.md)
