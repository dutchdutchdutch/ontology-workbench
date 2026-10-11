---
project: bistro
step: 05-glossary
published_from: v2
categories: 4
---

# Taxonomy: Linden Street Bistro

The categories come from each entry's `category:` key. None is invented here.

## The groups

| Category | Entries | Core | What it holds | Core terms in it |
|---|---|---|---|---|
| People | 6 | 3 | Who is involved: guests, parties and the staff who serve them | [[Guest]], [[Party]], [[Server]] |
| The meal | 11 | 6 | What happens to a guest, from the reservation to the tip | [[Reservation]], [[Seating]], [[Order]], [[Course]], [[Ticket]], [[Check]] |
| Floor | 4 | 2 | The dining room: tables, meal periods and how the floor counts them | [[Service]], [[Table]] |
| Kitchen | 6 | 1 | The line, the food and the kitchen's own places | [[Menu item]] |
| **Total** | **27** | **12** | | |

## The order of the groups

People come first, because no other definition reads without them. The meal takes the
value-stream slot: it holds what a guest actually receives. Floor and Kitchen follow
alphabetically. No category goes to the tail; the restaurant acts on everything it names.

## How the groups relate

The meal is a path across the other three. A party from People makes a reservation for a table
on the Floor. Its order becomes tickets that the Kitchen cooks from menu items. The check and
the tip close the meal and pay the server back in People. The `workflow: meal` key numbers that
path from 1 (Reservation) to 8 (Tip), and the ontology picture can light it up as a lens.

Two loops sit inside it. Fire is a call back from the pass to the stations, once per course.
When a party leaves, its table goes back to the start for the next one; the floor counts
each round as a turn.

## What this taxonomy does not claim

It does not say who owns each category. `owner:` on each entry says that, term by term. It also
does not say the meal always runs in this order: a walk-in skips the reservation, and a
comp changes the check after it is written.
