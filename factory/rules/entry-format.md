# Entry format

The shape of one glossary entry, in a draft (step 04) and in the published glossary (step 05).
One page. Read this before writing or editing any `glossary.md`.

The point: the entry has to serve two readers at once. A person reads the heading and the prose.
A script reads the heading and the YAML block. Neither reader should need the other's part.

The person comes first, because the person is the one who has to agree with the definition. So
the definition sits directly under the heading as a quoted line, and the keys sit at the end,
where a person can skip them and a script can still find them.

---

## One file per version

A glossary is one file: `04-draft/v<N>/glossary.md` for a draft, `05-glossary/glossary.md` for
the published one. Entries live inside it under category headings. There is no file per term;
editing a hundred small files was judged unmanageable, and git already tracks change per entry.

## Two shapes, one for each job

A draft and a published glossary are read by different people for different reasons, so the entry
has two shapes. The keys and the definition are the same in both. Only the support prose differs.

| | Draft, step 04 | Published, step 05 |
|---|---|---|
| Read by | a handful of reviewers deciding what is true | everybody, to look a word up |
| Holds | definition, support prose, keys | definition, keys |
| Why | a reviewer cannot judge a definition without the quotes behind it | a reader needs the word, not the argument |

Nothing is lost by dropping the support prose at publish. The quotes stay in
`01-terms/inventory-*.md`, the reasoning stays in `decisions/`, and the draft itself stays in
`04-draft/v<N>/`. The published entry keeps `rulings:`, which is the thread back to all three.

## The published entry

```markdown
### Guest

> A person who comes to the restaurant to eat, from the moment they arrive until they leave.

```yaml
type: role
owner: floor
status: verified
category: People
core: true
also_called: [customer (internal only)]
not_to_be_confused_with: ["[[Cover]]"]
rulings: [001]
```
```

Three lines of structure: the term, the definition, the keys. Nothing between them and nothing
after them. A key with nothing to say is left out: a guest is a root term, so it has no
`depends_on:`, and the line that joins it to [[Party]] lives on Party, the entry that acts. Note what the definition does not carry: ruling 001 settled that "customer" never
appears on a screen, and that fact is in `also_called:` and `rulings:`, not in the sentence a
reader came to read. A reader scrolling a hundred entries meets a heading and a quoted sentence every
time, in the same place every time.

The definition is a blockquote so that it stands out, and so that a script can find it without
counting paragraphs. A blockquote marks the definition and nothing else, anywhere in the file.

**Nothing that a reader needs may live only in the support prose.** If a ruling settled a fact
that a reader has to know, the fact belongs in the definition, not in a note under it. That check
belongs to step 05, before the prose is dropped.

## The draft entry

The same, with the support prose kept between the definition and the keys.

```markdown
### Guest

> A person who comes to the restaurant to eat, from the moment they arrive until they leave.

**Not to be confused with** [[Cover]], which is a guest counted, not a guest served. The floor
says "a twelve-top" and "twelve covers" for the same table, and the two words do different jobs.
**Naming** ruling 001 makes "guest" the only word on a screen. "Customer" is the app's database
table and is marked as such in `also_called:`. The rule lives in the key; the definition says
what a guest is.
**Examples** "We never say customer on the floor. Everyone who walks in is a guest" ([Staff
handbook](../../projects/bistro/00-sources/raw/drive/staff-handbook.md)) · "Customer record keeps
the phone number from the booking" ([BIS-14](../../projects/bistro/00-sources/raw/linear-issues/BIS-14.md)).
**Evidence** inventory rows: guest, customer.

```yaml
type: role
owner: floor
status: verified
category: People
core: true
...
```
```

Quotes from sources stay inline on the `**Examples**` line, with quotation marks, so a quote is
never mistaken for the definition.

The example is from [../../projects/bistro/](../../projects/bistro/), a fictional restaurant
kept as a worked example of every step.

## The nine fields, and where each lives

| Field | Lives in | Values |
|---|---|---|
| Term | the `### ` heading | The canonical name. One entry per sense; a homonym gets two headings with a qualifier: `Walk-in (party)`, `Walk-in (cold room)`. |
| Type | `type:` | One of twelve, each with a test: `role`, `organisation`, `entity`, `document`, `credential`, `identifier`, `rule`, `metric`, `action`, `event`, `state`, `surface`. See [Types, and the test for each](#types-and-the-test-for-each). |
| Definition | the blockquote under the heading | One to three sentences. Says what the thing is, then what it is for. Never what it is not, and never a ruling. Wikilinks to other terms. See [A definition says what a thing is](#a-definition-says-what-a-thing-is). |
| Also called | `also_called:` | Other names in use, including the deprecated and the customer-facing ones. Which is which is marked in the value: `waiter (deprecated)`. |
| Not to be confused with | `not_to_be_confused_with:`, plus a prose line in a draft | Wikilinks. Every item names a confusion actually seen in the evidence. In a draft the prose says how to tell them apart; at publish that difference moves into the two definitions. |
| Examples | the `**Examples**` line, draft only | Two verbatim quotes with links, from different sources where possible. |
| Owner | `owner:` | The discipline that decides this term's meaning: `product`, `engineering`, `design`, or as `project.yaml` lists them. |
| Status | `status:` | `draft`, `verified`, `gap`, `deprecated`. `gap` means the definition is a question with an example, not an answer. |
| Evidence | the `**Evidence**` line, draft only | The inventory rows and PRs the entry rests on. |

## Types, and the test for each

Every entry has one `type:`. The test: the sentence **"A [term] is a [type]."** must be true when
read aloud. A type with no test turns into a catch-all, and an agent asked "list the roles" then
gets a law and a company back.

| Type | "X is …" | Examples |
|---|---|---|
| `role` | a part a person or organisation plays | guest, server, host |
| `organisation` | a named body that exists apart from any role it plays | a regulator, a supplier company |
| `entity` | a thing that exists and is none of the other types | table, course, menu item |
| `document` | a written record that someone issues, signs or submits | a supplier contract, a signed delivery note |
| `credential` | something a person or business must hold to be allowed to work | a food handler's certificate, a liquor licence |
| `identifier` | a number or code that points at one thing | an order number, an account ID |
| `rule` | a law, regulation, policy or exemption that says what must or may happen | a privacy law, a refund policy |
| `metric` | a number measured over a period | conversion rate, retention |
| `action` | something someone does | firing a course, comping a dish |
| `event` | something that happens at a point in time | a seating, a no-show |
| `state` | a condition another term is in | an overdue task, a paid invoice |
| `surface` | a system, app or device people use | the mobile app, a partner portal |

**A child shares its parent's type.** An entry with an `is_a` line takes the type of the entry it
points at, so "every kind of document" is one query. The one exception is a `state` that names a
condition of its parent: an overdue task is a task, but its type is `state`.

**When two types both pass**, pick the one that says what matters about the term, and write the
choice in a ruling. A website that is also a public register can be `surface` or `entity`; the
ruling says which one the team means.

## Kind of: the is-a test

A hierarchy is a relation like any other. It is written in `relations:` with the kind `is_a`:

```yaml
relations: ["is a [[Party]]"]
relation_kinds: [is_a]
```

- **`is_a` means every X is a Y.** Every walk-in party is a party. The reverse is never true, and
  is never written. A test: if one X exists that is not a Y, the line is wrong.
- **No cycles.** If X is a Y, Y is never an X, at any distance.
- **One child, or more than twelve, is a warning.** One child usually means the child is really a
  state or an alias. More than twelve usually means a level is missing between them. Neither is an
  error; say so in `coverage.md` and move on.
- **One organisation with several names is not a hierarchy.** When two regimes name the same body
  (a tax form calls it one thing, a supplier contract another), use `aspect_of`: "X is the same organisation as
  Y, named by one regime". `is_a` would claim one is a narrower case of the other, which is false.

`is_a` replaces the `is a kind of` verb for hierarchy. A line that still says `is a kind of`
without a kind is read as `is_a`.

## A definition says what a thing is

A reader looks a word up to find out what it means. Everything else in the entry is for somebody
else, or for later. So the definition carries the meaning and nothing else.

**Never write what the thing is not.** "A party that arrives to eat, not one that booked
ahead" spends its last clause on a different term. Say it positively: "a party that arrives to
eat without a reservation". The word "without" carries the same fact and costs one word
instead of a clause. Where a negative cannot be turned positive, it is a distinction,
and a distinction belongs in `not_to_be_confused_with:`.

**Never quote or cite a ruling.** Not its number, not its wording, not the reading it rejected. A
ruling's result is the definition itself; if the entry now says the right thing, the ruling has
already done its work. `rulings:` names the id, and `decisions/NNN-*.md` holds the argument in
the expert's own words. A definition that says "(ruling 012)" is asking the reader to go and
audit the glossary, which is not why they opened it.

**Never name a banned or deprecated word.** "Customer is an AVOID for Guest" is a naming rule,
not a meaning. It goes in the other entry's `also_called:`, marked deprecated.

Each of these has a home, and the home is checkable in a way that a sentence is not:

| The fact | Where it lives |
|---|---|
| This term is confused with that one | `not_to_be_confused_with:` |
| That word is deprecated, or belongs to another term | `also_called:` on the entry that owns it |
| A ruling settled this | `rulings:`, and the file in `decisions/` |
| Only some people can see this | `visibility:` |
| What this thing does to another | `relations:` |

The test: read the definition to somebody who has never seen the glossary. Every clause should
tell them something about the thing in front of them. A clause that only makes sense once you
know the argument is a clause that belongs somewhere else.

## The extra keys, and why each earns its place

Every key in the block exists because the glossary itself needs it. None exists for the picture.

| Key | Why the glossary needs it |
|---|---|
| `category:` | The taxonomy in step 05 is built from it. |
| `core:` | Marks the dependency-ordered core set. See [core-selection.md](core-selection.md). |
| `relations:` | A verb phrase and a wikilink: `"serves [[Table]]"`. Required wherever the definition uses a wikilink with a verb. A relation is a claim about meaning; writing it down is what makes two entries agree. |
| `relation_kinds:` | One fixed kind per line of `relations:`, same length, same order: `[holds]`. A person reads the verb; a script or an agent reads the kind. The 21 kinds and their rules are in [relation-kinds.md](relation-kinds.md). Optional while the glossary grows. |
| `depends_on:` | The terms this definition cannot be written without. Core selection reads it. Not the same claim as `relations:`; see below. |
| `rulings:` | The ids of the rulings in `decisions/` that shaped this entry. The audit trail. |
| `visibility:` | Who can see the thing, when not everybody can: `[host, server]`. Left out when everybody can. |
| `workflow:` | Which sequence of work the term belongs to, and where in it: `["meal 3"]`. Optional. |

Keys stay flat: a scalar, or a list on one line or as `- ` lines. No nesting. Wikilinks inside
list values are quoted: `"[[Table]]"`. A key with no value is left out, not set to null.

**A comma inside an inline list value splits it in two.** `[user (internal only, never shown)]`
parses as two items, not one. Quote the value or drop the comma. Markers are short tags anyway,
like `(deprecated)` or `(internal only)`; a value that wants a comma is usually a sentence, and a
sentence belongs in the definition or in a ruling.

**Quote a code that starts with a zero.** A standard YAML reader takes `062` as a base-8 number
and returns 50, and takes `860` as a number, not text. Write `["062", "860"]`. The render script
reads its own way and hides the problem; any other tool, and any agent, will not.

**An alias names one entry.** Three rules keep a word from pointing two ways:

- An alias may not be another entry's name, not even marked `(deprecated)`. If "supplier" has its
  own entry, it is not also an alias of the entry beside it; say how the two relate in a relation
  or in `not_to_be_confused_with:`.
  The usual reason for such an alias is real: people say one word and mean the other, because
  they came from an organisation that used the words differently, or because in conversation the
  two mean the same while in the product they are different things. That habit is a confusion seen
  in the evidence, which is what `not_to_be_confused_with:` records. Put the other entry there, and
  in a draft say in the prose line where the habit comes from. An agent then reads "people may say
  covers and mean this" from one key, with no second answer for "covers".
- A short word that two entries truly share carries a context tag on each:
  `walk-in (floor)`, `walk-in (kitchen)`.
- An entry never lists its own name as an alias.

### `workflow:` earns its place, and here is the argument

The value is a name and a position: `workflow: ["meal 3"]`. A term in two sequences carries
two items. A term in none carries no key, and that absence is a fact too: nobody has placed it.

This key looks like it exists for the picture, which the rule above forbids. It does not. A
glossary that names a sequence of work has already made the claim; the key only records, per
term, what that claim means. Before the key, a project could hold an entry like "Guest journey:
everything from the booking to the paid check" and no way to check it. The key makes it
checkable: a reviewer reads the sequence in order and says whether it is the work they do.

The test for any new key is that question. Does the glossary already assert the fact somewhere a
reader can misread? Then a key records it. Does the fact exist only because a diagram wants it?
Then it does not go in.

A position is a claim about order, so it is a claim a reviewer can reject. Order the sequence by
what somebody does first, not by what depends on what: `depends_on` already carries dependency,
and the two orders are different. A ticket is defined using an order, and a host seats the
party before either exists.

A workflow never groups anything. `category:` is the only grouping the glossary has, and the
ontology frames every view by it. A workflow is a path across those categories, drawn as a lens
over the picture: it marks who is in the sequence and where, and moves nothing.

### `visibility:` earns its place, and here is the argument

The value is who can see the thing: `visibility: [host, server]`. **The default is
everybody, and the default is written by leaving the key out.** An entry with no `visibility:`
is visible to a guest, a server and a host alike, which is true of almost every term, so almost
every entry stays as it is.

It passes the test above. The glossary already asserts visibility, and before this key it
asserted it inside definitions, as a negative: a draft of [[Turn]] said "never shown to a guest"
and a draft of [[Comp]] said "not printed on the guest's copy". Both facts are real and both
were in the wrong place. A reader looking up Turn wants to know what a turn is. A person building a
screen wants to know who may see it, and wants to query it rather than read a hundred sentences.

List who can see, not who cannot. Two reasons. The rule above says a definition never states what
a thing is not, and a key that inverts it would smuggle the same habit back in. And the positive
list is the one a screen needs: a view asks "may I render this for the person in front of me",
which a list of permitted roles answers directly.

Use the role names the glossary already publishes, in lower case: `guest`, `server`, `host`,
or whatever roles that project's entries define. The key is not a permission model and does not
try to be one. Permissions belong to the product, not to the glossary. This records what the glossary already claims about who sees a word's thing,
so a reviewer can say it is wrong.

### `relations:` and `depends_on:` are two different claims

Both keys hold wikilinks, so they look alike. They are not, and most entries need both.

`depends_on` answers one question: which terms could I not write this definition without? It
points from the definition to the words it borrows.

`relations` answers a different one: what does this definition say this thing does to another
thing? It points from the subject to the object, the way the sentence does.

The two often point opposite ways across one pair. Take Order and Allergy note. [[Allergy note]]
is "a note on an order naming one guest's allergy", so it `depends_on` [[Order]]. Its line
`"is part of [[Order]]"`, kind `part_of`, says the order holds the note. The
containment runs one way and the dependency runs the other. A picture drawn from dependencies
alone draws the product backwards.

**The rule.** Every wikilink the definition uses with a verb becomes one relation. The entry is
the subject. The wikilink is the object. The verb phrase is the one the definition already uses.

**One verb, one object, link last.** A line holds one verb and one wikilink, and ends with it:
`"serves [[Table]]"`, never `"brings a [[Course]] to a [[Table]]"`. Detail such as "while
it is still hot" stays in the definition. A script reads the last link as the object, so a line with
two links, or text after its link, draws to the wrong term or is dropped. A line with two objects
is two lines.

**Each line can carry a kind.** `relation_kinds:` names, at the same position, what sort of fact
the line states: `relations: ["serves [[Table]]"]`, `relation_kinds: [serves]`. The verb stays for
the person; the kind is what a script and an agent read. The list of 21 and how a project adds its
own are in [relation-kinds.md](relation-kinds.md).

**One line per fact, said by the one who acts.** When two entries state the same fact from
opposite sides ("a server serves a table", "a table is served by a server"), the
glossary keeps one line: the active one, on the entry that acts, and from the product's own side
where the product is a party. The other line is removed from `relations:`; the definition may keep
its words. Two lines that say different things are not a mirror, and both stay, even between the
same two entries. A script that needs the reverse direction generates it from the kind; nobody
writes it by hand.

**The evidence.** A relation must be readable in this entry's own definition. If it is not there,
the definition is what is incomplete, and the definition is fixed first. A relation nobody can
find in a definition is a claim, not a fact. A claim belongs in a ruling in `decisions/` or in
the verification queue, never in this key.

**The verbs.** Use one of these where it fits, so a hundred entries read as one document. Where a
line carries a kind, the kind decides its flow and this table is not read; the table is the
fallback for a line with no kind yet.

| Verb | What it means | Flow |
|---|---|---|
| `contains` | the object sits inside the subject, and the subject is the whole | structure |
| `is part of` | the reverse of contains | structure |
| `is a kind of` | the subject is a narrower case of the object. Write `is a` with the kind `is_a` instead; see [Kind of: the is-a test](#kind-of-the-is-a-test) | structure |
| `is made of` | the subject is assembled from many of the object | structure |
| `produces` | doing or finishing the subject creates the object | produces |
| `is produced by` | the reverse of produces | consumes |
| `binds ... to` | the subject joins two other terms, both named in the phrase | produces |
| `is performed by` | the object is the person or role who does the subject | consumes |
| `records` | the subject is the durable trace of the object | produces |
| `is an instance of` | the subject is one concrete occurrence of the reusable object | consumes |
| `reads` | the subject takes the object in and acts on what it says | consumes |

### The flow column, and why a sentence is not enough

A relation is always written subject verb object, because that is the sentence the definition
makes. The picture needs a second fact the sentence does not give: which way the work moves.

"A station reads a ticket" is station to ticket as a sentence and ticket to station as a flow,
because reading takes something in. Drawn from the sentence alone, the edge shows a station
emitting tickets, which is backwards, and the feedback loop the glossary states disappears.

So each verb carries a flow, and the three values are the three kinds of claim the graph holds:

| Flow | Means | Drawn |
|---|---|---|
| `produces` | the subject makes, drives or acts on the object | subject to object, with the sentence |
| `consumes` | the subject takes the object in | object to subject, against the sentence |
| `structure` | containment, kind, requirement. Not a movement at all | no flow; the sentence is the whole claim |

A passive verb is not automatically consuming, and this is where it is easiest to get wrong. The
test is whether the verb's result lands in the subject. "A reservation is made by a host"
consumes, because making it fixes its time and table, so the host's decision flows in. "A course
is inspected by the expo" produces, because inspecting leaves the course unchanged and the expo
is the one taking something in. Both sentences are passive and they point opposite ways.

So passive verbs fall in two families, and the split is worth learning once.

| The agent... | Result lands in | Flow | Examples |
|---|---|---|---|
| brings the subject into being, or fixes its value | the subject | `consumes` | `is set by`, `is created by`, `is granted by`, `is produced by`, `is selected by` |
| takes an existing subject in, and leaves it as it was | the agent | `produces` | `is used by`, `is read by`, `is received by`, `is checked by`, `is watched by` |

The second family is the one that gets miscalled, because the grammar looks identical. "A
ticket is read by a station" gives the ticket to the station; the station does not flow into the
ticket. Read it with the active form beside it and they must agree: "a station reads a ticket"
consumes, so "a ticket is read by a station" produces. **Two entries stating the same link from opposite sides must
draw the same arrow.** When they do not, one of the two verbs is classified wrong, and that is
the cheapest check there is.

This changes nothing about what you write. The claim still lives on the entry whose definition
states it, still reads subject verb object, and `depends_on` is untouched. Only the picture reads
the flow. `tools/render-ontology.py` takes it from the line's kind when there is one, and derives
it from the verb when there is not, printing what it could not place, so a verb it guesses at is
visible rather than silent. A kind removes the guess.

Another verb is fine when the definition uses one this table does not hold. The table is a
default, not a fence.

**A project may classify its own verbs, and that classification wins.** The script holds one
short generic list, and generic means the word means the same in any domain: a passive verb with
an agent takes something in, a containment verb moves nothing. Everything else is a fact about
one product, so it lives with that product's other values, in the `verbs:` block of
`projects/<p>/project.yaml`:

```yaml
verbs:
  consumes:                     # the object flows into the subject; drawn against the sentence
    - verified through
  structure:                    # containment, kind, requirement. Nothing moves
    - priced as a
  produces: []                  # the default. List a verb here only to overrule a generic one
```

An entry is a stem, matched at the start of the verb phrase or as a whole word inside it, with
any wikilink removed first: `is a with no` matches `is a [[Party]] with no`. `produces` is read
before the other two, because it is also the fallback, so a project can overrule a generic
reading it disagrees with.

The reason for the split is a failure worth remembering. The generic list was grown from one
project's vocabulary, and when a second project rendered, nearly all of its verbs fell through to
`produces` and the picture's colours meant nothing. A shared list that carries one product's
words classifies the next product's words by accident.

**A gap entry carries no relations.** A `status: gap` definition is a question, and a question
has no subject to hang a verb on.

## Built version over version

A glossary is not finished in one pass, and the rules above are not a gate it must clear at once.
An early version may hold entries with no kind on their lines, a type nobody has tested yet, or
no relations at all. Each later version fills more in. This is the same shape as the core set:
see "Growth is the expected shape" in [core-selection.md](core-selection.md).

Two things are held apart:

| | Rule | Where it shows |
|---|---|---|
| **Correctness** of what exists | Required. A type that fails its test, a kind that does not fit its line, a mirror line, an alias that names another entry: each is a finding for the next version. | The review of the draft, and `tools/check-glossary.py` |
| **Completeness** of what is there | Reported, never a gate. Lines without a kind, entries with no relation, entries never typed by the tests. | `04-draft/v<N>/coverage.md` |

No step stops because coverage is low. A step stops because something written down is wrong.

## Wikilinks

`[[Term]]` links to the entry whose heading is `Term`. Use them in the YAML lists and in the prose.
A wikilink to a term that has no entry is a gap; the draft lists those at the end under
"Linked, not defined" so a reviewer can decide whether the term needs an entry.

## The cap

A draft holds at most 100 entries (or `targets.draft_entry_cap` in `project.yaml`). Everything
beyond the cap goes in an appendix table with term, type and one-line definition, so nothing is
lost and the reviewer's attention goes to the entries that carry conflict.

## What a script may read

Scripts read the `### ` headings, the YAML blocks, the blockquote that holds the definition, and
the wikilinks inside all three. Nothing else. If a script needs a fact that is only in the rest of
the prose, the fix is to add a key, not to parse the prose.

In the YAML block, that includes `relation_kinds:` beside `relations:`. A script finds the
hierarchy by kind, not by a separate key: the `is_a` and `aspect_of` lines are the parent links,
and the line's object is the parent.

The blockquote is what makes the definition machine-readable as well as readable. Before this
rule the definition was "the first paragraph after the YAML block", which a script could only
find by counting. `tools/render-ontology.py` still accepts that older shape, so drafts written
before the change keep rendering.

---

Related: [relation-kinds.md](relation-kinds.md) · [core-selection.md](core-selection.md) ·
[prose-style.md](prose-style.md) ·
[../steps/04-draft/CONTEXT.md](../steps/04-draft/CONTEXT.md) ·
[../steps/05-glossary/CONTEXT.md](../steps/05-glossary/CONTEXT.md)
