# Step 06: Ontology visualisation

Render the relationships the glossary already holds as a picture people can click through. A
display for explanation and comprehension, never a source. Runs on request, or when the term
graph is too large to hold in the head.

If the picture and the glossary disagree, the glossary wins, and the fix is in step 05.

## Precondition

`projects/<p>/05-glossary/glossary.md` exists, and someone asked for the picture.

When it is not asked for, this step writes `06-ontology/skipped.md` with `reason: not requested`
so the audit trail shows it was considered. When step 05 has not run, it writes `skipped.md` with
`reason: no glossary yet`.

## Inputs

- `projects/<p>/05-glossary/glossary.md`: the headings and the YAML blocks only.
- `tools/ontology-visualizer.html`: the renderer page.
- `tools/render-ontology.py`: the script.
- `projects/<p>/project.yaml`: the `relation_kinds:` block, this project's extra kinds; the
  `verbs:` block, this project's own verb flows; and the `ontology:` block, how the category
  frames are placed.
- `projects/<p>/04-draft/v<N>/verification-queue.md`, for the version named in the glossary's
  `published_from:`: the open question-pack items, which the machine file carries as unconfirmed.
  Nothing else is read from it.
- [../../rules/entry-format.md](../../rules/entry-format.md): what the script may read.
- [../../rules/relation-kinds.md](../../rules/relation-kinds.md): the kinds, their inverses and
  flows.

## Scope: three views, one path

**Every view is framed by `category:`.** The taxonomy step 05 publishes is the one grouping the
picture uses. A scope narrows which nodes are drawn; none of them regroups the nodes.

| Command | Draws | Framed by |
|---|---|---|
| `tools/render-ontology.py <p>` | every entry | `category:` |
| `tools/render-ontology.py <p> --core` | the entries marked `core: true` | `category:` |
| `tools/render-ontology.py <p> --workflows` | the entries with a `workflow:` key | `category:` |
| `tools/render-ontology.py <p> --relations-only` | drops the dependency edges from any of the above | unchanged |

`--core` is the default picture for people: the core set framed by category, which is the same
grouping as `05-glossary/taxonomy.md` and the same terms as `05-glossary/core-terms.md`.

Pick by the question. `--core` answers "what are the words I have to learn". The full render
answers questions about the whole vocabulary, such as finding a term with no edges at all.
`--workflows` narrows to the terms somebody has placed in a sequence, still in their categories.

"How does the work actually run" is not a scope. It is the **workflow lens**, a control on the
page that works on any of them. The lens marks which nodes are in one sequence and numbers each
by its position, and it moves nothing: a workflow is a path across the taxonomy, not a rival to
it. `meta.workflows` carries each sequence in order and every node carries its own positions, so
a term in two sequences is marked correctly in each.

Prefer a narrow view when the picture is for people. A hundred nodes is a diagram nobody reads.

Every scope is a filter on one key the glossary already holds. None invents a node, an edge or a
definition, and none changes one. The scope goes into `ontology-data.js` as `meta.scope` and
appears under the title, so a reader always knows whether they see all of the glossary or part of
it. One picture at one path: a second scope overwrites the first, and re-rendering costs one
command.

A narrow view cuts edges as well as nodes. An edge whose target the scope left out is counted in
`meta.outOfScope`, never in `meta.unresolved`. The two mean different things: out of scope means
the term has an entry and is not drawn here, unresolved means no entry exists anywhere, which is
a finding for step 05.

## Process

Run `tools/render-ontology.py <p>` from the workspace root, with `--core` when the picture is for
people. It:

1. Splits `glossary.md` on `### ` headings; each heading is a node. With `--core`, keeps only the
   nodes whose block says `core: true`; with `--workflows`, only those with a `workflow:` key.
2. Reads each entry's YAML block: `category` becomes the domain frame, `relations` become labelled
   edges, `depends_on` becomes "depends on" edges where no relation already links the pair,
   `core` marks the node. The two kinds of edge are drawn apart: a relation is a solid line with
   its verb, a dependency is dashed and muted. A reader sees at a glance how much of the picture
   is stated meaning and how much is fallback.
   Each relation also carries a flow: `produces`, `consumes` or `structure`. The flow comes
   from the line's kind in `relation_kinds:` when it has one, and is derived from its verb when
   it does not. A relation is written subject verb object because that is the sentence the
   definition makes, and a consuming verb runs against it: "a station reads a ticket" is station
   to ticket as a sentence and ticket to station as a flow. The page groups the passport by flow,
   colours a selection by flow (cyan consuming, pink producing, slate structural) and animates a
   consuming edge backwards, so a feedback loop reads as one. Colouring from the arrow instead
   would paint a consuming edge as producing, which is the one thing it is not. A structural edge
   is highlighted without animating, because containment is not a movement.
   [../../rules/entry-format.md](../../rules/entry-format.md) holds the verb table and the three
   values. The script prints how many verbs fell in each, and lists the ones it read as producing,
   so a wrong guess is visible.
   Verbs come from two places: one short generic list in the script, and the project's own in the
   `verbs:` block of `projects/<p>/project.yaml`, which wins. A first render is expected to read
   too much as producing, because `produces` is the fallback; the printed list is the worklist,
   and the fix is a kind on the line, or a stem in `project.yaml`.
   The script also warns about every relation line it cannot read: no link, or text after the
   link. A line it cannot read is dropped from the picture, and the warning is the only trace.
3. Lays the nodes out by category. Every scope does this. The frames start in the order the
   categories appear in the glossary, the reading order from step 05. That order is a starting
   point, not a rule for the picture: a project may set `ontology: layout: shortest` in
   `project.yaml`, and the script moves whole frames to make the lines shortest in total, keeping
   the reading order on a tie. `ontology: pin_left:` fixes named frames at the left first, in the
   order given, and the search places the rest. Or it may name `ontology: frame_order:` by hand,
   which wins: one item per column, and an item `A + B` stacks frame B under frame A in that
   column. The page grows its canvas to fit whatever the layout needs. Only
   frames move: a node keeps its row and its category's colour, and no node, edge or category
   changes. The script prints both total lengths, and `meta.layout` records the order used, so the
   page can say the frames were moved. `workflow:` rides along as data on each node and in
   `meta.workflows`, for the lens; it never sets the layout.
4. Writes `06-ontology/ontology-data.js` and copies the renderer next to it as `ontology.html`.
5. Writes `06-ontology/ontology-machine.json`, the machine lens. See below.

## Two lenses: one for people, one for machines

A person and an agent need different things from the same glossary, so the step writes two views
of it. Neither is a source; both are regenerated, never edited.

| | The page, for people | `ontology-machine.json`, for agents |
|---|---|---|
| Terms | the scope chosen | every entry, whatever the scope |
| Lines | one direction, as written, labelled with the verb | both directions: the written line, and its reverse built from the kind's inverse, marked `generated` |
| Each term carries | category, definition, edges | also type, status, core, aliases, not-to-be-confused-with, the is-a parent, rulings |
| Open questions | left out | each open question-pack relation, marked `unconfirmed`, so an agent says "not yet confirmed" instead of guessing |
| Coverage | not shown | the counts from `coverage.md` |

The page stays as it is. Its side panel (the passport) gains one collapsible section, **Machine
detail**, closed by default: the term's type, status, aliases, not-to-be-confused-with, its is-a
chain, and each relation with its kind and both directions, generated ones marked. It shows a
person exactly what an agent reads about the term, so a wrong kind is caught by eye. Nothing on
the canvas changes: a generated reverse line is never drawn.

**The canvas is for overview, and stays as simple as the glossary allows.** One line per written
relation, one direction, one label: the verb. Never on the canvas: the kind, the reverse line, an
unconfirmed question-pack line, or any second label. All of those live in the panel, under the
term they belong to. The same holds for the step 07 and 08 pages.

**How the page reads, for people.** These rules are in `tools/ontology-visualizer.html` and
`tools/stream-visualizer.html`, so every project gets them at its next render. Decision log 48.

| Rule | Why |
|---|---|
| At rest, with nothing selected, the canvas shows the frames and the terms and no lines. Selecting a term brings back its own lines. | A hundred lines and labels read as noise, and every one of them is in the passport once a term is selected. |
| The key is a set of switches: consuming, producing, structure. Consuming and producing start on; structure starts off and also hides the depends-on fallbacks. A project may start structure on with `ontology: show_structure: true` in its `project.yaml`. | People read what moves first and containment after. Structure lines cross the flow lines. A glossary whose lines are mostly containment and kind, where the structure is the point, reads better with them on. |
| The passport names both terms in every line: "Server serves Table", never "serves this". It always lists all three groups, whatever the switches say. | A reader should not have to resolve a pronoun to learn which term is which. |
| Every label on the page meets 7:1 contrast: line labels at 11px, a fallback shown by italics and a dashed border, never by fading. | Apple's human interface guidelines ask 4.5:1 at least and 7:1 for small text. A faded label had fallen to 2:1. |
| One top bar: reset and a one-line instruction, then every control in one shape with a small label, then the key. | The controls read as one set; the main control can be told apart. |

Rules:

- The script reads headings, YAML blocks and the wikilinks inside them. Nothing else. If it needs
  a fact that is only in prose, step 05 did its job wrong: add a key there, do not parse here.
- The script never asks for a field or an edge the glossary does not need on its own. A term with
  no relations renders as a node with no edges; that is information, not a defect.
- The script reports every entry whose definition links a term with no relation for it. That is a
  finding for step 05, not an error here. A picture made mostly of dashed lines means step 05 left
  the verbs in the prose.
- Never hand-edit `ontology-data.js` or `ontology.html`. Regenerate after any change to step 05.
  A hand edit is a fact that lives in the picture and not in the glossary.
- Never add a project's verb to the script. The generic list holds only words that mean the same
  in any domain; everything else goes in that project's `verbs:` block. A shared list carrying one
  product's vocabulary classifies the next product's by accident.

## Outputs

In `projects/<p>/06-ontology/`:

| File | Required | What it is |
|---|---|---|
| `ontology-data.js` | yes | Nodes, domain frames and edges, generated from the glossary. `meta.scope` says `all` or `core`. |
| `ontology.html` | yes | The renderer, next to its data. Open it in a browser. Self-contained apart from fonts. |
| `ontology-machine.json` | yes | The machine lens: every entry, its kinds, both directions, open questions marked unconfirmed. A view, never a source. |
| `skipped.md` | when not run | `reason:` and the date. |

## Human checkpoint

None for the picture itself. When a reader of the picture spots a wrong edge, the finding goes to
`decisions/` or to a step 05 edit, and the picture is regenerated. Nobody fixes the picture.

## Status signal

Step 06 is done when `projects/<p>/06-ontology/ontology.html` exists and is newer than
`05-glossary/glossary.md`. A `skipped.md` means considered, not rendered.

## Next

[../07-streams/CONTEXT.md](../07-streams/CONTEXT.md), when someone wants a value stream laid over
the picture. Otherwise [../08-publish/CONTEXT.md](../08-publish/CONTEXT.md), once the glossary is
at `trial`.

## Back to

[../../../CLAUDE.md](../../../CLAUDE.md)
