# decisions: rulings from the domain experts

One file per ruling. A ruling is an answer a domain expert gave to a question the verification
queue raised, in their own words. Rulings are inputs to step 04, never outputs of anything. Step
04 replays every one of them before it writes a draft, and stops if a draft would contradict one.

The expensive thing in this work is not the analysis. It is the human judgement collected across
weeks of review. This folder is where it lives, so a re-run cannot lose it.

## Precondition

None. Rulings arrive whenever an expert answers. The folder may be empty; step 04 then runs with
nothing to replay and says so in its header.

## Inputs

- `projects/<p>/04-draft/v<N>/verification-queue.md`: the questions.
- The expert's answer: a message, a meeting note, a comment on the queue.
- `projects/<p>/project.yaml`: `people:`, who may rule.

## Process

Done by the lead, by hand, one file per answer.

1. **Number it.** Next free `NNN`, three digits, starting at `001`. Never reuse a number.
2. **Name it.** `NNN-<slug>.md`, slug from the term: `003-walk-in-is-two-entries.md`.
3. **Fill the header.** The YAML block below. `terms` are wikilinks to the entries it touches.
4. **Quote the ruling.** Under `## Ruling`, the expert's own words, verbatim. Do not tidy. A
   paraphrase is the start of losing the ruling.
5. **State the question.** Under `## Question`, the queue item it answers, or the question as it
   was actually put.
6. **Say what it applies to.** Under `## Applies to`, which entries change and how, in one line
   each. This is what step 04 replays. A ruling may settle a relation as well as a meaning: "family
   meal comes before every service" is a ruling like any other, and step 04 writes it into
   `relations:` on replay. This is the only way a relation that no definition states gets into
   the glossary.

Rules:

- **Never edit a ruling.** When an expert changes their mind, write a new ruling and set
  `superseded_by: NNN` on the old one. Step 04 skips a superseded ruling and applies the new one.
- **When only part of a ruling falls, say so and keep the rest.** The new ruling carries
  `supersedes_in_part: NNN` and names, line by line, what is reversed and what stands. The old one
  carries `superseded_in_part_by: NNN`, keeps `status: standing`, and gains a quoted note at the
  top. Its text is never edited. Step 04 replays both, and the later ruling wins on the sentences
  it names.
  Marking such a ruling `superseded` instead would be wrong twice over: step 04 would skip it, so
  the parts that still stand would silently leave the glossary, and a reader would be told the
  whole thing was withdrawn when one sentence fell. Most rulings that fall, fall in part: the
  expert learns one new fact, not a new subject.
- One ruling per file, even when an expert answered five questions in one message. Five files.
- A ruling that contradicts another standing ruling is written down anyway, and the contradiction
  goes back to the experts as a new queue item. This folder records; it does not referee.

The file, from the worked example in [../../../projects/bistro/decisions/](../../../projects/bistro/decisions/):

```markdown
---
id: 003
date: 2026-09-08
ruled_by: Rosa
terms: ["[[Walk-in (party)]]", "[[Walk-in (cold room)]]"]
status: standing
---

# 003: Walk-in is two entries

## Question

Queue item 4, v1: the handbook uses "walk-in" for a party with no reservation and the kitchen
guide uses it for the cold room. Is it one word with two meanings, or should one of them get a
new name?

## Ruling

"Two things, both called walk-in, and nobody here will stop saying it either way. Keep the word
for both. On a screen the guest kind is always 'walk-in party'. The kitchen knows what we mean."

## Applies to

- [[Walk-in (party)]]: new entry; `also_called` gains "walk-in (floor)"; `not_to_be_confused_with`
  gains [[Walk-in (cold room)]].
- [[Walk-in (cold room)]]: new entry; `also_called` gains "walk-in (kitchen)";
  `not_to_be_confused_with` gains [[Walk-in (party)]].
```

`status:` is `standing` or `superseded`; a superseded ruling also carries `superseded_by: NNN`.
A ruling that lost only part of itself stays `standing` and carries `superseded_in_part_by: NNN`.

## Outputs

In `projects/<p>/decisions/`:

| File | Required | What it is |
|---|---|---|
| `NNN-<slug>.md` | one per ruling | Header, question, the ruling verbatim, what it applies to. |

## Human checkpoint

This folder is the checkpoint. Before running step 04 again, the lead reads the new rulings once
against the queue and confirms each answers the question it claims to. A ruling filed under the
wrong question is applied to the wrong entry, and nobody notices until a reader does.

## Status signal

The count of `NNN-*.md` files. `tools/status.sh` prints it. Step 04's header lists which ids it
applied, so a ruling that exists but was never applied is visible by comparing the two.

## Next

[../04-draft/CONTEXT.md](../04-draft/CONTEXT.md): run it again.
