---
project: bistro
step: 05-glossary
published_from: v2
core_terms: 12
---

> Published copy of the bistro vocabulary, draft v2, stage trial, published 2026-10-10. Do not edit it here: it is replaced on every publish. Send changes to Theo.

# About the core terms

For the person who wants to argue with the list in [core-terms.md](core-terms.md). That file
holds the definitions; this one says why these twelve, in what order, and what the shape of the
set says.

## How the core was chosen

By dependency, never by how often a word appears. A term is core when another core term cannot
be defined without it, or when it heads a chain of them. The evidence is each entry's
`depends_on:` in [glossary.md](glossary.md).

Two kinds of root. Guest, Service and Menu item are where the chains start: they depend on
nothing. Ticket and Check are where they end: nothing in the core rests on them, and they are the
words the chains exist to define. `factory/rules/core-selection.md` counts both as core.

Twelve is well under the 30 that `factory/rules/core-selection.md` expects for a first round.
That is the size of a small restaurant, not a missing area. `project.yaml` sets `expect: 12`.

## The dependency order

Read top to bottom and you never meet a core word before its definition.

| # | Term | Rests on |
|---|---|---|
| 1 | [[Guest]] | nothing |
| 2 | [[Service]] | nothing |
| 3 | [[Menu item]] | nothing |
| 4 | [[Party]] | Guest |
| 5 | [[Table]] | Party |
| 6 | [[Reservation]] | Table, Party, Service |
| 7 | [[Seating]] | Party, Table, Reservation |
| 8 | [[Course]] | Menu item |
| 9 | [[Order]] | Party, Seating, Course |
| 10 | [[Server]] | Table, Service, Order |
| 11 | [[Ticket]] | Order, Course |
| 12 | [[Check]] | Party, Server, Menu item |

## Cycles

None. An early draft had Party and Check defined through each other ("a party pays one check",
"the bill for one party"). The fix was in the definitions: Party now says only that its guests
arrive and eat together, and Check says a party may split it by guest.

## The swap test

Replace each core term with its nearest synonym. If the sentence still reads true, the
definition is too loose.

| Term | Nearest synonym | Does the swap still read true? |
|---|---|---|
| Guest | customer | No. Ruling 001: customer is the app's word, never on a screen |
| Party | table | No. A table seats a party; one table can hold three parties in a service |
| Server | waiter | Yes, and that is fine: waiter is listed in `also_called`, it is the same role |
| Reservation | booking | Yes, and that is fine: booking is the internal name for the same thing |
| Seating | arrival | No. A party arrives before its seating; walk-ins may wait at the bar |
| Order | ticket | No. One order makes one ticket per station |
| Course | dish | No. A course is every dish one table eats at once |
| Ticket | order | No. Same reason, the other way round |
| Check | receipt | No. The check comes before payment; a receipt comes after |
| Service | shift | No. A shift is a person's working hours; a service is the restaurant's meal period |
| Table | seat | No. A table has several seats |
| Menu item | ingredient | No. An ingredient goes into a menu item |

Two swaps read true, and both are aliases already recorded. No definition was tightened this
round.

## What the shape says

Half the core sits in The meal: the reservation-to-check sequence is what this vocabulary is for.
The kitchen has one core term, Menu item. Its other words are precise but nothing in the core
rests on them: Station waits in [backlog.md](backlog.md) as `next`, The pass and Fire as `later`.
