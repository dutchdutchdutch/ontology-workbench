# Step 04: Draft and review

Turn the merged inventory into a numbered draft glossary, then cut a new version after each round
of rulings. This step runs many times. It never decides a contested term itself: a contested term
goes to the verification queue, a human rules on it in `decisions/`, and the next version applies
the ruling.

## Precondition

Run when one of these is true, in this order of preference:

1. `projects/<p>/03-merge/inventory-merged.md` exists (full or multi-source run).
2. `projects/<p>/03-merge/skipped.md` exists and exactly one `01-terms/inventory-*.md` exists
   (single-source run: the one inventory is the merged inventory).
3. `projects/<p>/04-draft/v1/glossary.md` exists and `01-terms/` holds no inventory (seed draft:
   the project started from an existing glossary).

If none is true, stop. Do not draft from sources directly; that is step 01's job.

## Inputs

- `projects/<p>/03-merge/inventory-merged.md`, or the single inventory (precondition 2).
- `projects/<p>/03-merge/conflicts.md` (if step 03 ran): the conflict reading list.
- `projects/<p>/02-delta/delta-report.md` (if step 02 ran): the against-glossary sections, and the
  evidence behind each flag.
- `projects/<p>/04-draft/v<N-1>/`: the previous version, for anything above v1.
- `projects/<p>/decisions/*.md`: every ruling, always, all of them.
- `projects/<p>/project.yaml`: `targets.draft_entry_cap`, `targets.core_terms`.
- [../../rules/classification.md](../../rules/classification.md): cluster classes and their tests.
- [../../rules/entry-format.md](../../rules/entry-format.md): the entry shape, the YAML block, the
  type tests, wikilinks.
- [../../rules/relation-kinds.md](../../rules/relation-kinds.md): the kinds, one object per line,
  the mirror rule.
- [../../rules/evidence.md](../../rules/evidence.md): what counts as evidence.
- [../../rules/prose-style.md](../../rules/prose-style.md): how to write for the reader.

## Process

Done by Claude, in this order. Steps 1 and 2 happen before a single entry is written.

1. **Replay the rulings.** Read every `decisions/NNN-*.md`. Build the list of terms each ruling
   touches. A ruling with `superseded_by:` is skipped and the superseding ruling is used instead.
2. **Check for contradictions.** For each ruling, compare its ruling text with what the inputs say
   about the same terms. If following the inputs would contradict a standing ruling, and the ruling
   does not already cover that case, **stop**. Write `v<N>/blocked-by-rulings.md` naming the ruling,
   the term, and the two readings. Write no `glossary.md`. A human resolves it in `decisions/`.
3. **Cluster and classify.** Group inventory rows into concepts. Classify each cluster per
   [../../rules/classification.md](../../rules/classification.md). Never merge a `homonym` row.
4. **Write entries.** One entry per concept, in the shape from
   [../../rules/entry-format.md](../../rules/entry-format.md). Apply the rulings first: a term a
   ruling covers takes the ruling's wording, and the entry's `rulings:` key cites the ruling id.
   The definition says what the thing is and nothing else: never what it is not, never a ruling
   number or its wording, never a naming rule. A ruling's result is the definition. In a draft the
   argument goes in the support prose, and the facts go to `not_to_be_confused_with:`,
   `also_called:`, `rulings:` or `visibility:`.
   Write `relations:` as you write the definition: every wikilink the definition uses with a verb
   becomes one relation, in the definition's own words. The verb is in the source quote and in
   the definition; this is the step where it is either recorded or lost.
   Write each line with one verb and one object, link last, and give it a kind in
   `relation_kinds:` where one fits. Keep one line per fact, on the entry that acts. Give every
   entry a `type:` that passes its test, and a child its parent's type. A line with no kind yet,
   or a type not yet checked, is allowed; it shows up in `coverage.md`, not as a stop.
   Stop at `targets.draft_entry_cap` (default 100). Hold the rest in an appendix table.
5. **Mark gaps.** A term with evidence but no settled meaning gets `status: gap` and a question with
   an example. Do not invent a definition.
6. **Write the conflict report.** Same thing under different names; same name for different things.
   Tables, with a recommended canonical name and a confidence per row. A third table for relation
   conflicts: pairs two sources link with different verbs, or that one links and the other does not.
7. **Write the verification queue.** Every contested term, ordered by how many other entries depend
   on it. Each item names the disciplines affected, what is contested, and the decision needed.
   A relation nobody can read in a definition is a contested item too, and goes here rather than
   into `relations:`. Items already covered by a ruling do not appear.
   **Question packs, at the end of the queue.** An entry with no relation in either direction is
   a stand-alone term: a person can read it, but an agent cannot reach it. Group these terms by
   the part of the work they belong to, one pack per group, and for each write the draft relations
   the definitions suggest. Each pack holds the questions it should make answerable, a table of
   its terms (term, type, definition today), and a table of draft relations: `#`, the draft line
   as subject, kind and `[[object]]`, the question for the expert, and an empty answer column.
   These items are marked **non-blocking**. They are guesses offered to speed up a conversation,
   not contested meanings, so they never hold step 05, even when their subject is a core term. An
   answer becomes a ruling in the expert's own words, like any other.
8. **Record what was applied.** `glossary.md` opens with a `rulings_applied:` list in its header,
   and ends with a section "Rulings applied" mapping each ruling id to the entries it changed.
9. **Write the coverage report.** `coverage.md` counts what the version holds, so the next one
   knows where to start: entries by type, relation lines with and without a kind, stand-alone
   entries, `is_a` parents with one child or more than twelve, and open question-pack items.
   Compare each count with the previous version. It is a report, never a gate: see "Built version
   over version" in [../../rules/entry-format.md](../../rules/entry-format.md).

Version numbering: `v1` is the first draft. Every later run writes a new `v<N>` folder. Never edit
an older version in place; git holds history, and the folder holds the audit trail.

## Outputs

In `projects/<p>/04-draft/v<N>/`:

| File | Required | What it is |
|---|---|---|
| `glossary.md` | yes | The draft. Header, cluster table, entries by category, appendix, rulings applied. |
| `conflict-report.md` | yes | Synonym and homonym tables with recommendations. |
| `verification-queue.md` | yes | Ordered questions for the domain experts. Empty is a valid state; say so. Question packs sit at the end, marked non-blocking. |
| `coverage.md` | yes | What the version holds and what it still lacks: types, kinds, stand-alone entries, open pack items, each against the previous version. A report, never a gate. |
| `blocked-by-rulings.md` | only on stop | Written instead of the four above when step 2 finds a contradiction. |
| `core-terms.md` | optional | A dependency-ordered core set, when the review round is about the core. |
| `contested-term-probes.md` | optional | Deep probes of a few terms, each usage quoted with source and speaker. |

## Human checkpoint

The review is the rulings. The lead and the domain experts read `verification-queue.md`, and each
answer becomes one file in `decisions/`, in the expert's own words. Then this step runs again and
cuts `v<N+1>`. A ruling that never reaches `decisions/` is a ruling that will be lost on the next
run; that is the failure this whole folder exists to prevent.

Do not start step 05 while `verification-queue.md` still holds an item that touches a core term.
Question-pack items are the exception: they are marked non-blocking and never hold step 05.
Low coverage never holds it either.

## Status signal

Step 04 has run when `projects/<p>/04-draft/v<N>/glossary.md` exists. `v1` means unreviewed.
`v2` or higher means at least one ruling has been applied. A `blocked-by-rulings.md` without a
sibling `glossary.md` means the run stopped and is waiting on `decisions/`.

## Next

[../05-glossary/CONTEXT.md](../05-glossary/CONTEXT.md) once a v2 or higher exists and the queue
holds no core-term item. Otherwise [../decisions/CONTEXT.md](../decisions/CONTEXT.md).
