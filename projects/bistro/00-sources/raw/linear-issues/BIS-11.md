Title: BIS-11 Booking form: let customers pick a party size up to 12 · Link: EXAMPLE-not-a-real-link · Pulled: 2026-09-02

# BIS-11 Booking form: let customers pick a party size up to 12

Team: BIS · Reporter: Priya · Labels: booking, web · Status: Done

## Description

Customers can only book for up to 8 today. Raise the party size limit to 12. A booking for 9 or
more needs two tables pushed together, so the availability check must look for two free tables
side by side.

Linked PR: #41 "Add bookings table and customer model" (branch `priya/bis-11-booking-form`)
Linked PR: #44 "Add availability check before confirming booking" (branch `priya/bis-11-availability-check`)

## Comments

Theo: On the floor we call these reservations, not bookings. Fine in the code, but the screen the
host sees should say reservation.
