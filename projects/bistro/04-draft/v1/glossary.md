---
project: bistro
step: 04-draft
version: v1
date: 2026-09-05
based_on: 03-merge/inventory-merged.md
rulings_applied: []
entries: 25
---

# Draft glossary v1: bistro

The first draft, from `03-merge/inventory-merged.md`. Unreviewed. The four contested terms are
in `verification-queue.md`; the walk-in entry is a gap until an expert rules.

## Clusters and classification

| # | Concept | Rows | Class | Canonical name |
|---|---|---|---|---|
| 1 | Guest | guest, customer | SYNONYM | Guest (authority order; queue item 1) |
| 2 | Party | party, party size | CLEAN | Party |
| 3 | Cover | cover, covers (engineering) | OVERLOADED | folded into Guest for now; queue item 3 |
| 4 | Walk-in | walk-in (floor), walk-in (kitchen) | HOMONYM | open; queue item 4 |
| 5 | Server | server (person), server (computer) | HOMONYM | Server for the person; queue item 2 |
| 6 | Host | host | CLEAN | Host |
| 7 | Expo | expo | CLEAN | Expo |
| 8 | Reservation | reservation, booking | SYNONYM | Reservation (authority order) |
| 9 | No-show | no-show | CLEAN | No-show |
| 10 | Seating | seating, table assignment | SYNONYM | Seating (authority order) |
| 11 | Order | order | CLEAN | Order |
| 12 | Ticket | ticket, kitchen_order | SYNONYM | Ticket (authority order) |
| 13 | Allergy note | allergy note | CLEAN | Allergy note |
| 14 | Fire | fire | CLEAN | Fire |
| 15 | Course | course | CLEAN | Course |
| 16 | Check | check | CLEAN | Check |
| 17 | Comp | comp | CLEAN | Comp |
| 18 | Tip | tip | CLEAN | Tip |
| 19 | Table | table | CLEAN | Table |
| 20 | Service | service | CLEAN | Service |
| 21 | Turn | turn | CLEAN | Turn |
| 22 | Menu item | menu item | CLEAN | Menu item |
| 23 | Station | station | CLEAN | Station |
| 24 | The pass | the pass | CLEAN | The pass |
| 25 | 86'd | 86 | CLEAN | 86'd (the state, as the code and the expo say it) |
| 26 | Family meal | family meal | CLEAN | Family meal |

## People

### Guest

> A person who comes to the restaurant to eat, from the moment they arrive until they leave.

**Naming** Two open questions: may "customer" appear on a screen (queue item 1), and is a cover the same as a guest (queue item 3)?
**Examples** "We never say customer on the floor. Everyone who walks in is a guest." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Customer record keeps the phone number from the booking" ([BIS-14](../../00-sources/raw/linear-issues/BIS-14.md))
**Evidence** merged rows guest, customer.

```yaml
type: role
owner: floor
status: draft
category: People
core: true
also_called: [customer, covers]
```

### Party

> One or more [[Guest]]s who arrive together and eat together at one table.

**Examples** "A party is the group that comes in together. They sit together and they pay together." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Raise the party size limit to 12." ([BIS-11](../../00-sources/raw/linear-issues/BIS-11.md))
**Evidence** merged rows party, party size. Party size is a number on a reservation, not a second entry.

```yaml
type: entity
owner: floor
status: draft
category: People
core: true
relations: ["contains [[Guest]]"]
relation_kinds: [contains]
depends_on: ["[[Guest]]"]
```

### Walk-in

> Gap: is a walk-in a party that arrives without a reservation, or the kitchen's cold room? The
> handbook says "A walk-in is a party that turns up without a reservation." The kitchen guide says
> "The walk-in is our cold room."

**Naming** Queue item 4.
**Examples** "A walk-in is a party that turns up without a reservation." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "The walk-in is our cold room. Close the walk-in door every time." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md))
**Evidence** merged rows walk-in (floor), walk-in (kitchen), flagged homonym.

```yaml
type: entity
owner: floor
status: gap
category: People
core: false
```

### Server

> The person who works a [[Service]] looking after a section of [[Table]]s, takes each party's
> [[Order]] and brings its food.

**Naming** The app's issues and code use "server" for the computer. Queue item 2 asks whether that sense needs an entry or a new name.
**Examples** "Each server has a section of tables for the service." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "The floor read "server timeout" as one of our servers." ([BIS-13](../../00-sources/raw/linear-issues/BIS-13.md))
**Evidence** merged rows server (person), server (computer). The computer sense gets no entry.

```yaml
type: role
owner: floor
status: draft
category: People
core: true
also_called: [waiter]
relations: ["works [[Service]]", "serves [[Table]]", "takes [[Order]]"]
relation_kinds: [performs, serves, creates]
depends_on: ["[[Table]]", "[[Service]]", "[[Order]]"]
```

### Host

> The person at the door who greets each [[Party]], keeps the book of [[Reservation]]s and performs
> every [[Seating]].

**Examples** "The host stands at the door, greets every party and keeps the reservation book." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Server timeout when two hosts seat the same table" ([BIS-13](../../00-sources/raw/linear-issues/BIS-13.md))
**Evidence** merged row host.

```yaml
type: role
owner: floor
status: draft
category: People
core: false
relations: ["greets [[Party]]", "keeps [[Reservation]]", "performs [[Seating]]"]
relation_kinds: [serves, performs, performs]
depends_on: ["[[Party]]", "[[Reservation]]", "[[Seating]]"]
```

### Expo

> The person at [[The pass]] who reads every [[Ticket]], calls each [[Fire]] and inspects every
> plate before it goes out.

**Examples** "The expo reads every ticket, calls fire for each course and checks every plate before a server takes it." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "When the expo 86es a menu item, the servers should not be able to add it to an order." ([BIS-15](../../00-sources/raw/linear-issues/BIS-15.md))
**Evidence** merged row expo.

```yaml
type: role
owner: kitchen
status: draft
category: People
core: false
also_called: [expediter]
relations: ["works at [[The pass]]", "reads [[Ticket]]", "calls [[Fire]]"]
relation_kinds: [performs, fed_by, performs]
depends_on: ["[[The pass]]", "[[Ticket]]", "[[Fire]]"]
```


## The meal

### Reservation

> A promise, made for a named [[Party]], that holds a [[Table]] at a set time and falls in one
> [[Service]].

**Naming** "Reservation" wins by the authority order in `project.yaml`: the drive ranks above the issues and the code. "Booking" stays in the code, marked internal.
**Examples** "A reservation holds a table for a named party at a set time." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "On the floor we call these reservations, not bookings." ([BIS-11](../../00-sources/raw/linear-issues/BIS-11.md))
**Evidence** merged rows reservation, booking.

```yaml
type: entity
owner: floor
status: draft
category: The meal
core: true
workflow: [meal 1]
also_called: [booking (internal only)]
relations: ["is made for [[Party]]", "holds [[Table]]", "falls in [[Service]]"]
relation_kinds: [concerns, holds, part_of]
depends_on: ["[[Table]]", "[[Party]]", "[[Service]]"]
```

### No-show

> The moment a [[Reservation]] is voided because its party has not arrived 15 minutes after the set
> time. The [[Host]] marks it.

**Examples** "If the party has not arrived 15 minutes after the time, the host marks a no-show and gives the table away." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "No-show job releases booking after 15 min" ([PR #42](../../00-sources/raw/code/pr-42.md))
**Evidence** merged row no-show.

```yaml
type: event
owner: floor
status: draft
category: The meal
core: false
relations: ["voids [[Reservation]]", "is marked by [[Host]]"]
relation_kinds: [blocks, created_by]
depends_on: ["[[Reservation]]", "[[Host]]"]
```

### Seating

> The moment a [[Party]] is given a [[Table]] and sits down: the table its [[Reservation]] holds, or
> the next free one.

**Examples** "The host does every seating, so nobody walks a party to a table on their own." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Fix server timeout on concurrent table assignment" ([PR #43](../../00-sources/raw/code/pr-43.md))
**Evidence** merged rows seating, table assignment.

```yaml
type: event
owner: floor
status: draft
category: The meal
core: true
workflow: [meal 2]
also_called: [table assignment (internal only)]
relations: ["places [[Party]]", "fills [[Table]]", "follows [[Reservation]]"]
relation_kinds: [concerns, concerns, follows]
depends_on: ["[[Party]]", "[[Table]]", "[[Reservation]]"]
```

### Order

> Everything one [[Party]] asks for after its [[Seating]], grouped into [[Course]]s.

**Not to be confused with** [[Ticket]]. The code calls a ticket a kitchen_order, which reads like a kind of order.
**Examples** "Your server takes the order, brings the food and presents the check at the end." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "An allergy note belongs to the whole order, so it must print on every station's ticket for that order." ([BIS-17](../../00-sources/raw/linear-issues/BIS-17.md))
**Evidence** merged row order.

```yaml
type: entity
owner: floor
status: draft
category: The meal
core: true
workflow: [meal 3]
not_to_be_confused_with: ["[[Ticket]]"]
relations: ["is asked for by [[Party]]", "follows [[Seating]]", "contains [[Course]]"]
relation_kinds: [created_by, follows, contains]
depends_on: ["[[Party]]", "[[Seating]]", "[[Course]]"]
```

### Ticket

> The kitchen's printed copy of an [[Order]], with its items listed by [[Course]]. Each station that
> cooks part of the order gets its own copy.

**Not to be confused with** [[Order]]. One order makes one ticket per station; the code's name kitchen_order hides that they are different things.
**Naming** "Ticket" wins by the authority order. "Chit" is the kitchen's slang; kitchen_order is the code's name, marked internal.
**Examples** "Every order prints as a ticket at each station that cooks part of it." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "In the kitchen it is a ticket. Nobody here says kitchen order." ([BIS-17](../../00-sources/raw/linear-issues/BIS-17.md))
**Evidence** merged rows ticket, kitchen_order.

```yaml
type: document
owner: kitchen
status: draft
category: The meal
core: true
workflow: [meal 4]
also_called: [chit, kitchen_order (internal only)]
not_to_be_confused_with: ["[[Order]]"]
relations: ["copies [[Order]]", "lists [[Course]]"]
relation_kinds: [concerns, contains]
depends_on: ["[[Order]]", "[[Course]]"]
```

### Allergy note

> A note on an [[Order]] naming one [[Guest]]'s allergy. It prints in red on every [[Ticket]] for
> that order.

**Examples** "An allergy note prints in red on every ticket for that order." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "An allergy note belongs to the whole order, so it must print on every station's ticket for that order." ([BIS-17](../../00-sources/raw/linear-issues/BIS-17.md))
**Evidence** merged row allergy note.

```yaml
type: document
owner: kitchen
status: draft
category: The meal
core: false
relations: ["is part of [[Order]]", "concerns [[Guest]]", "prints on [[Ticket]]"]
relation_kinds: [part_of, concerns, feeds]
depends_on: ["[[Order]]", "[[Guest]]", "[[Ticket]]"]
```

### Fire

> The call to start cooking a [[Course]] now, timed so that it reaches the table hot.

**Examples** "We fire a course when the expo calls it, not before." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "The expo reads every ticket, calls fire for each course and checks every plate before a server takes it." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md))
**Evidence** merged row fire. Both quotes come from the kitchen guide; no other source uses the word.

```yaml
type: action
owner: kitchen
status: draft
category: The meal
core: false
workflow: [meal 5]
relations: ["starts [[Course]]"]
relation_kinds: [creates]
depends_on: ["[[Course]]"]
```

### Course

> Every [[Menu item]] that one table eats at the same time, such as starters, mains or dessert.

**Examples** "A course is everything one table eats at the same time: starters, mains, dessert." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "The ticket lists the items by course, starters first." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md))
**Evidence** merged row course.

```yaml
type: entity
owner: kitchen
status: draft
category: The meal
core: true
workflow: [meal 6]
relations: ["contains [[Menu item]]"]
relation_kinds: [contains]
depends_on: ["[[Menu item]]"]
```

### Check

> The bill for one [[Party]] that the [[Server]] presents at the end of the meal: every
> [[Menu item]] ordered, at its price, plus tax. A party may split it by guest.

**Examples** "The check lists everything the party ordered with its price, plus tax." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Split check by guest seat" ([PR #47](../../00-sources/raw/code/pr-47.md))
**Evidence** merged row check. The app's other check, the availability check, is out of scope.

```yaml
type: document
owner: floor
status: draft
category: The meal
core: true
workflow: [meal 7]
also_called: [bill]
relations: ["bills [[Party]]", "lists [[Menu item]]", "is presented by [[Server]]"]
relation_kinds: [bills, contains, performed_by]
depends_on: ["[[Party]]", "[[Server]]", "[[Menu item]]"]
```

### Comp

> Taking one item off a [[Check]] at no charge, approved by the floor manager, to make up for a
> problem.

**Examples** "Only Theo can comp an item: a comp takes the item off the check, and we note why." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Comps stay on the line they were applied to." ([BIS-16](../../00-sources/raw/linear-issues/BIS-16.md))
**Evidence** merged row comp.

```yaml
type: action
owner: floor
status: draft
category: The meal
core: false
visibility: [server, host]
relations: ["reduces [[Check]]"]
depends_on: ["[[Check]]"]
```

### Tip

> Money a [[Party]] leaves after paying the [[Check]], to pay its [[Server]] directly.

**Examples** "Servers keep their own tips." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Tips were good. Check average 38 per cover." ([Friday dinner, service notes](../../00-sources/raw/drive/friday-service-notes.md))
**Evidence** merged row tip.

```yaml
type: entity
owner: floor
status: draft
category: The meal
core: false
workflow: [meal 8]
relations: ["is left by [[Party]]", "is left after [[Check]]", "pays [[Server]]"]
relation_kinds: [created_by, follows, pays]
depends_on: ["[[Party]]", "[[Check]]", "[[Server]]"]
```


## Floor

### Table

> A numbered place in the dining room that seats one [[Party]] for a meal. It is named by its seats:
> a four-top seats four.

**Examples** "When we say "a six-top" we mean a table for six." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Friday 7:10pm: two devices assigned table 12 at the same second." ([BIS-13](../../00-sources/raw/linear-issues/BIS-13.md))
**Evidence** merged row table. The code's "bookings table" is a database table and is out of scope.

```yaml
type: entity
owner: floor
status: draft
category: Floor
core: true
also_called: [deuce, four-top, six-top]
relations: ["seats [[Party]]"]
relation_kinds: [holds]
depends_on: ["[[Party]]"]
```

### Service

> One meal period, such as lunch or dinner, from the first seating to the last order.

**Examples** "A service is one meal period: lunch is one service, dinner is another." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "When the expo 86es a menu item, the servers should not be able to add it to an order. Grey it out on the order screen until the end of the service." ([BIS-15](../../00-sources/raw/linear-issues/BIS-15.md))
**Evidence** merged row service.

```yaml
type: event
owner: floor
status: draft
category: Floor
core: true
```

### Turn

> A measure of a [[Table]]: how many [[Party]]s it seats in one service. Three parties at one table
> over dinner is three turns.

**Examples** "A turn is one party seated, fed and gone." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Three turns on the deuces, two on the four-tops." ([Friday dinner, service notes](../../00-sources/raw/drive/friday-service-notes.md))
**Evidence** merged row turn. Brought back from "Out of scope" by `01-terms/review.md`.

```yaml
type: metric
owner: floor
status: draft
category: Floor
core: false
visibility: [host, server, expo]
relations: ["measures [[Table]]", "counts [[Party]]"]
relation_kinds: [measures, measures]
depends_on: ["[[Table]]", "[[Party]]"]
```


## Kitchen

### Menu item

> One dish or drink on the menu, with its price.

**Examples** "When we run out of a menu item, the expo calls "86 the duck" and it is gone until the next service." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "Grey out 86'd menu items" ([PR #46](../../00-sources/raw/code/pr-46.md))
**Evidence** merged row menu item.

```yaml
type: entity
owner: kitchen
status: draft
category: Kitchen
core: true
also_called: [dish]
```

### Station

> One cooking position on the line, such as grill, sauté, cold or pastry, with its own cook and
> ticket printer. It reads each [[Ticket]] it is sent, cooks its own [[Menu item]]s and sends them
> to [[The pass]].

**Examples** "Each station cooks its own menu items and has its own ticket printer." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "kitchen_order: route items to station printers" ([PR #45](../../00-sources/raw/code/pr-45.md))
**Evidence** merged row station.

```yaml
type: entity
owner: kitchen
status: draft
category: Kitchen
core: false
relations: ["reads [[Ticket]]", "cooks [[Menu item]]", "sends to [[The pass]]"]
relation_kinds: [fed_by, creates, feeds]
depends_on: ["[[Ticket]]", "[[Menu item]]", "[[The pass]]"]
```

### The pass

> The heated counter between the kitchen and the dining room where finished plates wait to go out.

**Examples** "The pass is the heated counter between the kitchen and the dining room." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "Never walk into the kitchen to ask for a dish. Talk to the expo at the pass." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md))
**Evidence** merged row the pass.

```yaml
type: entity
owner: kitchen
status: draft
category: Kitchen
core: false
also_called: [pass]
```

### 86'd

> The state of a [[Menu item]] that has run out for the rest of the service. It comes back on the
> menu at the next one.

**Examples** "If the kitchen 86es something, it is gone for the rest of the service." ([Linden Street Bistro staff handbook](../../00-sources/raw/drive/staff-handbook.md)) · "Grey out 86'd menu items" ([PR #46](../../00-sources/raw/code/pr-46.md))
**Evidence** merged row 86.

```yaml
type: state
owner: kitchen
status: draft
category: Kitchen
core: false
also_called: ["86", eighty-sixed]
relations: ["applies to [[Menu item]]"]
relation_kinds: [concerns]
depends_on: ["[[Menu item]]"]
```

### Family meal

> The meal the kitchen cooks for the whole staff before dinner opens.

**Examples** "Family meal is at 4:15 before dinner service. Whoever is on cold cooks it. Everyone eats." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md)) · "Whoever is on cold cooks it." ([Kitchen guide](../../00-sources/raw/drive/kitchen-guide.md))
**Evidence** merged row family meal. Stands alone: no quote links it to another term.

```yaml
type: event
owner: kitchen
status: draft
category: Kitchen
core: false
```

## Appendix: beyond the entry cap

None. 25 entries, under the cap of 100.

## Linked, not defined

None. Every wikilink points at an entry.

## Rulings applied

None yet. This is the first draft, so no ruling exists.
