# Booking Lab Evidence Record

**Name:** Rarinthorn Sirivallop

**Student ID:** 6580229

**Repository:** https://github.com/reneesirivallop/iccs471-booking-lab-Rarinthorn-Sir.git

## Goal
To change overlap-rejection in the feature

## Constraints / Out of Scope
The files that have been changed are booking.py and test_booking.py. Thr behavior that had to remain intact are all original tests, and creation order.

## Key Decision and Agent Claim
 
The overlap check logic part using interval intersection (start < existing.end and existing.start < end) is placed before the booking is added to ensure that invalid bookings never enter the list. After review Copilot's plan, I decided to accept the change because its logic catches all types of overlaps while allowing back-to-back bookings.

## Verification: Claim → Evidence
- **Claim:** The system rejects overlapping bookings in the same room but allows adjacent bookings and same-time bookings in different rooms.
- **Command or test I ran:** 
```
uv run python -m unittest tests.test_booking -v 
```
- **Actual result:** 
```
test_allows_adjacent_same_room_and_overlapping_other_rooms (tests.test_booking.BookingServiceTests.test_allows_adjacent_same_room_and_overlapping_other_rooms) ... ok
test_bookings_remain_in_creation_order (tests.test_booking.BookingServiceTests.test_bookings_remain_in_creation_order) ... ok
test_create_and_list_booking (tests.test_booking.BookingServiceTests.test_create_and_list_booking) ... ok
test_rejects_blank_room_or_guest (tests.test_booking.BookingServiceTests.test_rejects_blank_room_or_guest) ... ok
test_rejects_invalid_time_range (tests.test_booking.BookingServiceTests.test_rejects_invalid_time_range) ... ok
test_rejects_same_room_overlap (tests.test_booking.BookingServiceTests.test_rejects_same_room_overlap) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.000s

OK
```
- **What this supports:** proving the new logic works exactly as intended. The passing tests test_rejects_same_room_overlap and test_allows_adjacent_same_room_and_overlapping_other_rooms confirm that same-room conflicts are correctly blocked, while valid adjacent and different-room bookings are successful.

## Manual Validation
Running demo.py confirmed the overlap bug is fixed. The script explicitly reported the overlapping booking in Room A as rejected and showed exactly 3 stored bookings instead of the baseline's 4. This proved the new logic correctly blocks same-room conflicts in practice without accidentally persisting the failed attempt, while still verifying that adjacent times and different rooms function normally.

## Remaining Uncertainty
Because room names are evaluated as exact strings without normalization, the system remains vulnerable to casing and whitespace inconsistencies. The tests do not establish whether a user booking "Room A" and another booking "room a" or "Room A " would be correctly identified as the same room, meaning double-bookings could still occur through simple typos.