# Relation kinds

Every line in `relations:` can carry a kind: one short, fixed word that says what sort of fact the
line states. The verb stays for the person. The kind is for a script or an agent, which cannot
answer "who pays whom?" from dozens of different verbs. Read
[entry-format.md](entry-format.md#relations-and-depends_on-are-two-different-claims) first; this
page holds the list and the rules that go with it.

---

## The shape

The kinds sit in their own list, `relation_kinds:`, at the same position as the line they name.

```yaml
relations: ["contains [[Guest]]", "holds [[Reservation]]"]
relation_kinds: [contains, holds]
```

- The two lists have the same length. Item 3 of `relation_kinds:` names item 3 of `relations:`.
- A value is one of the 21 kinds below, its inverse form, or an extra the project lists in
  `project.yaml`.
- An entry with relations and no `relation_kinds:` is allowed. The glossary is built version over
  version, and a missing kind is reported, not refused. See
  [entry-format.md](entry-format.md#built-version-over-version).

## The line rules

1. **One verb, one object, and the line ends with that `[[link]]`.** "serves [[Table]]", not
   "serves a [[Table]] through the whole service". Detail belongs in the definition. A line with two objects
   is two lines, each with its own kind.
2. **One line per fact, said by the one who acts.** When two entries state the same fact from
   opposite sides, keep one line: the active one, on the entry that acts, and from the product's
   own side where the product is a party. Remove the other line from `relations:`. The definition
   may still use the other side's words; only the line goes. This is the mirror rule.
3. **Two lines that say different things are not a mirror.** "A tip pays a server" and "a check
   bills a party" are two acts going opposite ways. Both stay.
4. **The inverse is generated, never written.** A script that needs both directions (an agent
   starting from the object, for example) builds the reverse line from the table below. A person
   reads the glossary with one line per fact.

## The 21 kinds

The active form names the fact from the subject. The inverse form is for a line whose subject is
the one acted on, which rule 2 makes rare. Flow is what step 06 draws: see
[entry-format.md](entry-format.md#the-flow-column-and-why-a-sentence-is-not-enough).

| Family | Kind | Inverse | "X [kind] Y" means | Flow |
|---|---|---|---|---|
| Kind of | `is_a` | `has_kind` | every X is a Y, or a condition of a Y | structure |
| | `aspect_of` | `has_aspect` | X is the same organisation as Y, named by one regime | structure |
| Structure | `contains` | `part_of` | Y is listed in, held inside or carried on X | structure |
| | `identifies` | `identified_by` | X is the number or code that points at Y | structure |
| | `holds` | `held_by` | X possesses Y (a credential, a listing) | structure |
| | `employs` | `employed_by` | X employs Y | structure |
| Rules | `requires` | `required_by` | X cannot happen or be valid without Y | structure |
| | `blocks` | `blocked_by` | X stops Y from happening or being valid | structure |
| | `governs` | `governed_by` | X sets the terms, rate or limits of Y | produces |
| | `authorizes` | `authorized_by` | X gives permission or funding for Y | produces |
| Work | `follows` | `precedes` | X happens after Y in the work | structure |
| | `performs` | `performed_by` | X does or keeps Y | produces |
| | `serves` | `served_by` | X delivers a service to Y | produces |
| | `creates` | `created_by` | X brings Y into being (writes, issues, generates, triggers) | produces |
| | `becomes` | `became_from` | X turns into Y | produces |
| | `verifies` | `verified_by` | X confirms or checks Y | produces (both forms) |
| Money and data | `pays` | `paid_by` | X sends money to Y | produces |
| | `bills` | `billed_by` | X asks Y for money | produces |
| | `feeds` | `fed_by` | X's data or hours flow into Y | produces |
| | `measures` | `measured_by` | X is a number that tracks Y | produces (both forms) |
| | `concerns` | `concerned_by` | X is about Y (a flag, a note, a match) | produces |

**An inverse consumes, unless its agent only takes the subject in.** "Y is paid by X" says the
money lands in Y, so the flow runs against the sentence, from X to Y. That holds for every inverse
whose agent brings the subject into being or fixes its value. Two inverses are the other family
(see the two families of passive verbs in [entry-format.md](entry-format.md#the-flow-column-and-why-a-sentence-is-not-enough)):
`verified_by` and `measured_by` **produce**. Checking or measuring leaves the subject as it was,
and the result lands in the agent: an expo inspects a course and takes the answer in, so the
course flows to the expo. A structure kind stays structure in both forms.

**Flow comes from the kind.** Where a line has a kind, the kind decides the flow, and the verb is
not read. Where it has none, the verb table in
[entry-format.md](entry-format.md#relations-and-depends_on-are-two-different-claims) and the
project's `verbs:` block decide, as before.

The 21 were fitted to a real glossary and covered every line in it. They are meant to be
generic: each word means the same in any product. A kind that only makes sense in one product is
an extra, below.

## A project's own kinds

When no kind fits, a project adds one in `projects/<p>/project.yaml`, beside `verbs:`:

```yaml
relation_kinds:
  represents: { inverse: represented_by, flow: produces }   # X acts for Y
```

An extra needs an inverse and a flow, and the flow is one of `produces`, `consumes` or
`structure`. Add one only when a line truly fits none of the 21; stretching a kind is better than
a second name for the same fact. An extra that a second project also needs is a candidate for
this table, through a note in `DESIGN-NOTES.md`.

---

Related: [entry-format.md](entry-format.md) ·
[../steps/04-draft/CONTEXT.md](../steps/04-draft/CONTEXT.md) ·
[../steps/06-ontology/CONTEXT.md](../steps/06-ontology/CONTEXT.md)
