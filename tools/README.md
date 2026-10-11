# tools

Eight scripts and five pages. Bash and Python standard library only; nothing to install. Run every
script from the workspace root.

| File | What it does | Reads | Writes |
|---|---|---|---|
| `new-project.sh <name>` | Copies [../_templates/project/](../_templates/project/) to `projects/<name>/`, refuses if it exists, puts the name and today's date into `project.yaml` and the README files. | the template | `projects/<name>/` |
| `status.sh <name>` | Prints the step table for one project by checking which files exist, plus the highest draft version, the ruling count, and what to do next. The table in [../CLAUDE.md](../CLAUDE.md) is its specification. | the filesystem | nothing. This is the generated index. |
| `render-ontology.py <name>` | Reads the `### ` headings, YAML blocks and definitions of `05-glossary/glossary.md`, writes `06-ontology/ontology-data.js`, and copies the renderer next to it as `ontology.html`. Every view is framed by `category:`, the taxonomy step 05 publishes. With `--core` draws only the terms marked `core: true`, which is the default picture for people; with `--workflows` draws only the terms carrying a `workflow:` key, still framed by category. A workflow is a lens on the page, not a grouping. With `--relations-only` drops the depends-on fallback edges. The frames run in the glossary's category order unless the project's `ontology:` block says `layout: shortest`, which moves whole frames to make the lines shortest in total (`pin_left:` fixes named frames at the left first), or names a `frame_order:`, one item per column, where `A + B` stacks B under A. With `--skip "<why>"` writes `06-ontology/skipped.md` instead. It prints how many edges are stated relations and how many are fallbacks, names every definition that links a term it states no relation for, and names every relation line it cannot read as written (no link, text after the link, two links). Every render also writes `06-ontology/ontology-machine.json`, the lens for agents: every entry whatever the scope, each line with its kind, the reverse of each kinded line marked generated, and open question-pack relations from the draft's verification queue marked unconfirmed. | step 05 output, the draft's `verification-queue.md` | step 06 output |
| `ontology-visualizer.html` | The renderer page. Loads `./ontology-data.js` from its own folder. Holds no project data. The passport ends in a folded "Machine detail" section: what an agent reads about the term, both directions of each relation. The canvas never shows it. At rest the canvas shows no lines; selecting a term shows its own. The key's three chips switch consuming, producing and structure lines (structure off by default; a project turns it on with `ontology: show_structure: true`, which reaches the page as `meta.linesOn`). See "How the page reads, for people" in `factory/steps/06-ontology/CONTEXT.md`. Open the copy in `projects/<name>/06-ontology/`, not this one. | `ontology-data.js` | nothing |
| `render-streams.py <name>` | Step 07. Copies the step 06 picture from `06-ontology/ontology-data.js` unchanged, adds the value streams authored in `07-streams/<stream>.md`, writes `07-streams/stream-data.js`, and copies the page next to it as `value-streams.html`. Imports `render-ontology.py`, so the two pictures cannot drift apart. Prints each stream's flows by confidence, the terms it names with no entry, the terms the step 06 picture does not draw, and the terms one hop from the stream. With `--stream <s>` reports only that stream; with `--skip "<why>"` writes `07-streams/skipped.md`. | step 05 and 06 output, stream files | step 07 output |
| `stream-visualizer.html` | The step 07 page: the step 06 picture with a value-stream lens and the workflow lens. Open the copy in `projects/<name>/07-streams/`. | `stream-data.js` | nothing |
| `render-processes.py <name>` | Step 07, the other kind of file. Reads every `07-streams/*.md` whose front matter holds `process:`, checks every `[[term]]` a box names against `05-glossary/glossary.md`, every lane, step and edge target against the file, and writes `07-streams/process-data.js` with the boxes, the edges and the glossary definition of every term named; copies the page next to it as `processes.html`. Prints the unresolved terms, a finding for step 05. Not drawn over the step 06 picture: an activity is not a term. | step 05 output, process files | step 07 output |
| `process-visualizer.html` | The process page: lanes by steps, boxes as activities, a panel to pick steps and lanes, a step-by-step walk (Play, arrow keys, `#step-N`), and a sidebar with each box's longer explanation and the glossary's definition of each term it uses. Open the copy in `projects/<name>/07-streams/`. | `process-data.js` | nothing |
| `build-review.py <name>` | A review package before `trial`: `08-publish/review/` with `index.html`, the key terms (the core set, read from `05-glossary/glossary.md`), and copies of the ontology, value-stream and process pages, each with a link back to the index; plus `08-publish/<name>-review.zip`. Stops if a picture is older than its source. No stage gate, no log row. | step 05, 06 and 07 output | `08-publish/review/` |
| `glossary-visualizer.html` | The key-terms page of a review package: core entries by category, a category index, search, links between core terms. | `glossary-data.js` | nothing |
| `review-index.html` | The landing page of a review package: four doors, a question each, a 15-minute path, where to send corrections. | `review-data.js` | nothing |
| `stage-publish.py <name>` | Step 08. Refuses unless the glossary is at `trial` or `adopted` and every listed picture is fresh. Copies the files named in the `publish:` block of `project.yaml` into `08-publish/outbox/`, each with a "do not edit" note, writes a README with every file's hash, and adds one staged row per destination to `08-publish/publish-log.md`. `--sent <dest> "<receipt>"` marks a row sent; `--verify <dest> <folder>` compares a downloaded copy with the last send and names the files edited there. `files:` may name `processes` as well as `streams`, and `ontology-machine` for agents. | step 05, 06 and 07 output | step 08 output |
| `check-glossary.py <name>` | Checks a glossary against the entry rules. Errors, a rule broken (exit 1): a type not one of the twelve, an unknown kind, `relation_kinds:` the wrong length, a line that is not one verb and one object with the link last, an alias that is another entry's name or its own, a shared alias with no context tag, a comma-split alias, an unquoted leading-zero code, an `is_a` cycle. Warnings, findings: an `is_a` parent with one child or more than twelve, a child typed unlike its parent, mirror pairs, `depends_on` loops. Coverage, never an error: lines with a kind, stand-alone entries, entries by type. `--file <path>` checks a draft; `--coverage <out.md>` writes step 04's `coverage.md`. | a glossary | nothing, or `coverage.md` |

Rules:

- No script touches the network. Steps 00 and 08 are the network steps, and both are done by Claude
  through the connected servers, not by a script.
- No script writes a status file. Status is read from what exists. `08-publish/publish-log.md` is
  not one: it records a send, which happens outside the workspace and leaves no file here to read.
- `render-ontology.py` reads headings, YAML blocks and the quoted definition. If it ever needs
  to read other prose, step 05 did its job wrong: add a key to the entry format instead.
- The picture has one grouping and it is `category:`. A workflow is a path across those groups,
  shown by the page's lens, which marks the members of one sequence and numbers them in order.
  Nothing on the canvas moves when the lens changes.
- Each relation carries a flow: `produces`, `consumes` or `structure`. A line with a kind
  (`relation_kinds:`, [../factory/rules/relation-kinds.md](../factory/rules/relation-kinds.md))
  takes the kind's flow; a line without one has its flow read off its verb. The
  sentence runs subject to object; the flow may run the other way, because a consuming verb takes
  the object in. The page groups the passport by flow, so a feedback loop reads as one.
- The verbs are read from two places. `render-ontology.py` holds one short generic list, of words
  that mean the same in any domain. Each project holds its own in the `verbs:` block of
  `projects/<name>/project.yaml`, and those win. Never add a project's word to the script: a
  shared list carrying one product's vocabulary classifies the next product's by accident: one
  early render read nearly every verb as producing.
- An edge is a stated relation, drawn solid with the verb the definition uses, or a depends-on
  fallback, drawn dashed and muted and hideable from the page. A picture that is mostly dashed
  means the verbs are still sitting in the prose; the fix is in step 05, never here.

Back to [../CLAUDE.md](../CLAUDE.md).
