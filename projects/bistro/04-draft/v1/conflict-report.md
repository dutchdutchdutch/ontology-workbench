---
project: bistro
step: 04-draft
version: v1
date: 2026-09-05
---

# Conflict report v1: bistro

## Synonyms: one thing, several names

| Names | Recommended canonical name | Rule that decided it | Confidence | Note |
|---|---|---|---|---|
| guest, customer | Guest | authority order: drive outranks issues and code | high | The app's screens say customer today. Whether that may stay is queue item 1 |
| reservation, booking | Reservation | authority order | high | Booking stays in the code, marked internal |
| ticket, kitchen_order, chit | Ticket | authority order | high | Chit is kitchen slang; kitchen_order is the code's name |
| seating, table assignment | Seating | authority order | medium | Table assignment is the code's name |

## Homonyms: one name, several things

| Name | Sense A | Sense B | Recommendation | Confidence |
|---|---|---|---|---|
| server | the person who looks after a section of tables (floor) | the computer the app runs on (engineering) | One entry, the person. The computer needs another word in anything the floor reads. Queue item 2 | high |
| walk-in | a party with no reservation (floor) | the kitchen's cold room (kitchen) | Two entries with a qualifier each. Queue item 4 | medium |
| covers | guests who sat down, counted (floor) | the party size on a reservation (engineering) | Overloaded, not a true homonym. Treated as a guest for now; queue item 3 | low |

## Relation conflicts

| Term A | Term B | Source A says | Source B says | Recommendation |
|---|---|---|---|---|
| No-show | Reservation | drive: the host "marks a no-show and gives the table away" | code: the "no-show job releases booking" | The entry says the no-show voids the reservation, and the host is the one who marks it. The app's job follows the host's mark |
| Allergy note | Ticket | drive: it "prints in red on every ticket" | linear-issues: it "belongs to the whole order" | Both are true. Two lines: part of the order, printed on every ticket |
