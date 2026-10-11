---
process: order-to-table
title: From the door to the paid check
cadence: per party
target: "Every course reaches the table hot, and every allergy note reaches every station."
drafted_by: Claude
drafted: 2026-09-16
reviewed: 2026-09-18
reviewed_by: [Theo, Rosa]
source: "The staff handbook and the kitchen guide, walked through with Theo and Rosa"
---

# From the door to the paid check

A process. Theo and Rosa read every box aloud and signed it on 2026-09-18.

Every box names the glossary terms it uses. The page shows the glossary's own definition for each;
nothing here defines a term. A word in a box that has no entry is listed under Working names.

## In one line

The host seats the party, the server takes its order, the kitchen cooks each course when the expo
calls it, and the party pays the check.

## Lanes

```yaml
party: { label: "Party", who: "The guests at one table", kind: people }
floor: { label: "Floor", who: "The host and the servers", kind: team }
kitchen: { label: "Kitchen", who: "The stations and the expo", kind: team }
```

## Steps

```yaml
steps: ["Arrive", "Sit", "Order", "Cook", "Serve", "Pay"]
```

## Paths

### A quiet night

> The party has a reservation and nothing runs out.

```yaml
id: quiet
share: 70%
boxes: [greet, seat, take, print, fire, pass, serve, present, pay]
```

The simplest run. Every box on it happens once per course, except the first two and the last two.

### A busy night

> Walk-ins wait at the bar, and the kitchen runs out of something.

```yaml
id: busy
share: 30%
boxes: [greet, bar, seat, take, print, fire, out, pass, serve, present, pay]
```

The same process with its two side doors open: a party with no reservation waits for a table,
and an item that runs out sends the server back to the table.

## Boxes

### Host greets the party

> The host checks the book for the party's reservation.

```yaml
id: greet
step: 1
lane: floor
terms: ["[[Host]]", "[[Party]]", "[[Reservation]]"]
next: [seat]
when_needed: [{ to: bar, label: "No reservation" }]
tag: "Host"
```

The [[Host]] is the only person who seats anyone. A [[Party]] with a [[Reservation]] goes straight
to its table.

### Walk-in waits at the bar

> No table is free yet; the party waits at the bar.

```yaml
id: bar
step: 1
lane: party
terms: ["[[Walk-in (party)]]"]
next: [seat]
```

The handbook: "Seat walk-ins at the bar first if the floor is full."

### Host seats the party

> The party gets its table and sits down.

```yaml
id: seat
step: 2
lane: floor
terms: ["[[Seating]]", "[[Table]]"]
next: [take]
tag: "Host"
```

The [[Seating]] uses the [[Table]] the reservation holds, or the next free one.

### Server takes the order

> One order per party, with an allergy note when anyone needs one.

```yaml
id: take
step: 3
lane: floor
terms: ["[[Server]]", "[[Order]]", "[[Allergy note]]"]
next: [print]
tag: "Server"
```

The allergy note goes on the [[Order]], never on one dish, so that every station sees it.

### A ticket prints at each station

> Each station that cooks part of the order gets its own ticket.

```yaml
id: print
step: 3
lane: kitchen
terms: ["[[Ticket]]", "[[Station]]"]
next: [fire]
```

The app calls this a kitchen_order. On the line it is a [[Ticket]].

### Expo calls fire

> The expo calls fire on the next course.

```yaml
id: fire
step: 4
lane: kitchen
terms: ["[[Expo]]", "[[Fire]]", "[[Course]]"]
next: [pass]
when_needed: [{ to: out, label: "Ran out" }]
tag: "Expo"
```

Mains are fired when the starters are cleared, so they land hot.

### An item is 86'd

> The kitchen has run out; the server goes back to the table.

```yaml
id: out
step: 4
lane: kitchen
terms: ["[[86'd]]", "[[Menu item]]"]
next: [take]
```

The app greys the [[Menu item]] out on the order screen for the rest of the service.

### Expo inspects every plate

> Plates wait at the pass; the expo reads the allergy note aloud.

```yaml
id: pass
step: 5
lane: kitchen
terms: ["[[The pass]]", "[[Expo]]", "[[Allergy note]]"]
next: [serve]
human_moment: true
tag: "Expo"
```

A person reads the allergy note out loud before the plate goes. Nobody wants a screen to do this
alone.

### Server brings the course

> The course reaches the table.

```yaml
id: serve
step: 5
lane: floor
terms: ["[[Server]]", "[[Course]]"]
next: [present]
when_needed: [{ to: fire, label: "Next course" }]
tag: "Server"
```

After each course the expo fires the next one, until dessert.

### Server presents the check

> The bill for the party, with any comp already taken off.

```yaml
id: present
step: 6
lane: floor
terms: ["[[Check]]", "[[Comp]]"]
next: [pay]
tag: "Server"
```

Only the floor manager can approve a [[Comp]].

### Party pays and tips

> The party pays the check and leaves a tip for its server.

```yaml
id: pay
step: 6
lane: party
terms: ["[[Party]]", "[[Check]]", "[[Tip]]"]
next: []
```

The [[Tip]] goes to the server directly. The table is free for its next turn.

## Working names

| Word | What it is today | Note |
|---|---|---|
| the bar | where walk-ins wait | a place, not a term the floor argues about |
| the book | the host's list of reservations | the screen in the app; "reservation" covers it |
| floor manager | Theo's job; approves every comp | a job title, not a role the glossary needs yet |

## Findings for step 05

None.

## Open questions

None left.
