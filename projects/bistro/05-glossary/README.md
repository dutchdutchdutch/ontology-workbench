# 05 Glossary: bistro

What goes here: the product. The published glossary, the core set, the taxonomy, the backlog,
and during trial the feedback. Written from the highest reviewed draft in `../04-draft/`.
Re-publishing moves the old files to `../_archive/` named with the draft version they came from.

| File | Required | How it gets here |
|---|---|---|
| `glossary.md` | yes | Step 05 writes it. Entries by category. Header carries `published_from`, `stage`, `stage_since`, `reviewed_by`. |
| `core-terms.md` | yes | Step 05 writes it. One table per category, a term beside its definition on each row, no header labels, nothing else. |
| `about-core-terms.md` | yes | Step 05 writes it. How the core was chosen, the dependency order, the cycles, the swap test. |
| `taxonomy.md` | yes | Step 05 writes it. |
| `backlog.md` | yes | Step 05 writes it. Everything not core, staged. |
| `feedback.md` | from `trial` on | Copy `_feedback.template.md`. One row per item the team raised while using the glossary, and where it went. |

A published entry is three things: the term, its definition as a quoted line, and its YAML block.
The definition says what the thing is and nothing else: never what it is not, never a ruling
number or its wording, never a naming rule. Each of those has a key instead.
That is all. The examples, the evidence lines and the ruling notes stay in the draft that produced
it, because `../01-terms/` and `../decisions/` already hold them and a reader looking a word up
needs the word, not the argument. [../../../factory/rules/entry-format.md](../../../factory/rules/entry-format.md)
holds both shapes.

The same split runs through the other files. `core-terms.md` is definitions only, laid out as one
table per category so thirty terms fit on two screens. `about-core-terms.md` takes the method.
Keeping the two apart is the point: a file that explains itself before its first definition is
not a file a team keeps open.

The glossary passes through three stages, named in its header as `stage:`. No folders, no
stage in a filename: one file, one path, and git holds the history.

| `stage:` | Means | Moves on when |
|---|---|---|
| `review` | Just published. Reviewers read it. | Every reviewer has signed off and the lead has run the swap test on the core. |
| `trial` | The team uses it for real work. | Every row in `feedback.md` has a disposition. |
| `adopted` | The team's vocabulary. Drift mode watches it. | A re-publish, which starts again at `review`. |

This folder is what step 02's drift mode and step 06 read. The picture in `../06-ontology/` is a
view of `glossary.md`; if they disagree, this file wins.

Contract: [../../../factory/steps/05-glossary/CONTEXT.md](../../../factory/steps/05-glossary/CONTEXT.md)
