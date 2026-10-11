# Core selection

How the core set is chosen and ordered. Used by step 05, and by step 04 when a review round is
about the core. One page.

The point: the core is the small set of terms a team aligns on first. It is chosen by what
depends on what, never by how often a word appears.

**Every term lives in the glossary. A subset of them is core.** The core is not a separate
product and never holds a term the glossary does not. It is a reading order and a place to start
an argument.

It earns its keep twice. A new person learns thirty words instead of a hundred and can then read
the rest. And a stakeholder discussion about a harder term gets somewhere, because a term built
out of core terms is settled by pointing at its parts. Most arguments about a compound word are
really arguments about one of the words inside it, and the core is where those live.

---

## The test

A term is core if at least one other core term cannot be defined without it, or if it is the
root of such a chain: the term a chain of core terms builds up to, which nothing else in the
core rests on. Frequency is not a reason. A word that is everywhere but that nothing
depends on is common vocabulary, not core; it goes in the backlog with a note saying so.

Work from the entries' `depends_on:` lists. That field is the evidence; if the field is empty for
a term you believe is core, the definition has not been written precisely enough yet. Fix the
definition, then the field, then the core list. Never the reverse.

## The size, round over round

A core set is meant to grow. Start small to focus the first conversations, then let each round of
review add the terms that earned their place.

| Round | Expect | What is happening |
|---|---|---|
| 1 to 2 | about 30 | The first alignment. Keep it small so stakeholders argue about meaning, not about scope. |
| 3 to 4 | 35 to 45 | Review rounds promote terms that other core terms turned out to rest on. |
| 5 to 6 | about 50 | The vocabulary is settling. Most new promotions come from resolving a compound term. |
| beyond | warn over 55 | Say so, and say why the glossary may be the better home. Then carry on if the answer is still yes. |

**Growth is the expected shape, not a defect.** A set that is the same size in round six as in
round one usually means nobody has been promoting, which is its own problem. Ask what happened to
the `next` stage in the backlog.

**Over 55, warn and steer, do not block.** Write the warning where the count lives, in
`about-core-terms.md`, and name the terms most likely to belong in the glossary instead. Then
accept whatever the reviewer decides. **The warning may be ignored, and ignoring it is not an
error.** Record that it was ignored and move on. A rule that stops work is worse than a rule that
speaks up.

The reason for the warning is not tidiness. Past about 55, the core stops doing the job in "The
point": a reader cannot hold it in their head, so it stops being the small thing you learn first,
and a discussion cannot be resolved by pointing at it. At that size the useful move is usually to
settle the compound terms in the glossary rather than to promote more parts.

`targets.core_terms` in `project.yaml` overrides the table for one project. The numbers are a
prompt, never a cap: they do not decide membership, the test above does. Falling outside them
means look again, and looking again has three honest endings. A term is demoted, the numbers are
wrong for this project, or the set grew because a term earned its place. Only the first is a
correction, and the last needs no permission.

Below the round's number usually means a whole area of the product has no agreed vocabulary yet.
Say so in the backlog and name the area.

## The two files

The core set is written twice, for two readers.

`core-terms.md` is for the person who wants to know what a word means. One `## ` heading per
category, and under it one table: two columns, the term in bold on the left and its definition on
the right. The header cells are left empty, because a column of bold terms beside a column of
sentences needs no label. Nothing else: no heading per term, no category repeated on each row, no
dependency notes, no method. A reader looks a word up here and stops.

Rows inside a category are ordered for reading, not by dependency: the container before its
parts, the general before the special. The dependency order is a different order and lives in the
other file, so the two will disagree, and that is not an error.

A table, not the entry shape from [entry-format.md](entry-format.md). That shape is for
`glossary.md`, where each term carries keys. Here there are no keys, so a heading per term buys
nothing and costs four lines each. Thirty terms fit on two screens as tables, against six as
headings, and a `## ` category stays easy to tell apart from the terms under it.

`about-core-terms.md` is for the person who wants to argue with the list. It holds the dependency
order, the cycles, the swap test, and what the shape of the set says. Keeping it out of
`core-terms.md` is deliberate: a file that has to explain itself before its first definition is
not the file a team will keep open.

## The order of the categories

The categories run in the same sequence in `core-terms.md` and in `glossary.md`. The two files do
not hold the same set, because a category can have entries and no core term, so the sequences are
not identical. They are in sync: the glossary's extra categories sit in their place in the same
run, and a reader who learns the shape of one file can find their way around the other.

The sequence:

1. **People, parties or actors, whatever the project calls them, first.** A reader cannot hold any
   other definition until they know who is involved.
2. **The end user's value stream second.** The category holding most of the terms for the thing the
   end user actually receives. If no category is clearly that one, skip this position.
3. **Everything else alphabetically, by the category heading.**
4. **A category the product does not act on goes last**, after the alphabetical run, whatever its
   letter. This is the category mapped only so a reader recognises something, never built on.

Positions 2 and 4 are judgement calls, so name the choice in `taxonomy.md` in one sentence. If
nothing fits position 2, People is followed straight by the alphabetical run; do not stretch to
fill the slot.

This is a reading order, not a claim about the work. The order things happen in is what
`taxonomy.md` is for, in prose, where it can say that a step is a gate or a loop. A sequence of
headings cannot say that, and a reader who cannot find a category pays for the attempt.

A glossary published before this rule keeps its order until its next publish.

## The order of the terms

`about-core-terms.md` holds the core in dependency order: a term appears after every term it
depends on. A reader who goes top to bottom never meets a word that has not been defined yet.
Cycles are a finding, not an error: record the cycle in the backlog as a question for the
experts, and break it in the order at the entry with the shortest definition.

## What goes in the backlog

Everything that did not make core, staged:

| Stage | Meaning |
|---|---|
| `next` | Depends on core terms and is used by more than one discipline. Likely core in the next round. |
| `later` | Used by one discipline, or not yet stable. |
| `common vocabulary` | Everywhere, but nothing depends on it. Needs an entry, not a place in the core. |
| `question` | Cannot be placed until an expert rules. Points at the verification queue item. |

---

Related: [entry-format.md](entry-format.md) ·
[../steps/05-glossary/CONTEXT.md](../steps/05-glossary/CONTEXT.md)
