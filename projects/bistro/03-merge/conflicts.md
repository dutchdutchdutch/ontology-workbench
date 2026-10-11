---
project: bistro
step: 03-merge
run: 2026-09-04
flagged_rows: 14
---

# Conflicts: bistro

Every flagged row in `inventory-merged.md`, grouped by flag, with the evidence on each side.
Nothing is resolved here. Step 04 reads this list.

## homonym

| term | sense A, source and quote | sense B, source and quote |
|---|---|---|
| server | floor, staff handbook: "Each server has a section of tables for the service." | engineering, BIS-13: "The server timed out on the lock and every tablet froze for about five minutes." Also PR #43 "Fix server timeout on concurrent table assignment" |
| walk-in | floor, staff handbook: "A walk-in is a party that turns up without a reservation." | kitchen, Kitchen guide: "The walk-in is our cold room. Close the walk-in door every time." |

## overloaded

| term | reading A, source and quote | reading B, source and quote |
|---|---|---|
| cover / covers | floor, staff handbook: "When we count covers we count guests: a six-top with five people at it is five covers." BIS-14, Theo: "Covers is how many guests actually sat down." | engineering, BIS-14: "Covers is the party size on the booking, not a separate count." |

## synonym

| names | source and quote for each |
|---|---|
| guest / customer | floor, staff handbook: "We never say customer on the floor. Everyone who walks in is a guest." Engineering, BIS-14: "Customer record keeps the phone number from the booking, so the host can text the party when their table is ready." |
| reservation / booking | floor, staff handbook: "A reservation holds a table for a named party at a set time." Engineering, PR #42: "No-show job releases booking after 15 min". Both in BIS-11: "On the floor we call these reservations, not bookings." |
| ticket / kitchen_order / chit | kitchen, Kitchen guide: "Every order prints as a ticket at each station that cooks part of it." Engineering, BIS-17: "In the code a ticket is a kitchen_order. One order, one kitchen_order per station." Rosa, BIS-17: "In the kitchen it is a ticket. Nobody here says kitchen order." |
| seating / table assignment | floor, staff handbook: "The host does every seating, so nobody walks a party to a table on their own." Engineering, PR #43: "Fix server timeout on concurrent table assignment" |
