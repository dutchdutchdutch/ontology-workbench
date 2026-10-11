---
project: bistro
step: 01-terms
source: linear-issues
produced_by: claude
prompt: issue-tracker.md
run: 2026-09-02
rows: 21
---

# Inventory: linear-issues (bistro)

| term | variants seen | frequency band | source type | discipline or team | inferred meaning | example quote + link | confidence | flag |
|---|---|---|---|---|---|---|---|---|
| customer | customers, customer record | common | issue | engineering | The person who books, and the app's record of them | "Customer record keeps the phone number from the booking, so the host can text the party when their table is ready." [BIS-14](../00-sources/raw/linear-issues/BIS-14.md) | high | synonym-suspect |
| guest | | occasional | issue | floor | One person in a party | "Let the server split one party's check by guest, so each guest pays for what they ordered." [BIS-16](../00-sources/raw/linear-issues/BIS-16.md) | medium | synonym-suspect |
| booking | booking time, booking form | everywhere | issue | engineering | A table held for a party at a set time | "If the party has not arrived 15 minutes after the booking time, the host marks a no-show." [BIS-12](../00-sources/raw/linear-issues/BIS-12.md) | high | synonym-suspect |
| reservation | reservations | rare | issue | floor | The floor's word for a booking | "On the floor we call these reservations, not bookings." [BIS-11](../00-sources/raw/linear-issues/BIS-11.md) | high | synonym-suspect |
| party size | party | common | issue | engineering | The number of people on a booking | "Raise the party size limit to 12." [BIS-11](../00-sources/raw/linear-issues/BIS-11.md) | high | |
| covers | | occasional | issue | engineering | The party size on a booking | "Covers is the party size on the booking, not a separate count." [BIS-14](../00-sources/raw/linear-issues/BIS-14.md) | medium | homonym-suspect |
| covers | | occasional | issue | floor | How many guests actually sat down | "Covers is how many guests actually sat down." [BIS-14](../00-sources/raw/linear-issues/BIS-14.md) | high | homonym-suspect |
| no-show | | occasional | issue | floor, engineering | A booking whose party never arrives | "Mark booking as no-show after 15 minutes" [BIS-12](../00-sources/raw/linear-issues/BIS-12.md) | high | |
| walk-in | | rare | issue | floor | A party with no booking | "The app should release the table at the same moment, so the host can seat a walk-in there." [BIS-12](../00-sources/raw/linear-issues/BIS-12.md) | medium | |
| host | hosts | occasional | issue | floor | The person who seats parties | "Server timeout when two hosts seat the same table" [BIS-13](../00-sources/raw/linear-issues/BIS-13.md) | medium | |
| table | table 12 | common | issue | floor, engineering | A numbered place a party is given | "Friday 7:10pm: two devices assigned table 12 at the same second." [BIS-13](../00-sources/raw/linear-issues/BIS-13.md) | high | |
| server | | occasional | issue | engineering | The computer the app runs on | "The server timed out on the lock and every tablet froze for about five minutes." [BIS-13](../00-sources/raw/linear-issues/BIS-13.md) | high | homonym-suspect |
| server | servers | occasional | issue | floor | A person on the floor | "The floor read "server timeout" as one of our servers." [BIS-13](../00-sources/raw/linear-issues/BIS-13.md) | high | homonym-suspect |
| menu item | item | occasional | issue | kitchen | One dish on the menu | "When the expo 86es a menu item, the servers should not be able to add it to an order." [BIS-15](../00-sources/raw/linear-issues/BIS-15.md) | high | |
| 86 | 86es | occasional | issue | kitchen | To mark a menu item as run out | "When the expo 86es a menu item, the servers should not be able to add it to an order." [BIS-15](../00-sources/raw/linear-issues/BIS-15.md) | high | |
| order | order screen | common | issue | floor, kitchen | What a party asks for | "An allergy note belongs to the whole order, so it must print on every station's ticket for that order." [BIS-17](../00-sources/raw/linear-issues/BIS-17.md) | medium | |
| check | split check | occasional | issue | floor | The party's bill | "Let the server split one party's check by guest, so each guest pays for what they ordered." [BIS-16](../00-sources/raw/linear-issues/BIS-16.md) | high | |
| comp | comps | rare | issue | floor | An item taken off the check | "Comps stay on the line they were applied to." [BIS-16](../00-sources/raw/linear-issues/BIS-16.md) | medium | |
| ticket | | occasional | issue | kitchen | The kitchen's printed copy of an order | "In the kitchen it is a ticket. Nobody here says kitchen order." [BIS-17](../00-sources/raw/linear-issues/BIS-17.md) | high | synonym-suspect |
| kitchen_order | kitchen order | rare | issue | engineering | The app's record of a ticket, one per station | "In the code a ticket is a kitchen_order. One order, one kitchen_order per station." [BIS-17](../00-sources/raw/linear-issues/BIS-17.md) | high | synonym-suspect |
| allergy note | allergy notes | occasional | issue | kitchen | A note naming an allergy, printed on tickets | "An allergy note belongs to the whole order, so it must print on every station's ticket for that order." [BIS-17](../00-sources/raw/linear-issues/BIS-17.md) | high | |

## Seen, not quoted

- tip: looked for in all seven issues and their comments. No issue mentions tips; the app does not
  handle them yet.

## Out of scope

| term | quote | why it is out |
|---|---|---|
| availability check | "A booking for 9 or more needs two tables pushed together, so the availability check must look for two free tables side by side." [BIS-11](../00-sources/raw/linear-issues/BIS-11.md) | engineering only; a step inside the app |
| lock | "The server timed out on the lock and every tablet froze for about five minutes." [BIS-13](../00-sources/raw/linear-issues/BIS-13.md) | engineering only |
