# 01 Terms: bistro

What goes here: one inventory per source, and the reviewer's list of the terms expected and not
seen. Reads `../00-sources/raw/` and nothing else. An inventory a human made inside a tool the
pipeline cannot reach is pasted here too.

| File | Required | How it gets here |
|---|---|---|
| `inventory-<source>.md` | one per source | Step 01 writes it from `../00-sources/raw/<source>/`, or a human pastes it after running the matching prompt from `factory/steps/01-terms/prompts/`. One row per term per sense, each with a verbatim quote. Two lists sit at the bottom of each inventory: "Seen, not quoted" for a term with no evidence, "Out of scope" for a term with evidence that only one audience uses. |
| `review.md` | yes, before step 02 | The lead writes it. The terms expected and not seen, one row each with a status, and `reviewed:` filled with the date. Scaffold: `_review.template.md`. Step 02 does not run until it is signed. |

No scaffold for the inventory: its row shape lives once, in
[../../../factory/rules/evidence.md](../../../factory/rules/evidence.md).

Contract: [../../../factory/steps/01-terms/CONTEXT.md](../../../factory/steps/01-terms/CONTEXT.md)
