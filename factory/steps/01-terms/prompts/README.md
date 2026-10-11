# Prompts: one per source type

What is here: the instruction that turns one source into a term inventory. One file per common
source type, not per tool, because tools of one type ask for the same things. Linear and Jira are
both issue trackers. Drive, SharePoint and Box are all document stores.

| File | Type | Tools it fits |
|---|---|---|
| [issue-tracker.md](issue-tracker.md) | tickets with titles, descriptions, comments | Linear, Jira, GitHub Issues, Asana, Shortcut |
| [document-store.md](document-store.md) | documents, decks, wireframes, sheets | Google Drive, SharePoint, Box, S3, Confluence, Notion, Linear docs |
| [code-repository.md](code-repository.md) | pull requests and branch names | GitHub, GitLab, Bitbucket |

Claude runs the same file. The contract in [../CONTEXT.md](../CONTEXT.md) says "apply
`prompts/<type>.md` to `raw/<source>/`", so an inventory made inside a tool and one made in the
pipeline have the same shape by construction.

## When to run one by hand

The pipeline has no connector to the tool. The team does not allow one, or none exists. Step 00
has written the source under "Inventoried externally" in `00-sources/manifest.md`, naming the
prompt file to use.

## How to fill it

Every prompt has a placeholder table at the top. Fill each placeholder from `project.yaml`
before you copy. `<seed terms>` is optional but worth five minutes: five or six terms you already
know steer the search towards the product's own words.

## How to run it

Copy everything below the horizontal line into the tool's own assistant, or into any chat with
the exported text attached. Keep the output exactly as returned. Do not tidy the table.

## How to paste it back

1. File: `projects/<p>/01-terms/inventory-<source>.md`, where `<source>` is the key of the
   source in `project.yaml`.
2. Front matter, then a heading, then the table as returned, then the `## Seen, not quoted`
   section as returned:

```markdown
---
project: <name>
step: 01-terms
source: <source>
produced_by: external
tool: <the tool the prompt ran in>
prompt: <type>.md
run: <YYYY-MM-DD, the date you pasted>
rows: <n>
---

# Inventory: <source> (<project>)
```

3. A row without a quote: move it under `## Seen, not quoted` by hand. Do not delete it.
4. In `00-sources/manifest.md`, fill the "Pasted" date on the source's row.
5. Write `01-terms/review.md` as for any inventory: the terms you expected and do not see. When
   a term is missing from an external inventory, re-run the prompt with that term under
   `<seed terms>`; Claude cannot search a source it cannot reach.

## A new source type

Copy the closest file. Change only the `## Task` section; keep `## Rules and output` identical
to the other files, byte for byte. Name the file by the type, as a noun: `chat-transcripts.md`,
not `slack.md`. Add a row to the table above, and note the decision in `DESIGN-NOTES.md`.
