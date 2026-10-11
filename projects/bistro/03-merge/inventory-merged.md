---
project: bistro
step: 03-merge
run: 2026-09-04
inventories: [drive, linear-issues, code]
rows: 34
---

# Merged inventory: bistro

Three inventories, one table. Flags come from the `flag after delta` column of
`../02-delta/delta-report.md`. Flags: `synonym` (two names, one thing, confirmed by a second
source), `homonym` (one name, two things; the rows are never merged), `overloaded` (one name used
at two levels of precision), `unnamed-concept`, or empty.

| term | variants seen | frequency band | source type | discipline or team | inferred meaning | example quote + link | confidence | flag |
|---|---|---|---|---|---|---|---|---|
| guest | guests | everywhere | doc, issue | floor | A person who comes in to eat | "We never say customer on the floor. Everyone who walks in is a guest." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-16 | high | synonym |
| customer | customer record, customer model | common | doc, issue, pr | floor, engineering | The app's name for the person who books; the floor avoids it | "Customer record keeps the phone number from the booking, so the host can text the party when their table is ready." [BIS-14](../00-sources/raw/linear-issues/BIS-14.md). Also: staff handbook, PR #41 | high | synonym |
| party | party of one | everywhere | doc | floor | The group that comes in, sits and pays together | "A party is the group that comes in together. They sit together and they pay together." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md) | high | |
| party size | | common | issue | engineering | The number of people on a booking | "Raise the party size limit to 12." [BIS-11](../00-sources/raw/linear-issues/BIS-11.md) | high | |
| cover | covers | common | doc, issue | floor | One guest who sat down, counted | "When we count covers we count guests: a six-top with five people at it is five covers." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-14 | high | overloaded |
| covers | | occasional | issue | engineering | The party size on a booking | "Covers is the party size on the booking, not a separate count." [BIS-14](../00-sources/raw/linear-issues/BIS-14.md) | medium | overloaded |
| table | six-top, four-top, deuce, table 12 | everywhere | doc, issue | floor, engineering | A numbered place where one party sits | "When we say "a six-top" we mean a table for six." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-13 | high | |
| service | lunch, dinner | everywhere | doc | floor, kitchen | One meal period | "A service is one meal period: lunch is one service, dinner is another." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md) | high | |
| host | hosts | common | doc, issue | floor | The person at the door who greets and seats | "The host stands at the door, greets every party and keeps the reservation book." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-13 | high | |
| seating | seat | common | doc | floor | The moment a party is taken to its table | "The host does every seating, so nobody walks a party to a table on their own." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md) | medium | synonym |
| table assignment | seat-lock | rare | pr, branch | engineering | Giving a party a table | "Fix server timeout on concurrent table assignment" [PR #43](../00-sources/raw/code/pr-43.md) | medium | synonym |
| reservation | reservation book, reservations | common | doc, issue | floor | A table held for a named party at a set time | "A reservation holds a table for a named party at a set time." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-11 | high | synonym |
| booking | bookings, booking time, booking form | everywhere | doc, issue, pr, branch | floor, engineering | A table held for a party at a set time | "If the party has not arrived 15 minutes after the booking time, the host marks a no-show." [BIS-12](../00-sources/raw/linear-issues/BIS-12.md). Also: Friday dinner service notes, PR #42 | high | synonym |
| no-show | no-shows, no-show job | occasional | doc, issue, pr, branch | floor, engineering | A reserved party that never arrives | "If the party has not arrived 15 minutes after the time, the host marks a no-show and gives the table away." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-12, PR #42 | high | |
| walk-in | walk-ins | common | doc, issue | floor | A party that arrives without a reservation | "A walk-in is a party that turns up without a reservation." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-12 | high | homonym |
| walk-in | walk-in door | common | doc | kitchen | The kitchen's cold room | "The walk-in is our cold room. Close the walk-in door every time." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md) | high | homonym |
| server | servers | everywhere | doc, issue | floor | The person who looks after a section of tables | "Each server has a section of tables for the service." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-13 comments | high | homonym |
| server | server timeout | occasional | doc, issue, pr | floor, engineering | The computer the app runs on | "The server timed out on the lock and every tablet froze for about five minutes." [BIS-13](../00-sources/raw/linear-issues/BIS-13.md). Also: Friday dinner service notes, PR #43 | high | homonym |
| order | ordered, order screen | everywhere | doc, issue | floor, kitchen | What a party asks for | "Your server takes the order, brings the food and presents the check at the end." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-17 | medium | |
| check | split checks, check average, split check, split-check | common | doc, issue, pr, branch | floor, engineering | The party's bill | "The check lists everything the party ordered with its price, plus tax." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-16, PR #47 | high | |
| comp | comped, comps | occasional | doc, issue | floor | Taking an item off the check for free | "Only Theo can comp an item: a comp takes the item off the check, and we note why." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-16 | high | |
| tip | tips | occasional | doc | floor | Money the party leaves for the server | "Servers keep their own tips." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md) | medium | |
| turn | turns | occasional | doc | floor | One party seated, fed and gone at a table | "A turn is one party seated, fed and gone." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md) | high | |
| expo | | common | doc | kitchen, floor | The person at the pass who runs the tickets | "The expo reads every ticket, calls fire for each course and checks every plate before a server takes it." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md) | high | |
| the pass | pass | common | doc | kitchen, floor | The heated counter where plates wait to go out | "The pass is the heated counter between the kitchen and the dining room." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md) | high | |
| station | grill, saute, cold, pastry, station printers | common | doc, pr | kitchen, engineering | One cooking position on the line | "Each station cooks its own menu items and has its own ticket printer." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md). Also: PR #45 | high | |
| ticket | chit | everywhere | doc, issue | kitchen | The kitchen's printed copy of an order | "Every order prints as a ticket at each station that cooks part of it." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md). Also: BIS-17 | high | synonym |
| kitchen_order | kitchen order, kitchen-order-routing | rare | issue, pr, branch | engineering | The app's record of a ticket, one per station | "In the code a ticket is a kitchen_order. One order, one kitchen_order per station." [BIS-17](../00-sources/raw/linear-issues/BIS-17.md). Also: PR #45 | high | synonym |
| course | starters, mains, dessert | common | doc | kitchen | Everything one table eats at the same time | "A course is everything one table eats at the same time: starters, mains, dessert." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md) | high | |
| fire | fire mains | common | doc | kitchen | Start cooking a course now | "We fire a course when the expo calls it, not before." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md) | high | |
| menu item | dish, item, menu items | common | doc, issue, pr | kitchen, engineering | One dish or drink on the menu | "When we run out of a menu item, the expo calls "86 the duck" and it is gone until the next service." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md). Also: BIS-15, PR #46 | high | |
| 86 | 86es, 86'd, eighty-six | occasional | doc, issue, pr, branch | kitchen, floor, engineering | A menu item run out for the rest of the service | "If the kitchen 86es something, it is gone for the rest of the service." [Linden Street Bistro staff handbook](../00-sources/raw/drive/staff-handbook.md). Also: BIS-15, PR #46 | high | |
| allergy note | allergy notes | occasional | doc, issue | floor, kitchen | A note on an order naming an allergy, printed on every ticket | "An allergy note prints in red on every ticket for that order." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md). Also: BIS-17 | high | |
| family meal | | rare | doc | kitchen | The staff meal before service | "Family meal is at 4:15 before dinner service. Whoever is on cold cooks it. Everyone eats." [Kitchen guide](../00-sources/raw/drive/kitchen-guide.md) | high | |
