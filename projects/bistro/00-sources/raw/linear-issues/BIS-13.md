Title: BIS-13 Server timeout when two hosts seat the same table · Link: EXAMPLE-not-a-real-link · Pulled: 2026-09-02

# BIS-13 Server timeout when two hosts seat the same table

Team: BIS · Reporter: Priya · Labels: bug, seating · Status: Done

## Description

Friday 7:10pm: two devices assigned table 12 at the same second. The server timed out on the lock
and every tablet froze for about five minutes.

Linked PR: #43 "Fix server timeout on concurrent table assignment" (branch `priya/bis-13-seat-lock`)

## Comments

Theo: The floor read "server timeout" as one of our servers. Can we not use that word for the
computer in anything staff see?
Priya: Agreed. In the app's messages we'll say "the system". The code keeps its names.
