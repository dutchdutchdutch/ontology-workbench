---
stream: <name>
drafted_by: <name>
drafted: <YYYY-MM-DD>
reviewed: none          # the date, once a named reviewer has read every flow aloud
reviewed_by: []
---

# <Value>: the value stream, as a hypothesis

Where <value> comes from, where it goes, what sets it off and what stops it. Drafted from
`05-glossary/glossary.md`. **Nothing here is agreed** until `reviewed:` holds a date.

| confidence | means |
|---|---|
| `stated` | one entry says this in so many words |
| `inferred` | two entries together imply it, but no single entry says it |
| `assumed` | neither. A guess, so the row is a question |

## The stream in one line

<One sentence: where the value starts, what it passes through, where it lands.>

## Flows

The value actually moving. One heading per flow.

### 1. <Funder> <verb> <earner>

> <The flow in one plain sentence.>

```yaml
from: "[[<Term>]]"
to: "[[<Term>]]"
kind: <what moves>
via: ""
trigger: ""
confidence: stated
evidence: "<Term>: <the glossary sentence, verbatim>."
note: ""
```

## Roles

What each term does in this stream. A term with no role here is not part of the stream. Delete
the roles nobody holds.

```yaml
funder: []
approver: []
gate: []
claim: []
conduit: []
unit: []
meter: []
clock: []
trigger: []
earner: []
leak: []
repair: []
```

| Role | Means |
|---|---|
| `funder` | pays for the value; it starts here |
| `approver` | decides that the value may move, and how much |
| `gate` | the value cannot pass until this is true |
| `claim` | the document that asks for the value |
| `conduit` | what carries the value |
| `unit` | what the value is counted in |
| `meter` | what sets the amount |
| `clock` | what sets the timing |
| `trigger` | what sets a flow off, when it is not a claim or a clock |
| `earner` | is paid for delivering the value; it lands here |
| `leak` | value that should flow and does not |
| `repair` | the work that fixes a leak |

## Findings for step 05

Terms the stream needs with no entry, and entries that say too little. None yet.

## Open questions

What the reviewer must answer before signing.
