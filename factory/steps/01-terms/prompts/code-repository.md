# Prompt: code repository

Fits: GitHub, GitLab, Bitbucket, and any tool that holds pull requests and branch names.

Copy everything below the line into the tool's own assistant, or into any chat with the exported
pull request list attached. Fill every placeholder first. Claude applies this same file to
`raw/<source>/` in step 01, so an inventory made here has the same shape as one made in the
pipeline.

| Placeholder | Fill from |
|---|---|
| `<project>` | `project.yaml` `display_name` |
| `<scope>` | `project.yaml` `sources.code.github_repo` |
| `<cutoff date>` | `project.yaml` `sources.code.pr_cutoff` |
| `<seed terms>` | `project.yaml` `seed_terms`, or five or six terms you already know |
| `<row target>` | 40 to 80, unless the source is tiny |
| `<disciplines>` | `project.yaml` `disciplines` |
| `<audiences>` | `project.yaml` `audiences` |

---

## Task

You are building a domain-term inventory for <project> from the repository <scope>: pull
requests opened since <cutoff date>, their titles, and the branch names behind them. The term is
the name as code spells it (identifier, table, enum value, PR scope), case kept. The quote is the
PR title or the branch name, verbatim, with the PR link. "source type" is one of: pr, branch,
code. "discipline or team" is engineering unless the repository says otherwise. Seed examples:
<seed terms>.

Where code uses one word for two things (a "table" that is a database table and a "table" a guest sits at), write two rows, both homonym-suspect. Do not map code names to product names here;
that comparison is a later step. Work module by module (or PR scope by PR scope), then
consolidate.

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
