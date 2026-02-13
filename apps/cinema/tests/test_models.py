from datetime import date, timedelta

from ddf import G
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.cinema import models as cinema_models
from apps.movie import models as movie_models

User = get_user_model()


class CinemaModelsTest(TestCase):
    """
    Testcases for Cinema Models
    """

    @classmethod
    def setUpTestData(cls):
        cls.location_data = {"city": "delhi"}
        cls.location = G(cinema_models.Location, **cls.location_data)

        cls.cinema_data = {
            "name": "PVR",
            "location": cls.location,
            "rows": 5,
            "seats_per_row": 5,
        }
        cls.cinema = G(cinema_models.Cinema, **cls.cinema_data)

        cls.movie_data = {
            "name": "jawaan",
            "description": "It is a shah rukh khan movie",
            "duration": timedelta(hours=3),
            "release_date": date(2025, 11, 1),
        }
        cls.movie = G(movie_models.Movie, **cls.movie_data)

        cls.slot_data = {
            "cinema": cls.cinema,
            "movie": cls.movie,
            "start_time": timezone.now() + timedelta(days=2),
            "price": 200,
        }
        cls.slot = G(cinema_models.Slot, **cls.slot_data)

        cls.user_data = {
            "email": "rudra@gmail.com",
            "name": "rudra",
            "phone_number": "1234567890",
            "password": "Rudra@261204",
        }
        cls.user = G(User, **cls.user_data)

        cls.booking_data = {"status": "B", "user": cls.user, "slot": cls.slot}
        cls.booking = G(cinema_models.Booking, **cls.booking_data)

        cls.cinema_seat = cinema_models.CinemaSeat.objects.filter(
            cinema_id=cls.cinema.id
        )

        cls.booking_seat = {"cinema_seat": cls.cinema_seat, "booking": cls.booking}

    def test_location_model(self):
        """
        Testing location model
        """
        self.assertEqual(self.location.city, self.location_data["city"])

    def test_cinema_model(self):
        """
        Testing cinema model
        """
        self.assertEqual(self.cinema.name, self.cinema_data["name"])
        self.assertEqual(self.cinema.location, self.cinema_data["location"])
        self.assertEqual(self.cinema.rows, self.cinema_data["rows"])
        self.assertEqual(self.cinema.seats_per_row, self.cinema_data["seats_per_row"])
        self.assertTrue(self.cinema.slug)

    def test_cinema_seat_model(self):
        """
        Testing cinema_seat model
        """
        self.assertTrue(self.cinema_seat)

    def test_slot_model(self):
        """
        Testing slot model
        """
        self.assertEqual(self.slot.start_time, self.slot_data["start_time"])
        self.assertEqual(self.slot.price, self.slot_data["price"])

    def test_booking_model(self):
        """
        Testing booking model
        """
        self.assertEqual(self.booking.status, self.booking_data["status"])

    def test_booking_seat_model(self):
        """
        Testing booking_seat model
        """
        self.assertTrue(self.booking_seat)
