# Prompt: document store

Fits: Google Drive, SharePoint, Box, S3, Confluence, Notion, Linear docs, and any tool that holds
documents, slide decks, wireframes and spreadsheets.

Copy everything below the line into the tool's own assistant, or into any chat with the exported
documents attached. Fill every placeholder first. Claude applies this same file to `raw/<source>/`
in step 01, so an inventory made here has the same shape as one made in the pipeline.

| Placeholder | Fill from |
|---|---|
| `<project>` | `project.yaml` `display_name` |
| `<scope>` | `project.yaml` `sources.<name>`: the folder link, space or site |
| `<cutoff date>` | `project.yaml` `sources.<name>.cutoff` |
| `<seed terms>` | `project.yaml` `seed_terms`, or five or six terms you already know |
| `<row target>` | 40 to 80, unless the source is tiny |
| `<disciplines>` | `project.yaml` `disciplines` |
| `<audiences>` | `project.yaml` `audiences` |

---

## Task

You are building a domain-term inventory for <project> from <scope>, documents modified since
<cutoff date>. Prioritise documents and slide decks; skip spreadsheets unless titled as a spec, a
model or definitions. A domain term is a name for something the product or business manipulates
or decides on. Seed examples: <seed terms>.

This is where each discipline's dialect lives. For every row, record the discipline the document
belongs to (<disciplines>), inferred from folder, title or author. Customer-facing documents
(decks, help articles) often use different names than internal ones; capture both. "source type"
is one of: doc, slides, wireframe, spreadsheet. Work folder by folder, then consolidate.

## Rules and output

Rules:

- A domain term is a name for something the product or business manipulates or decides on: an
  entity, a state, a role, an event, a metric, a core action. Not user-interface chrome, not
  general software words.
- One row per term per sense. Where a word is used two different ways, list it twice and flag
  both rows homonym-suspect.
- Different words for the same thing: separate rows, each flagged synonym-suspect, each naming
  the others under "variants seen". Do not pick a winner.
- Customer-facing names and internal names are both real. Capture both, flag synonym-suspect,
  do not resolve.
- No quote, no row. Every row carries one verbatim quote and a link to the item it came from.
  Verbatim: do not fix grammar, do not expand abbreviations, do not translate.
- The audience test decides scope. Keep a term in the table when two or more of <audiences> need
  to share its meaning. A term only one of them uses is that group's own extension, not common
  vocabulary: engineering's implementation detail, legal's wording, an early vision document's
  word that never shipped. Move it to the "Out of scope" list below, with its quote. Never delete
  it, and never use this test on a term that simply lacks a quote.
- Frequency is a band, never a count: rare (one or two items), occasional (a few items, or one
  team only), common (most items, from more than one team), everywhere (hard to find an item
  without it).
- Confidence is high, medium or low: how sure you are of the inferred meaning. A term with
  evidence but no settled meaning gets low, and an inferred meaning that ends in a question mark.
- Flag is one of: synonym-suspect, homonym-suspect, overloaded, unnamed-concept, or empty.
- Leave a cell empty when there is no value. Never fill a cell to make the table look complete.
- Target <row target> rows.

Output. Return only this, nothing before or after it:

1. One markdown table with exactly these nine columns, in this order:
   | term | variants seen | frequency band | source type | discipline or team | inferred meaning | example quote + link | confidence | flag |
   "example quote + link" is the quote in double quotes, then the item title as a markdown link.
   "discipline or team" is one of: <disciplines>, or empty.
2. A line "## Seen, not quoted", then one line per term you saw but could not quote, with where
   you saw it. Write "none" if there are none.
3. A line "## Out of scope", then a table with exactly these three columns:
   | term | quote | why it is out |
   One row per term that failed the audience test. Write "none" if there are none.
