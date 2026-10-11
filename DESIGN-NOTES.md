# Design notes

Why the workspace looks the way it does. One note per decision: what was decided, and why. Read
this before changing a rule in `factory/`. When you make a new decision, add a note at the end of
the section it belongs to.

Examples use the worked example in [projects/bistro/](projects/bistro/).

---

## The workspace

1. **The method and the work live apart.** `factory/` holds the rules and one contract per step.
   `projects/<name>/` holds the work. `CLAUDE.md` only routes. *Why:* an agent reads the one
   contract it needs, and a project can never quietly change the method.
2. **Steps are numbered folders, `00-sources` to `08-publish`, in the factory and in every
   project.** *Why:* the same number means the same step everywhere, and a folder listing reads in
   pipeline order.
3. **Each step has one contract, `factory/steps/<step>/CONTEXT.md`.** Project folders hold a short
   README that links to it. *Why:* one master copy of each rule. Copies drift.
4. **The step folder is the output.** There is no `output/` subfolder. *Why:* one less level, and
   the file that marks a step done sits where you look for it.
5. **Status is the filesystem.** A step is done when its output file exists. `tools/status.sh`
   reads the files; nobody keeps a status field. *Why:* a status someone has to update is a status
   that goes stale.
6. **A step that is considered and passed over writes `skipped.md` with a `reason:` line.**
   *Why:* an empty folder cannot say whether the step was skipped or forgotten.
7. **Every project value lives in `projects/<name>/project.yaml`.** No script and no rule holds a
   product's words. *Why:* a shared tool that carries one product's vocabulary misreads the next
   product's.
8. **Tools are bash and the Python standard library.** Nothing to install. *Why:* the people who
   run this are not all engineers.
9. **The project template sits at the same depth as a project.** *Why:* its relative links work
   before and after `tools/new-project.sh` copies it.
10. **Nothing is deleted.** Superseded project files move to the project's `_archive/`, named
    with the version they came from. *Why:* the audit trail is part of the product.

## Sources and evidence

11. **Step 00 is the only step that reads the network, and step 08 the only one that sends.**
    Every other step reads files. *Why:* re-running a step costs a minute, not another crawl, and
    nothing changes underneath a review.
12. **The `code` source is git metadata: pull request titles and branch names.** Never source
    files. *Why:* the names engineers give their work are the proxy for their words, at a fraction
    of the reading. The bistro's "kitchen_order" came from a PR title.
13. **No quote, no row.** Every inventory row carries a verbatim quote with a title and a link.
    *Why:* a definition built on a paraphrase cannot be checked.
14. **A source the pipeline cannot reach is inventoried by a person**, with one prompt per source
    type in `factory/steps/01-terms/prompts/`. The rows still need quotes and links. *Why:* some
    tools allow no connector, and their words still count.
15. **Step 01 keeps a term only when two or more audiences share it.** The rest go under "Out of
    scope", with their quotes, never deleted. *Why:* a glossary of everyone's private jargon is too
    long to agree on. The bistro's "bookings table" is engineering's alone.
16. **The step 01 review lists what is missing; it never deletes.** It is signed with a date and a
    name, and step 02 does not run until it is. *Why:* the signature separates "I read these" from
    "nobody has looked". The bistro's review brought "turn" back from "Out of scope".
17. **Step 02 decides the suspect flags. Step 03 copies them.** *Why:* one place where a flag can
    change, so a wrong flag has one place to be fixed.

## Drafts and rulings

18. **One file per draft version, `04-draft/v<N>/glossary.md`.** Each entry carries a fenced YAML
    block. Older versions are never edited. *Why:* a hundred term files are unmanageable; git
    already tracks change per entry.
19. **Rulings are inputs, one file each, in the expert's own words.** Step 04 replays every one
    before it writes a draft, and stops if the evidence would contradict one. *Why:* a ruling that
    lives only in a meeting is lost on the next run.
20. **The glossary is built version over version.** Correctness is required; completeness is
    reported in `coverage.md` and never blocks. *Why:* a rule that stops work is worse than a rule
    that speaks up.
21. **Question packs are guesses, and never block.** Stand-alone terms get draft relations for an
    expert to confirm. *Why:* they speed up a conversation without pretending to be meaning.

## The entry

22. **A published entry is the term, a quoted definition and a YAML block.** The evidence stays in
    the draft. *Why:* a reader needs the word, not the argument.
23. **A definition says what a thing is.** Never what it is not, never a ruling number, never a
    naming rule. Those go in keys: `not_to_be_confused_with`, `rulings`, `also_called`,
    `visibility`. *Why:* every clause of a definition should tell a stranger something about the
    thing in front of them.
24. **Twelve types, each with a test: "A [term] is a [type]."** *Why:* a type with no test becomes
    a catch-all.
25. **An alias names one entry.** It is never another entry's name; a word two entries share
    carries a context tag on each. *Why:* an agent asked what "walk-in" means must get one answer
    per sense. See the bistro's two walk-ins.
26. **`relations:` and `depends_on:` are different claims.** A relation is what the thing does to
    another thing; a dependency is a word the definition borrows. *Why:* a picture drawn from
    dependencies alone draws the product backwards.
27. **One verb, one object, link last.** *Why:* a script reads the last link as the object.
28. **Twenty-one relation kinds, each with an inverse and a flow.** A project adds its own in
    `project.yaml`. *Why:* a script or an agent cannot answer "who pays whom?" from a hundred
    different verbs.
29. **One line per fact, on the entry that acts.** The reverse is generated. *Why:* two lines for
    one fact drift apart.
30. **Every relation has a flow: produces, consumes or structure.** A passive verb is tested by
    where its result lands. *Why:* "a station reads a ticket" runs station to ticket as a sentence
    and ticket to station as work.

## The core and the published glossary

31. **The core is chosen by dependency, never by frequency.** *Why:* a word everyone says that
    nothing rests on is common vocabulary, not a foundation.
32. **The core size is a review trigger, not a cap.** It grows round over round, with a warning
    past about 55. *Why:* past that size nobody holds it in their head.
33. **Categories read in a fixed order: people, then the value stream, then alphabetical, then
    anything the product does not act on.** *Why:* a reader cannot hold a definition before they
    know who is involved.
34. **The stage (`review`, `trial`, `adopted`) is a header field in the one published file.**
    Trial closes with a feedback table. *Why:* every reader depends on one file at one path; a
    second copy would be a second product.
35. **`core-terms.md` holds definitions only; `about-core-terms.md` holds the argument.** *Why:*
    a file that explains itself before its first definition is not the file a team keeps open.

## The pictures and sending

36. **The glossary is the product. The ontology is a view of it.** When they disagree, the
    glossary wins, and a fix goes in step 05, never in the picture.
37. **`category:` is the only grouping. A workflow is a lens laid over it.** Nothing on the canvas
    moves when the lens changes. *Why:* two groupings on one canvas make every position ambiguous.
38. **Step 06 writes two outputs: a page for people and `ontology-machine.json` for agents.**
    *Why:* an agent should read meaning from data, not from a picture.
39. **The picture has fixed reading rules.** At rest it shows no lines; structure lines start off;
    every label meets 7:1 contrast. A project may start structure on with
    `ontology: show_structure: true`. *Why:* a hundred lines at once read as noise.
40. **Streams and processes are hypotheses until a named reviewer signs them** (step 07). *Why:*
    a value stream nobody owns is a guess with a nice picture.
41. **A value stream's ends are a funder and an earner, and a role name never matches a term
    name.** *Why:* "who pays" and "who gets paid" are the questions people ask first.
42. **Step 08 sends copies, never the working files.** Only at `trial` or `adopted`, through a
    staged outbox and a log, with a "do not edit" note on every copy and a freshness check on every
    picture. *Why:* people read the copy where they work, and a copy edited out there must be
    caught, not trusted.
43. **A review package can go out before trial.** `tools/build-review.py` bundles the key terms
    and the pictures into one folder and a zip. *Why:* leadership reviews a page, not a repository.

## Meaning changes made by an agent

44. **An agent that changes a meaning says so.** When it hands work back, it lists every change to
    a definition, a type, a relation or the core set, so the lead can approve or reverse each one.
    Wording-only edits need no list. *Why:*
    an agent is confident about domains it does not know, which is the problem this workspace
    exists to solve.

## Credits

The layout borrows from ICM, the Interpretable Context Methodology
([github.com/RinDig/icm-architect](https://github.com/RinDig/icm-architect)): one folder per job,
numbers that encode order, a small file that routes, explicit folder contracts, the factory kept
apart from the product, the filesystem as the state, and new work made by copying a template.
