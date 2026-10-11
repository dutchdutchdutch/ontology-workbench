# Step 05: Glossary and taxonomy

Publish the glossary. This is the product: the categorised entries, the dependency-ordered core
set, the taxonomy the categories form, and a staged backlog of everything that did not make core.
Everything before this step is evidence gathering; everything after it is a view.

This step is judged on precision. A definition that a reader can misread is not done, however
complete the rest of the file looks.

## Precondition

`projects/<p>/04-draft/v<N>/glossary.md` exists with N of 2 or higher (at least one ruling has
been applied), and the matching `verification-queue.md` holds no item that touches a core term.
Question-pack items, marked non-blocking, do not count. Neither does low coverage: a missing kind
or an untyped entry never blocks a publish.

## Inputs

- `projects/<p>/04-draft/v<N>/glossary.md`: the highest version. Nothing from older versions.
- `projects/<p>/04-draft/v<N>/verification-queue.md`: what is still open, for the backlog.
- `projects/<p>/decisions/*.md`: every ruling, to confirm each is reflected.
- `projects/<p>/project.yaml`: `targets.core_terms`.
- [../../rules/entry-format.md](../../rules/entry-format.md): the entry shape.
- [../../rules/relation-kinds.md](../../rules/relation-kinds.md): the kinds and the mirror rule.
- [../../rules/core-selection.md](../../rules/core-selection.md): the core test and order.
- [../../rules/prose-style.md](../../rules/prose-style.md): definitions and the swap test.

## Process

Done by Claude, then checked line by line by the lead.

1. **Carry the entries over, and strip them to the published shape.** Every entry from the draft,
   under its category, in the published shape from
   [../../rules/entry-format.md](../../rules/entry-format.md): the term, the definition, the keys.
   Order the categories by "The order of the categories" in
   [../../rules/core-selection.md](../../rules/core-selection.md): people first, the end user's
   value stream second, the rest alphabetically, and anything the product does not act on last.
   The examples, the evidence lines and the ruling notes stay behind in the draft. The
   inventories and `decisions/` already hold them, and a reader looking a word up needs the word,
   not the argument.
   Read every line before dropping it. If it carries a fact the reader needs, move that fact into
   the entry first. Nothing a reader needs may survive only in prose that is about to go.
   **The definition is not the destination for every fact.** It says what the thing is and
   nothing else: no ruling number, no statement of what the thing is not, no naming rule. Those
   go to `not_to_be_confused_with:`, `also_called:`, `rulings:` or `visibility:`. The rule and
   the table of destinations are in
   [../../rules/entry-format.md](../../rules/entry-format.md).
   An entry with `status: gap` stays a gap; do not close it here.
2. **Fill `relations`, then `depends_on`.** For every entry, read its definition twice.
   First for the verbs: every wikilink the definition uses with a verb becomes one `relations:`
   item, in the definition's own words, per
   [../../rules/entry-format.md](../../rules/entry-format.md). Then for the dependencies: the
   terms the definition cannot be written without.
   An entry whose definition uses a wikilink with a verb and carries no relation for it is not
   finished. An entry whose definition uses a wikilink it does not list in `depends_on` is not
   finished either. `depends_on` is the evidence for the next step.
   Invent no verb. If a relation is true but no definition says it, the definition is what is
   incomplete; fix that, or send the relation to `decisions/`.
   Keep `relation_kinds:` with its lines, same length, same order; it is part of the published
   shape. Check the mirror rule in
   [../../rules/relation-kinds.md](../../rules/relation-kinds.md): a fact stated from both sides
   keeps the active line only. A line with no kind is published as it is.
3. **Select and order the core.** Apply [../../rules/core-selection.md](../../rules/core-selection.md).
   Write `core-terms.md` as one table per category, the term beside its definition, no header
   labels and nothing else, so a person can look a word up in one jump. Its categories run in the
   same sequence as the glossary's, minus the ones that hold no core term. Write the dependency
   order, the cycles and the swap
   test into `about-core-terms.md`, so the method never stands between a reader and a definition.
4. **Write the taxonomy.** The categories, what each holds, and how they relate, in one table and
   a short paragraph each. Categories come from the entries' `category:` keys; the taxonomy does
   not invent a category no entry uses. List them in the published sequence, and say in one
   sentence which category took the value-stream slot and which, if any, was sent to the tail.
   The order things happen in is prose here, not a heading sequence.
5. **Stage the backlog.** Everything not in core, by stage (`next`, `later`, `common vocabulary`,
   `question`), each with the one-line reason.
6. **Confirm the rulings.** For every ruling in `decisions/`, name the entry that reflects it in a
   closing section "Rulings reflected". A ruling with no entry is a finding; say so and stop.

Rules:

- Nothing in this step is done to make the ontology look better. If a relation or a category
  would only exist for the picture, leave it out.
- Read every definition back before publishing. A clause that only makes sense to somebody who
  followed the argument belongs in a key, not in the definition.
- Every `not_to_be_confused_with` names a confusion actually seen in the evidence.
- The published glossary is the only source of meaning step 02's drift mode and step 06 read.
  Keep it whole. Step 06's machine lens also reads the open question-pack items from the draft it
  came from, and carries them as unconfirmed, never as meaning.

## Outputs

In `projects/<p>/05-glossary/`:

| File | Required | What it is |
|---|---|---|
| `glossary.md` | yes | The entries, by category. Header names the draft version it was published from and the stage it is at. |
| `core-terms.md` | yes | The core set grouped by category. One definition per term, nothing else. |
| `about-core-terms.md` | yes | How the core was chosen, the dependency order, the cycles, the swap test. |
| `taxonomy.md` | yes | The categories and how they relate. |
| `backlog.md` | yes | Everything not core, staged, with reasons. |
| `feedback.md` | from `trial` on | One row per item of trial feedback and where it went. |

The header of `glossary.md`:

```yaml
---
project: <name>
step: 05-glossary
published_from: v3
stage: review          # review | trial | adopted
stage_since: 2026-09-19
reviewed_by: []        # names, one added as each reviewer signs off
---
```

Re-publishing: a new draft version leads to a new publish. The old files move to
`projects/<p>/_archive/` with the version they were published from: `glossary-v3.md`. The new
publish opens at `stage: review`.

## After publishing: review, trial, adoption

Publishing is not the end. A glossary earns trust in three stages, and the stage is a fact about
the one published file, so it lives in that file's header. There are no `trial/` or `adopted/`
folders and no stage in a filename: every reader of the glossary (drift mode, step 06,
`tools/status.sh`) depends on one file at one path, and a second copy would be a second product.
Git holds the history; each stage change is one commit.

| Stage | Meaning | Ends when |
|---|---|---|
| `review` | Published from draft v<N>. The lead and the named reviewers read it. | Every reviewer in `reviewed_by:` has signed off and the lead has run the swap test on the core. Set `stage: trial`. |
| `trial` | The team uses it for real work. Feedback goes into `feedback.md`. | Every row in `feedback.md` has a disposition. Set `stage: adopted`. |
| `adopted` | The glossary is the team's vocabulary. Drift mode watches it. | A re-publish, which returns the stage to `review`. |

`feedback.md` has one row per item: `#`, `from`, `term`, `what they said`, `disposition`,
`note`. A row is open while `disposition` is empty. Rows are never removed. Each item goes one of
three ways:

- **Meaning changes.** Write a ruling in `projects/<p>/decisions/`. Step 04 cuts the next draft;
  this step re-publishes. Disposition: `ruling NNN`. This is the existing loop; trial only names
  where the question came from.
- **Wording only.** Edit the published glossary here. Same stage, one commit. Disposition:
  `edit`.
- **Declined.** Disposition: `declined`, with the reason in `note`.

A re-publish sets `stage: review`. The lead may set `trial` directly when every change came from
trial feedback that the reviewers already saw. A wording-only edit keeps the current stage.

## Human checkpoint

The lead reads every core entry in `core-terms.md` and runs the swap test from
[../../rules/prose-style.md](../../rules/prose-style.md), which `about-core-terms.md` repeats in
place for the reviewer: replace the term with its nearest
synonym; if the sentence still reads true, the definition is too loose. Then the same for any
entry with more than two relations. Read each relation aloud as a sentence, subject verb object:
"an allergy note is part of an order". A sentence that is false, or that no definition says,
is the finding. This is the main session of the engagement; it is where the precision is bought.

Two more gates follow, one per stage change. Before `trial`: every reviewer in `reviewed_by:` has
signed off. Before `adopted`: no row in `feedback.md` is open. Both are the lead's call, made by
editing the header and committing.

## Status signal

Step 05 is done when `projects/<p>/05-glossary/glossary.md` exists and the lead has run the swap
test on the core. Its `stage:` field says how far the glossary is trusted; `tools/status.sh`
prints it, and for `trial` counts the open rows in `feedback.md`.

## Next

[../06-ontology/CONTEXT.md](../06-ontology/CONTEXT.md), on request, and
[../07-streams/CONTEXT.md](../07-streams/CONTEXT.md) on top of it. Otherwise the stages above:
review, then trial, then adopted. At `trial`, [../08-publish/CONTEXT.md](../08-publish/CONTEXT.md)
sends the vocabulary out; send again after every re-publish that reaches `trial`. Once `adopted`,
run step 02 in drift mode on a schedule.
