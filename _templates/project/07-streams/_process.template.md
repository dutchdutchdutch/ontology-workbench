---
process: <name>                 # the file name, lowercase, hyphens
title: <Title the page shows>
cadence: <weekly | daily | per intake>   # optional; delete when the process has none
target: "<optional: a one-line goal the process serves, shown in the panel>"
drafted_by: <name>
drafted: <YYYY-MM-DD>
reviewed: none                  # the date, once a named reviewer has read every box aloud
reviewed_by: []
source: "<the diagram or brief this was drawn from, and who made it>"
---

# <Title>

A process, as a hypothesis. **Nothing here is agreed** until `reviewed:` holds a date.

Every box names the glossary terms it uses. The page shows the glossary's own definition for each;
nothing here defines a term. A word in a box that has no entry is listed under Working names.

## In one line

<One sentence a newcomer can repeat: who does what, and what comes out.>

## Lanes

Who does the work, top to bottom. `kind` is `people`, `ai` or `team` and sets the colour.

```yaml
<lane-id>: { label: "<Lane name>", who: "<one line on who this is>", kind: people }
<lane-id>: { label: "<Lane name>", who: "<one line>", kind: ai }
<lane-id>: { label: "<Lane name>", who: "<one line>", kind: team }
```

## Steps

The columns, left to right.

```yaml
steps: ["<Step 1>", "<Step 2>", "<Step 3>"]
```

## Paths

The same process at rising levels of trouble, simplest first. Each lights the boxes it uses and
fades the rest; they nest. Delete this section if the process has one path.

### Happy path

> <When the week looks like this.>

```yaml
id: happy
share: <how often, e.g. 10%>
boxes: [<id>, <id>]
```

<What this path is, for the sidebar.>

## Boxes

One heading per box. The quote is the card text. The YAML places the box and links its terms. The
prose after it is the longer explanation the page shows in the sidebar.

### <Box title>

> <The card text, one line.>

```yaml
id: <short-id>
step: 1
lane: <lane-id>
terms: ["[[<Term>]]", "[[<Term>]]"]
next: [<id>]                                   # main flow, solid
when_needed: [{ to: <id>, label: "<chip>" }]   # dashed, optional
human_moment: false                            # true draws the badge
tag: ""                                        # optional: the party acting, when a lane holds more than one
```

<The longer explanation. Plain prose, as long as it needs to be. Wikilinks work here too.>

## Working names

Words in the boxes that have no glossary entry, and why they are not linked.

| Word | What it is today | Note |
|---|---|---|

## Findings for step 05

Terms the process needs with no entry, and entries that say too little. None yet.

## Open questions

What the reviewer must answer before signing.
