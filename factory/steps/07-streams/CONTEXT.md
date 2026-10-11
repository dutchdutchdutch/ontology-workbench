# Step 07: Streams

Views of how the work runs, keyed to the glossary. Optional, and run on request, but most
projects will want one: the taxonomy says where a term belongs, and these views say how the work
or the value actually travels across it.

Three views, two pages:

| View | What it shows | Where it comes from | Page |
|---|---|---|---|
| Workflow lens | the order somebody touches terms in: "meal" runs from the reservation to the paid check | the `workflow:` key on glossary entries. Step 05 owns it; step 06 already draws it | `value-streams.html`, over the step 06 picture |
| Value stream lens | something of value moving between terms: money, data, food, approvals | a stream file in `07-streams/`, written by a person | `value-streams.html`, over the step 06 picture |
| Process | who does what, in what order: lanes are the people and agents, columns are the steps, boxes are the activities | a process file in `07-streams/`, written by a person | `processes.html`, its own picture |

A workflow lives in the glossary because it is a fact about each term. A value stream and a
process live here because each is a claim about many terms at once, and a hypothesis until
somebody signs it.

A lens is drawn over the step 06 picture, because its unit is the term. A process is not: its
unit is an activity, and the lanes and the order are the point, so it has its own picture. What
ties a process to the vocabulary is that every box names the glossary terms it uses, the page
shows the glossary's own definition for each, and a term with no entry is a finding for step 05.
The audience for a process is a newcomer: it answers "what happens, and who does it" before the
ontology answers "how do the concepts relate".

If a view and the glossary disagree, the glossary wins, and the fix is in step 05.

## Precondition

For a lens: `projects/<p>/06-ontology/ontology-data.js` exists. For a process:
`projects/<p>/05-glossary/glossary.md` exists. And someone asked for the view.

When nobody asked, this step writes `07-streams/skipped.md` with `reason: not requested`
(`tools/render-streams.py <p> --skip "not requested"`). When step 06 has not run, the reason is
`no ontology yet`.

## Inputs

- `projects/<p>/06-ontology/ontology-data.js`: the picture, read as it stands. Step 07 draws the
  same terms under the same numbers at whatever scope step 06 used.
- `projects/<p>/05-glossary/glossary.md`: to check that every term a stream names has an entry.
- `projects/<p>/07-streams/<name>.md`: one file per value stream, or per process. Start from
  `_stream.template.md` or `_process.template.md` in the same folder. A process file is told
  apart by `process:` in its front matter.
- `tools/render-streams.py` and `tools/stream-visualizer.html` for the lenses;
  `tools/render-processes.py` and `tools/process-visualizer.html` for processes.
- [../../rules/evidence.md](../../rules/evidence.md): no quote, no row. It applies to flows too.

Both pages keep their look for people. Each term's panel gains the same closed **Machine detail**
section as the step 06 passport: type, status, aliases, is-a chain, and on the stream page each
relation with its kind and both directions. See "Two lenses" in
[../06-ontology/CONTEXT.md](../06-ontology/CONTEXT.md). The canvas does not change.

## The stream file

One file per stream, named for it: `money.md`, `guest-data.md`. The script reads the sections
below and nothing else, the same way step 06 reads only headings and YAML blocks.

| Section | Required | What it holds |
|---|---|---|
| front matter | yes | `stream:`, `drafted_by:`, `drafted:`, and `reviewed:`, which holds `none` until a named reviewer has read every flow, then the date. `reviewed_by:` lists who |
| `## The stream in one line` | yes | the whole stream in one sentence, for the reader who stops there |
| `## Flows` | yes, unless `## Base` | one `### ` heading per flow, a one-line blockquote, and a YAML block |
| `## Roles` | yes, unless `## Base` | one YAML block: each role and the terms that hold it |
| `## Trace` | no | which flow keys stay lit when the lens is on. Default: every key that names a term |
| `## Base` | no | `extends: <stream>` and `label:`. The file adds to another stream instead of repeating it |
| `## Reach` | no | terms one stated relation away from the stream, such as an approval or a submission |
| `## Findings for step 05` | yes | terms the stream needs that have no entry, or entries that say too little. Say "none" when empty |
| `## Open questions` | no | what the reviewer must answer before signing |

A flow's YAML block:

| Key | Required | Means |
|---|---|---|
| `from` | yes | where the value starts. A wikilink: `"[[Party]]"` |
| `to` | yes | where it lands. An empty string is a finding: the value goes somewhere the glossary never names |
| `kind` | yes | what moves, in plain words: `payment`, `tip`, `order` |
| `via`, `trigger`, `rate`, `timing`, `gate`, `approved_by`, `bypasses` | no | the term that carries, starts, sizes, times, holds, approves or routes around the flow. A bare word is a literal and is not checked: `rate: statutory` |
| `confidence` | yes | `stated` (one entry says it), `inferred` (two entries together imply it), `assumed` (a guess, so the row is a question) |
| `evidence` | yes | the glossary sentences the flow comes from, verbatim. A flow with no evidence is reported and is not a row yet |
| `note` | no | anything the reviewer needs. Start it with `FINDING.` when it is one |

The stream page follows the step 06 page rules ("How the page reads, for people" in
[../06-ontology/CONTEXT.md](../06-ontology/CONTEXT.md)), with two of its own: at rest it shows no
lines unless a value stream is chosen, and the value-stream menu leads the top bar in gold. A lit
stream takes the same gold for every role money moves through or that sets its amount or timing;
funders are green, approvers orange, gates pink, leaks red with a mark, the repair teal.

The roles, in the order value meets them: `funder`, `approver`, `gate`, `claim`, `conduit`, `unit`,
`meter`, `clock`, `trigger`, `earner`, `leak`, `repair`. The words came from money, and they hold
for any value: data has a funder that supplies it, a gate and an earner that gets it in return
for work. A value stream is an exchange, so the two ends are named by what they do: a funder pays
for the value, an earner is paid for delivering it. Any other role is reported as a typo. The
template says what each one means.

## The process file

One file per process, named for it: `order-to-table.md`. The script reads the front matter,
the sections below, and inside `## Boxes` the headings, blockquotes and YAML blocks, plus the
prose after each block. Nothing else.

| Section | Required | What it holds |
|---|---|---|
| front matter | yes | `process:`, `title:`, `drafted_by:`, `drafted:`, `source:`, and `reviewed:`, which holds `none` until a named reviewer has read every box, then the date. `reviewed_by:` lists who. Optional: `cadence:` (weekly, daily, per intake), accented in the title when the title says it; `target:`, a one-line goal the process serves, shown in the panel |
| `## In one line` | yes | the whole process in one sentence, shown under the title |
| `## Lanes` | yes | one YAML block, one lane per line: `id: { label, who, kind }`. `kind` is `people`, `ai` or `team` and sets the colour |
| `## Steps` | yes | one YAML block: `steps: [..]`, the columns in order |
| `## Paths` | no | the same process at rising levels of trouble, one `### ` heading per path: a one-line blockquote saying when the week looks like this, a YAML block with `id`, `share` (how often, as the author estimates it) and `boxes` (the ids on this path), and prose for the sidebar. Paths nest: the common path holds the happy path. The page fades every box outside the chosen path and walks only its steps |
| `## Boxes` | yes | one `### ` heading per box: the card title. A one-line blockquote: the card text. A YAML block: `id`, `step`, `lane`, `terms` (wikilinks), `next` (main flow), `when_needed` (dashed), `human_moment: true`, and `tag` for the party acting when a lane holds more than one ("Host" in the floor lane). The prose after the block is the longer explanation the page shows in its sidebar |
| `## Working names` | no | words in the boxes with no glossary entry, and why they are not linked |
| `## Findings for step 05` | yes | terms the process needs that have no entry, or entries that say too little. Say "none" when empty |
| `## Open questions` | no | what the reviewer must answer before signing |

An edge is a box id, or `{ to: <id>, label: "<chip>" }` when the arrow carries a label such as
"Needs a person". `next` is drawn solid, `when_needed` dashed. A box with no `terms` is allowed
and is reported, because a box that names no term is not tied to the vocabulary.

## Process

### A process

1. **Pick the process.** Ask what a newcomer must understand in their first week: the thing that
   repeats. A weekly cycle, an intake, a close. One process per file.
2. **Draft it.** The source is usually a diagram or a brief the team already has; name it in
   `source:`. Link every glossary term a box uses. Do not invent an entry for a word that has
   none: keep it as a plain word and list it under `## Working names` with what it is today.
3. **Render.** Run `tools/render-processes.py <p>`. It writes `07-streams/process-data.js` with
   every box, every edge and the glossary definition of every term named, and copies the page
   next to it as `processes.html`. Several process files render into the one page.
4. **Read the report.** Boxes, steps, lanes, edges, each path's share of the boxes; every term
   with no glossary entry, which is a finding for step 05; every box whose lane, step or edge
   target does not exist, every path that names a box that does not exist, and every box that
   names no term.
5. **Send findings on.** Each missing or thin entry goes to `decisions/` or a step 05 edit. Never
   fix the glossary from here.

### A value stream

1. **Pick the stream.** Ask what value the product exists to move: money for a services business,
   data or results for a measurement product. One stream per file. A stream that only exists to
   add reach to another one uses `## Base`.
2. **Draft it from the glossary.** Claude or a person writes the file from `05-glossary/glossary.md`
   alone. Every flow quotes the entries it comes from. Mark each `confidence` honestly: a stream
   full of `assumed` rows is a list of questions, and that is a useful thing to hand a reviewer.
3. **Render.** Run `tools/render-streams.py <p>`. It copies step 06's picture unchanged, adds the
   stream edges, writes `07-streams/stream-data.js`, and copies the page next to it as
   `value-streams.html`. The workflow lens from step 06 is on the same page.
4. **Read the report.** It prints, for each stream:
   - the flows by confidence, naming every one that is not `stated`;
   - every term named by a stream with no glossary entry. That is a finding for step 05;
   - every term the stream names that the step 06 picture does not draw. Either re-render step 06
     at a wider scope, or the stream reaches past the core;
   - every term one hop from the stream that the stream leaves out. Each is a question: does it
     carry value too, or is the edge of the stream right here?
   Fix the file and render again until the report holds only the findings you mean to keep.
5. **Send findings on.** Each missing or thin entry goes to `decisions/` or a step 05 edit. Never
   fix the glossary from here.

Rules:

- A process never defines a term. The sidebar shows the glossary's definition, read at render
  time. A process file that needs its own definition is asking for a step 05 entry.
- A lens is never a layout. Nothing on the canvas moves when a lens changes. A stream that needs
  its own layout is asking to be a category, and that is a step 05 question.
- A stream edge is not a relation and does not pretend to be one. Money often runs against the
  sentence a definition makes, which is why the page draws it apart.
- Never hand-edit a generated file: `stream-data.js`, `value-streams.html`, `process-data.js`,
  `processes.html`. Regenerate after any change to an authored file, to step 05 or to step 06.
- Never add a project's role or flow key to the script. If a stream needs a new one, it is a
  factory change, made for every project, with a note in `DESIGN-NOTES.md`.

## Outputs

In `projects/<p>/07-streams/`:

| File | Required | What it is |
|---|---|---|
| `<name>.md` | one per stream or process | Authored by a person. A hypothesis until `reviewed:` holds a date. A process file has `process:` in its front matter. |
| `stream-data.js` | with a stream | Step 06's picture plus every stream, generated. |
| `value-streams.html` | with a stream | The lens page, next to its data. Open it in a browser. |
| `process-data.js` | with a process | Every process, with the glossary definition of every term it names, generated. |
| `processes.html` | with a process | The process page. One toolbar: process, path, steps All / None, and the walk (Play, Prev, Next). The step numbers in the column headers are the step navigation; an eye on each hides it. The sidebar holds the longer explanation and the glossary's definitions, next to the picture. |
| `skipped.md` | when not run | `reason:` and the date. |

## Human checkpoint

A named reviewer, usually the person who owns that value in the business, reads every flow aloud
as a sentence: "the party pays the check through the card reader". A false
sentence is a finding. The reviewer answers the open questions, then fills `reviewed:` with the
date and adds their name to `reviewed_by:`.

For a process, the reviewer reads every box aloud as "<lane> <does this> at step N", and checks
the sidebar explanation says nothing the glossary contradicts. Same signature, same line.

Step 08 publishes a page only when every file behind it is signed.

## Status signal

Step 07 is done when each page that has files behind it is newer than those files (and than
`06-ontology/ontology-data.js` for the lens page, `05-glossary/glossary.md` for the process page),
and every authored file has a `reviewed:` date. `tools/status.sh` prints streams and processes
on separate rows. A `skipped.md` means considered, not rendered.

## Next

[../08-publish/CONTEXT.md](../08-publish/CONTEXT.md), once the glossary is at `trial`.

## Back to

[../../../CLAUDE.md](../../../CLAUDE.md)
