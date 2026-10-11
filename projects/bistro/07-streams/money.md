---
stream: money
drafted_by: Claude
drafted: 2026-09-16
reviewed: 2026-09-18
reviewed_by: [Theo]
---

# Money: the value stream, as a hypothesis

Where a guest's money comes from, where it goes, and what stops it. Drafted from
`05-glossary/glossary.md`. Theo read every flow aloud and signed it on 2026-09-18.

| confidence | means |
|---|---|
| `stated` | one entry says this in so many words |
| `inferred` | two entries together imply it, but no single entry says it |
| `assumed` | neither. A guess, so the row is a question |

## The stream in one line

A party pays its check at the end of the meal and leaves a tip that goes straight to its server.

## Flows

### 1. Party pays the check

> The party settles the check, priced from the menu items it ordered.

```yaml
from: "[[Party]]"
to: ""
kind: payment
via: "[[Check]]"
rate: "[[Menu item]]"
timing: "[[Service]]"
confidence: stated
evidence: "Check: The bill for one Party that the Server presents at the end of the meal: every Menu item ordered, at its price, plus tax."
note: "FINDING. The money lands with the restaurant itself, and the glossary has no entry for the restaurant as a business. Theo: leave it out for now; nobody on staff is confused about who gets paid."
```

### 2. Party tips the server

> After the check, the party leaves money that goes to its server directly.

```yaml
from: "[[Party]]"
to: "[[Server]]"
kind: tip
via: "[[Tip]]"
trigger: "[[Check]]"
confidence: stated
evidence: "Tip: Money a Party leaves after paying the Check, to pay its Server directly."
note: ""
```

## Roles

```yaml
funder: ["[[Party]]"]
claim: ["[[Check]]"]
conduit: ["[[Tip]]"]
unit: ["[[Cover]]"]
meter: ["[[Menu item]]"]
clock: ["[[Service]]"]
earner: ["[[Server]]"]
leak: ["[[No-show]]", "[[Comp]]"]
repair: ["[[Walk-in (party)]]"]
```

| Role | Means here |
|---|---|
| `funder` | the party pays for everything |
| `claim` | the check asks for the money |
| `conduit` | the tip carries money past the check, straight to the server |
| `unit` | the floor reports money per cover: "check average 38 per cover" |
| `meter` | each menu item's price sets the amount |
| `clock` | the check comes at the end of the meal, inside one service |
| `earner` | the server earns the tip |
| `leak` | a no-show holds a table that earns nothing; a comp takes an item off the check |
| `repair` | a walk-in party fills the table a no-show left |

## Findings for step 05

- The restaurant itself has no entry, so flow 1 has no `to`. Theo decided not to add one this
  round (see the note on flow 1).

## Open questions

None left. Theo answered both before signing: tips are not pooled, and comps never touch the tip.
