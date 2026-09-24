import unittest

from booking_app.booking import BookingService


class BookingServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = BookingService()

    def test_create_and_list_booking(self) -> None:
        created = self.service.create_booking("A", 540, 600, "Narin")
        self.assertEqual(created.room, "A")
        self.assertEqual(created.guest, "Narin")
        self.assertEqual(self.service.list_bookings(), (created,))

    def test_bookings_remain_in_creation_order(self) -> None:
        first = self.service.create_booking("A", 540, 600, "Narin")
        second = self.service.create_booking("B", 600, 660, "Mali")
        self.assertEqual(self.service.list_bookings(), (first, second))

    def test_rejects_blank_room_or_guest(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_booking("  ", 540, 600, "Narin")
        with self.assertRaises(ValueError):
            self.service.create_booking("A", 540, 600, "  ")
        self.assertEqual(self.service.list_bookings(), ())

    def test_rejects_same_room_overlap(self) -> None:
        first = self.service.create_booking("A", 540, 600, "Narin")
        with self.assertRaises(ValueError):
            self.service.create_booking("A", 570, 630, "Mali")
        self.assertEqual(self.service.list_bookings(), (first,))

    def test_allows_adjacent_same_room_and_overlapping_other_rooms(self) -> None:
        first = self.service.create_booking("A", 540, 600, "Narin")
        second = self.service.create_booking("A", 600, 660, "Mali")
        cross_room = self.service.create_booking("B", 570, 630, "Korn")
        self.assertEqual(self.service.list_bookings(), (first, second, cross_room))

    def test_rejects_invalid_time_range(self) -> None:
        for start, end in ((600, 600), (660, 600), (-1, 60), (1380, 1441)):
            with self.subTest(start=start, end=end):
                with self.assertRaises(ValueError):
                    self.service.create_booking("A", start, end, "Narin")
        self.assertEqual(self.service.list_bookings(), ())


if __name__ == "__main__":
    unittest.main()
