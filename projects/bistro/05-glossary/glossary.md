---
project: bistro
step: 05-glossary
published_from: v2
stage: trial
stage_since: 2026-09-15
reviewed_by: [Theo, Rosa, Priya]
---

# Linden Street Bistro glossary

The words the floor, the kitchen and the app share, and what each one means here. Many of them
mean something else outside a restaurant: a cover is not a lid, a ticket is not for a concert,
the check is the bill, and a server is a person. When this file and another document disagree,
this file wins.

Four companion files: [core-terms.md](core-terms.md) (the twelve words to learn first),
[about-core-terms.md](about-core-terms.md) (why those twelve), [taxonomy.md](taxonomy.md) (how the
categories fit together) and [backlog.md](backlog.md) (what is not core, and why).

## How to read an entry

Each entry is a heading, a definition in a quoted block, and a block of keys.

| Key | What it tells you |
|---|---|
| `type` | What kind of thing the term is: a role, an entity, an event, a document, a metric, an action or a state |
| `owner` | Who decides what the word means: the floor, the kitchen or engineering |
| `core` | `true` for the twelve terms to learn first |
| `workflow` | Where the term sits in the meal, from reservation (1) to tip (8) |
| `also_called` | Other words people use for the same thing. `(internal only)` means the app's name, never shown to staff or guests |
| `not_to_be_confused_with` | A term people mix this one up with |
| `visibility` | Who can see it, when not everyone can |
| `relations` | What this thing does to another, one line each |
| `depends_on` | The terms the definition is built from |
| `rulings` | The decisions in `../decisions/` that shaped the entry |

## Categories

| Category | Entries | Core | What it holds |
|---|---|---|---|
| People | 6 | 3 | who is involved: guests, parties and the staff who serve them |
| The meal | 11 | 6 | what happens to a guest, from reservation to tip |
| Floor | 4 | 2 | the dining room: tables, services and how the floor counts them |
| Kitchen | 6 | 1 | the line, the food and the kitchen's own places |
| **Total** | **27** | **12** | |

## People

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

### Party

> One or more [[Guest]]s who arrive together and eat together at one table.

```yaml
type: entity
owner: floor
status: verified
category: People
core: true
relations: ["contains [[Guest]]"]
relation_kinds: [contains]
depends_on: ["[[Guest]]"]
```

### Walk-in (party)

> A [[Party]] that arrives to eat with no reservation.

```yaml
type: entity
owner: floor
status: verified
category: People
core: false
also_called: [walk-in (floor), walk-in party (on screens)]
not_to_be_confused_with: ["[[Walk-in (cold room)]]"]
relations: ["is a [[Party]]"]
relation_kinds: [is_a]
depends_on: ["[[Party]]"]
rulings: [003]
```

### Server

> The person who works a [[Service]] looking after a section of [[Table]]s, takes each party's
> [[Order]] and brings its food.

```yaml
type: role
owner: floor
status: verified
category: People
core: true
also_called: [waiter]
relations: ["works [[Service]]", "serves [[Table]]", "takes [[Order]]"]
relation_kinds: [performs, serves, creates]
depends_on: ["[[Table]]", "[[Service]]", "[[Order]]"]
rulings: [004]
```

### Host

> The person at the door who greets each [[Party]], keeps the book of [[Reservation]]s and performs
> every [[Seating]].

```yaml
type: role
owner: floor
status: verified
category: People
core: false
relations: ["greets [[Party]]", "keeps [[Reservation]]", "performs [[Seating]]"]
relation_kinds: [serves, performs, performs]
depends_on: ["[[Party]]", "[[Reservation]]", "[[Seating]]"]
```

### Expo

> The person at [[The pass]] who reads every [[Ticket]], calls each [[Fire]] and inspects every
> plate before it goes out.

```yaml
type: role
owner: kitchen
status: verified
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

```yaml
type: entity
owner: floor
status: verified
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

```yaml
type: event
owner: floor
status: verified
category: The meal
core: false
relations: ["voids [[Reservation]]", "is marked by [[Host]]"]
relation_kinds: [blocks, created_by]
depends_on: ["[[Reservation]]", "[[Host]]"]
```

### Seating

> The moment a [[Party]] is given a [[Table]] and sits down: the table its [[Reservation]] holds, or
> the next free one.

```yaml
type: event
owner: floor
status: verified
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

```yaml
type: entity
owner: floor
status: verified
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

```yaml
type: document
owner: kitchen
status: verified
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

```yaml
type: document
owner: kitchen
status: verified
category: The meal
core: false
relations: ["is part of [[Order]]", "concerns [[Guest]]", "prints on [[Ticket]]"]
relation_kinds: [part_of, concerns, feeds]
depends_on: ["[[Order]]", "[[Guest]]", "[[Ticket]]"]
```

### Fire

> The call to start cooking a [[Course]] now, timed so that it reaches the table hot.

```yaml
type: action
owner: kitchen
status: verified
category: The meal
core: false
workflow: [meal 5]
relations: ["starts [[Course]]"]
relation_kinds: [creates]
depends_on: ["[[Course]]"]
```

### Course

> Every [[Menu item]] that one table eats at the same time, such as starters, mains or dessert.

```yaml
type: entity
owner: kitchen
status: verified
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

```yaml
type: document
owner: floor
status: verified
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

```yaml
type: action
owner: floor
status: verified
category: The meal
core: false
visibility: [server, host]
relations: ["reduces [[Check]]"]
depends_on: ["[[Check]]"]
```

### Tip

> Money a [[Party]] leaves after paying the [[Check]], to pay its [[Server]] directly.

```yaml
type: entity
owner: floor
status: verified
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

```yaml
type: entity
owner: floor
status: verified
category: Floor
core: true
also_called: [deuce, four-top, six-top]
relations: ["seats [[Party]]"]
relation_kinds: [holds]
depends_on: ["[[Party]]"]
```

### Service

> One meal period, such as lunch or dinner, from the first seating to the last order.

```yaml
type: event
owner: floor
status: verified
category: Floor
core: true
```

### Cover

> One [[Guest]] who sat down, counted. Covers measure how busy a [[Service]] was.

```yaml
type: metric
owner: floor
status: verified
category: Floor
core: false
not_to_be_confused_with: ["[[Guest]]"]
relations: ["counts [[Guest]]", "measures [[Service]]"]
relation_kinds: [measures, measures]
depends_on: ["[[Guest]]", "[[Service]]"]
rulings: [002]
```

### Turn

> A measure of a [[Table]]: how many [[Party]]s it seats in one service. Three parties at one table
> over dinner is three turns.

```yaml
type: metric
owner: floor
status: verified
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

```yaml
type: entity
owner: kitchen
status: verified
category: Kitchen
core: true
also_called: [dish]
```

### Station

> One cooking position on the line, such as grill, sauté, cold or pastry, with its own cook and
> ticket printer. It reads each [[Ticket]] it is sent, cooks its own [[Menu item]]s and sends them
> to [[The pass]].

```yaml
type: entity
owner: kitchen
status: verified
category: Kitchen
core: false
relations: ["reads [[Ticket]]", "cooks [[Menu item]]", "sends to [[The pass]]"]
relation_kinds: [fed_by, creates, feeds]
depends_on: ["[[Ticket]]", "[[Menu item]]", "[[The pass]]"]
```

### The pass

> The heated counter between the kitchen and the dining room where finished plates wait to go out.

```yaml
type: entity
owner: kitchen
status: verified
category: Kitchen
core: false
also_called: [pass]
```

### 86'd

> The state of a [[Menu item]] that has run out for the rest of the service. It comes back on the
> menu at the next one.

```yaml
type: state
owner: kitchen
status: verified
category: Kitchen
core: false
also_called: ["86", eighty-sixed]
relations: ["applies to [[Menu item]]"]
relation_kinds: [concerns]
depends_on: ["[[Menu item]]"]
```

### Walk-in (cold room)

> The refrigerated room, big enough to walk into, where the kitchen keeps its ingredients and from
> which it stocks every [[Station]] before a service.

```yaml
type: entity
owner: kitchen
status: verified
category: Kitchen
core: false
also_called: [walk-in (kitchen)]
not_to_be_confused_with: ["[[Walk-in (party)]]"]
relations: ["stocks [[Station]]"]
relation_kinds: [feeds]
depends_on: ["[[Station]]"]
rulings: [003]
```

### Family meal

> The meal the kitchen cooks for the whole staff before dinner opens.

```yaml
type: event
owner: kitchen
status: verified
category: Kitchen
core: false
```

## Rulings reflected

| Ruling | Reflected in |
|---|---|
| 001 | [[Guest]]: `also_called: [customer (internal only)]` |
| 002 | [[Cover]]: its own entry, a metric; [[Guest]]: `not_to_be_confused_with` |
| 003 | [[Walk-in (party)]] and [[Walk-in (cold room)]]: two entries, each tagged in `also_called` |
| 004 | [[Server]]: the person; no entry for the computer |

## Still open

One question, non-blocking: does [[Family meal]] always come before a [[Service]]? It is in the
question pack at the end of `../04-draft/v2/verification-queue.md`.
