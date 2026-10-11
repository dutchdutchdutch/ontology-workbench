# 06 Ontology: <project>

What goes here: the rendered picture of the glossary's relationships, for explaining and
understanding. A view, never a source. Generated; never edited by hand.

| File | Required | How it gets here |
|---|---|---|
| `ontology-data.js` | when rendered | `tools/render-ontology.py <project>` writes it from `../05-glossary/glossary.md`. `meta.scope` says which terms it drew. |
| `ontology.html` | when rendered | The same script copies the renderer next to the data. Open in a browser. |
| `skipped.md` | when not rendered | Step 06 writes it: `reason: not requested` or `reason: no glossary yet`. |

Every view is framed by `category:`, the same grouping as `../05-glossary/taxonomy.md`. A scope
narrows which terms are drawn and never regroups them. `tools/render-ontology.py <project>` draws
every entry; `--core` draws the core terms, the same set as `../05-glossary/core-terms.md`, and
is the default picture for people; `--workflows` draws the terms carrying a `workflow:` key,
still by category; `--relations-only` drops the depends-on fallbacks from whichever is in play.

An edge label is the verb the entry's own definition uses. A dashed, faint edge labelled
"depends on" is a fallback: the glossary states no relation for that pair, so the renderer fell
back to `depends_on:`. The banner toggle hides them. A picture that is mostly dashed means the
verbs are still sitting in the prose, and the fix is in step 05.

Click a term and the picture colours by what each relation claims, not by which end of the arrow
the term sits on: cyan for what it consumes, pink for what it produces, slate for structure. A
structural edge is highlighted without animating, because containment is not a movement. The
passport panel groups the same three ways. A relation is written subject verb object, and a consuming verb runs
against that: "a station reads a ticket" is station to ticket as a sentence, and ticket to
station as a flow. Grouping by flow is what makes a feedback loop read as a loop.

A workflow is a lens, not a grouping. When entries carry a `workflow:` key the banner offers a
lens control: pick a sequence and the picture marks its terms where they already sit and numbers
each by its position. Nothing moves. A workflow is a path across the taxonomy, so reading one
means watching it cross the category frames, which is the thing worth seeing.

Prefer a narrow scope for a picture people will read: a hundred nodes is a diagram nobody reads.
Re-rendering with another scope overwrites this one, which costs a single command, and
`meta.scope` always says which view is on disk.

Contract: [../../../factory/steps/06-ontology/CONTEXT.md](../../../factory/steps/06-ontology/CONTEXT.md)
