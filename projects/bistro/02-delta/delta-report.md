---
project: bistro
step: 02-delta
run: 2026-09-04
inventories: [drive, linear-issues, code]
against: none
review: 01-terms/review.md    # reviewed 2026-09-03, 3 expected terms listed
---

# Delta report: bistro

Three inventories compared with each other. There is no glossary yet, so sections 4 to 7 are one
line each. Four suspect flags are confirmed, one turns into `overloaded`, and two are cleared.

## 1. Same word, different meaning

| term | source A meaning and quote | source B meaning and quote | flag in inventory | flag after delta |
|---|---|---|---|---|
| server | drive (floor): the person who looks after a section of tables. "Each server has a section of tables for the service." | linear-issues and code (engineering): the computer the app runs on. "The server timed out on the lock and every tablet froze for about five minutes." | homonym-suspect | homonym |
| walk-in | drive, Linden Street Bistro staff handbook (floor): a party with no reservation. "A walk-in is a party that turns up without a reservation." Confirmed by linear-issues: "so the host can seat a walk-in there." | drive, Kitchen guide (kitchen): the cold room. "The walk-in is our cold room. Close the walk-in door every time." | homonym-suspect | homonym |
| covers | linear-issues (engineering): the party size on a booking. "Covers is the party size on the booking, not a separate count." | drive and linear-issues (floor): guests who actually sat down. "When we count covers we count guests: a six-top with five people at it is five covers." | homonym-suspect | overloaded |
| check | drive, linear-issues and code all use it for the bill. "The check lists everything the party ordered with its price, plus tax." | The other sense, a check inside the app, is under "Out of scope" in two inventories: "Add availability check before confirming booking" | homonym-suspect | (none): one shared sense; the other is out of scope |

## 2. Different words, same meaning

| term | source A meaning and quote | source B meaning and quote | flag in inventory | flag after delta |
|---|---|---|---|---|
| guest / customer | drive (floor): "We never say customer on the floor. Everyone who walks in is a guest." | linear-issues and code (engineering): "Customer record keeps the phone number from the booking, so the host can text the party when their table is ready." | synonym-suspect | synonym. Guest is the word staff and guests see; customer is the app's internal name. Noted, not resolved. |
| reservation / booking | drive (floor): "A reservation holds a table for a named party at a set time." | linear-issues and code (engineering): "No-show job releases booking after 15 min". BIS-11 uses both: "On the floor we call these reservations, not bookings." | synonym-suspect | synonym |
| ticket / kitchen_order / chit | drive (kitchen): "Every order prints as a ticket at each station that cooks part of it." The Kitchen guide gives chit as a variant. | linear-issues and code (engineering): "In the code a ticket is a kitchen_order. One order, one kitchen_order per station." | synonym-suspect | synonym |
| seating / table assignment | drive (floor): "The host does every seating, so nobody walks a party to a table on their own." | code (engineering): "Fix server timeout on concurrent table assignment" | synonym-suspect | synonym |
| cover / guest | drive (floor): "When we count covers we count guests: a six-top with five people at it is five covers." | drive (floor): "We never say customer on the floor. Everyone who walks in is a guest." | synonym-suspect | (none): a cover counts a guest; it is not another name for one. See section 1. |

## 3. Present in one source only

| term | source | discipline | note |
|---|---|---|---|
| party | drive | floor | linear-issues has `party size`, an attribute of a booking, not the group |
| service | drive | floor, kitchen | |
| seating | drive | floor | code says table assignment; see section 2 |
| tip | drive | floor | expected in linear-issues by `review.md`; not quoted there |
| turn | drive | floor | brought back from "Out of scope" by `review.md` |
| expo | drive | kitchen, floor | |
| the pass | drive | kitchen, floor | |
| course | drive | kitchen | |
| fire | drive | kitchen | |
| family meal | drive | kitchen | no quote links it to another term; see `review.md` |
| server timeout | drive | floor | the floor quoting the app's error; see section 1 |
| party size | linear-issues | engineering | |
| table assignment | code | engineering | see section 2 |

Different relation:

| term A | term B | source A verb | source B verb | note |
|---|---|---|---|---|
| no-show | reservation | drive: the host "marks a no-show and gives the table away" | code: the "no-show job releases booking" | Who acts differs: a person on the floor, a job in the app. Both say the reservation stops holding the table. |
| allergy note | ticket | drive: an allergy note "prints in red on every ticket for that order" | linear-issues: an allergy note "belongs to the whole order" | Two facts, not a conflict: it belongs to the order and prints on each ticket. |
| ticket | station | drive: an order "prints as a ticket at each station" | code: "route items to station printers" | Same direction, different subject: the drive makes the ticket the thing that moves, the code routes items. |

## 4. New terms

No glossary to compare against.

## 5. Moved meaning

No glossary to compare against.

## 6. Code drift

No glossary to compare against. The code's own names are compared with the other inventories in
sections 1 and 2.

## 7. Unused glossary terms

No glossary to compare against.
