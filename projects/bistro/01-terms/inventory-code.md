---
project: bistro
step: 01-terms
source: code
produced_by: claude
prompt: code-repository.md
run: 2026-09-02
rows: 10
---

# Inventory: code (bistro)

| term | variants seen | frequency band | source type | discipline or team | inferred meaning | example quote + link | confidence | flag |
|---|---|---|---|---|---|---|---|---|
| booking | bookings, booking-form | common | pr, branch | engineering | A table held for a party at a set time | "No-show job releases booking after 15 min" [PR #42](../00-sources/raw/code/pr-42.md) | high | synonym-suspect |
| customer | customer model | rare | pr | engineering | The app's record of the person who books | "Add bookings table and customer model" [PR #41](../00-sources/raw/code/pr-41.md) | high | synonym-suspect |
| no-show | no-show job | rare | pr, branch | engineering | A booking whose party never arrives | "No-show job releases booking after 15 min" [PR #42](../00-sources/raw/code/pr-42.md) | high | |
| server | | rare | pr | engineering | The computer the app runs on | "Fix server timeout on concurrent table assignment" [PR #43](../00-sources/raw/code/pr-43.md) | high | homonym-suspect |
| table assignment | seat-lock | rare | pr, branch | engineering | Giving a party a table | "Fix server timeout on concurrent table assignment" [PR #43](../00-sources/raw/code/pr-43.md) | medium | synonym-suspect |
| kitchen_order | kitchen-order-routing | rare | pr, branch | engineering | The record of one order sent to one station | "kitchen_order: route items to station printers" [PR #45](../00-sources/raw/code/pr-45.md) | high | synonym-suspect |
| station | station printers | rare | pr | engineering | A kitchen position with its own printer | "kitchen_order: route items to station printers" [PR #45](../00-sources/raw/code/pr-45.md) | medium | |
| 86'd | eighty-six | rare | pr, branch | engineering | A menu item marked as run out | "Grey out 86'd menu items" [PR #46](../00-sources/raw/code/pr-46.md) | high | |
| menu item | menu items | rare | pr | engineering | One dish on the menu | "Grey out 86'd menu items" [PR #46](../00-sources/raw/code/pr-46.md) | high | |
| check | split-check | rare | pr, branch | engineering | The party's bill | "Split check by guest seat" [PR #47](../00-sources/raw/code/pr-47.md) | high | homonym-suspect |

## Seen, not quoted

none

## Out of scope

| term | quote | why it is out |
|---|---|---|
| bookings table | "Add bookings table and customer model" [PR #41](../00-sources/raw/code/pr-41.md) | engineering only: a database table, not a place to sit |
| availability check | "Add availability check before confirming booking" [PR #44](../00-sources/raw/code/pr-44.md) | engineering only: a step inside the app, not a bill |
| guest seat | "Split check by guest seat" [PR #47](../00-sources/raw/code/pr-47.md) | engineering only: the seat number the app stores per guest |
