# Evidence rules

Every claim in an inventory rests on something a reader can go and check. One page. Read this
before writing any inventory row, before running a prompt inside a tool, and again before merging
rows.

The point: a glossary is only useful if every meaning in it can be traced back to a place where
someone actually used the word that way.

---

## No quote, no row

Every inventory row carries one verbatim quote, the title of the document it came from, and a
link to it. A term you remember seeing but cannot quote does not get a row in the table. It goes
under `## Seen, not quoted` at the bottom of the same inventory file. A later pull, or a re-run of
step 01 with the term listed in `01-terms/review.md`, finds the quote or leaves it there. It is
never deleted: the reviewer's expectation is evidence of an assumption step 02 must check.

Verbatim means verbatim. Do not fix grammar, do not expand abbreviations, do not translate. The
quote is evidence of how people write, not of what they meant.

## Out of scope is not the same as unquotable

A glossary exists so that different groups agree on the key terms. `audiences:` in
`project.yaml` names those groups. A term stays in the table when two or more of them need to
share its meaning. A term only one group uses is that group's own extension of the common
vocabulary: engineering's implementation detail, legal's wording in a privacy notice, an early
vision document's word that never shipped. All three are real, and none belongs in a glossary
that is meant to be shared. Those terms move under `## Out of scope` at the bottom of the
inventory, in a table of term, quote and why it is out.

Keep the two lists apart. `## Seen, not quoted` means there is no evidence. `## Out of scope`
means there is evidence, and one audience. A term goes in one or the other, never both, and is
deleted from neither. The lead overrules the test at the checkpoint, and a row in
`01-terms/review.md` brings a term back into the table using the quote it already carries.

## The row

One row per term per sense, in this order:

| Column | What goes in it |
|---|---|
| term | The word as the source spells it. Case kept. |
| variants seen | Other spellings and other words used for the same thing in this source, comma separated. |
| frequency band | `rare`, `occasional`, `common` or `everywhere`. Never a count. |
| source type | `doc`, `slides`, `wireframe`, `spreadsheet`, `linear doc`, `issue`, `pr`, `branch`, `code`. |
| discipline or team | Who wrote it: `product`, `engineering`, `design`, or as `project.yaml` lists them. Empty if unknown. |
| inferred meaning | One sentence. What the writer meant, in plain words. |
| example quote + link | The verbatim quote, then the document title as a link. |
| confidence | `high`, `medium`, `low`. How sure the inferred meaning is. |
| flag | `synonym-suspect`, `homonym-suspect`, `overloaded`, `unnamed-concept`, or empty. |

Leave a cell empty when there is no value. Never fill a cell to make the table look complete.

The prompts in [../steps/01-terms/prompts/](../steps/01-terms/prompts/README.md) restate this row
for a human running them inside a tool. Change the row here and there together.

## Frequency as bands

Bands, never counts. A count invites false precision and goes stale the day a document is added.

| Band | Test |
|---|---|
| `rare` | One or two documents use it. |
| `occasional` | A few documents, or one discipline only. |
| `common` | Most documents from more than one discipline. |
| `everywhere` | Hard to find a document that does not use it. |

The highest band across sources wins at merge time.

## Same word, different meanings

Separate rows, each flagged `homonym-suspect`. Never merge them, at inventory time or at merge
time. A homonym that is merged becomes a definition that is wrong for half its readers, and no
later step can see that it happened.

`homonym-suspect` becomes `homonym` when `02-delta/delta-report.md` finds a second source that
shows the second sense. Step 02 decides; step 03 applies.

## Different words, same meaning

Separate rows, each flagged `synonym-suspect`, each listing the others under "variants seen". Do
not pick a winner here. Whether two sources agree that two names are one thing is decided in
`02-delta/delta-report.md`, never in an inventory. Choosing the canonical name is a step 04
decision, made with the conflict report and the rulings in view. An inventory that resolves
synonyms hides the evidence the reviewer needs.

## Internal and customer-facing names

Capture both. A team often has one word for the thing on the inside (`org`, `tenant`) and another
in the product (`account`, `workspace`). Both are real, both go in, and the glossary entry later records
which is which under "Also called". Do not choose between them at inventory time.

## Mark gaps, do not fill them

A term with evidence but no settled meaning gets `confidence: low` and an inferred meaning that
ends in a question mark, with the quote that raised it. A question mark with an example is worth
more than an invented definition, because the reviewer can answer a question and cannot spot a
plausible invention.

## Only the raw pulls

Inventories read `00-sources/raw/` and nothing else. If a term seems to be missing, the fix is
another pull in step 00, or a row in `01-terms/review.md` that sends step 01 back to `raw/` for
that term. Never a search from step 01 outside `raw/`. That is what makes step 01 cheap to re-run.

## Exception: external inventories

A team may not allow a connector to one of its tools. Then a human runs the matching prompt from
`factory/steps/01-terms/prompts/` inside that tool and pastes the table into
`01-terms/inventory-<source>.md`. There is no `raw/<source>/` for it. The evidence is the quote
and link on each row, which is the same evidence every other row carries. The manifest records
the source under "Inventoried externally"; the inventory's front matter says
`produced_by: external` and names the tool and the prompt. Steps 02 and 03 treat it like any
other inventory. A missing term is fixed by re-running the prompt with the term under seed terms,
not by a search from step 01. An external inventory carries an `## Out of scope` section like any
other; the prompt the human ran asks for one.

---

Related: [classification.md](classification.md) · [entry-format.md](entry-format.md) ·
[../steps/01-terms/CONTEXT.md](../steps/01-terms/CONTEXT.md) ·
[../steps/02-delta/CONTEXT.md](../steps/02-delta/CONTEXT.md)
