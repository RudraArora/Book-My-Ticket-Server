from datetime import timedelta

from ddf import G
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.cinema import models as cinema_models
from apps.movie import models as movie_models

User = get_user_model()


class CinemaViewTests(APITestCase):
    """
    Test for Cinema Views
    """

    @classmethod
    def setUpTestData(cls):
        cls.location = G(cinema_models.Location, city="testcity")
        cls.cinema = G(
            cinema_models.Cinema,
            name="Test Cinema",
            location=cls.location,
            rows=2,
            seats_per_row=3,
        )

        cls.movie = G(
            movie_models.Movie,
            name="Test Movie",
            duration=timedelta(hours=2),
            release_date=timezone.now().date() - timedelta(days=1),
        )

        cls.slot = G(
            cinema_models.Slot,
            cinema=cls.cinema,
            movie=cls.movie,
            start_time=timezone.now() + timedelta(days=2),
            price=100.00,
        )

        cls.user = G(User, email="test@gmail.com", password="Test@123")

    def test_cinema_list(self):
        """
        Ensure the cinema list endpoint returns 200 OK.
        """
        url = reverse("cinemas")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cinema_detail(self):
        """
        Ensure cinema detail endpoint returns valid data and 200 OK.
        """
        url = reverse("cinema_detail", args=[self.cinema.slug])
        response = self.client.get(url)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_list(self):
        """
        Ensure location list returns 200 OK and includes created location.
        """
        url = reverse("locations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0].get("city"), self.location.city)

    def test_seat_availability(self):
        """
        Ensure seat availability endpoint returns a list of seats
        and includes availability information.
        """
        url = reverse("available_seats", args=[str(self.cinema.id), str(self.slot.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertIn("available", response.data[0])

    def test_cinema_movie_slots(self):
        """
        Ensure cinema movie slots endpoint returns slot data (200 OK)
        without date filter.
        """
        url = reverse("cinema_movie_slots", args=[self.cinema.id]) + "?date=2025-11-27"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_cinema_movie_slots_with_date_filter(self):
        """
        Ensure cinema movie slots endpoint works with a valid date filter.
        """
        url = (
            reverse("cinema_movie_slots", args=[str(self.cinema.id)])
            + "?date=2025-11-22"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_cinema_movie_slots_with_invalid_date_filter(self):
        """
        Ensure passing an invalid date format returns 400 BAD REQUEST.
        """
        url = (
            reverse("cinema_movie_slots", args=[str(self.cinema.id)])
            + "?date=19-11-2025"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_booking_ticket(self):
        """
        Ensure a user can successfully book a ticket
        when authenticated and valid seat is provided.
        """
        self.client.force_authenticate(user=self.user)
        real_seat = cinema_models.CinemaSeat.objects.filter(
            cinema_id=self.cinema
        ).first()
        booking_url = reverse("booking_seat", args=[str(self.slot.id)])
        response = self.client.post(
            booking_url, {"status": "B", "seat_ids": [real_seat.id]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_booking_cancel(self):
        """
        Ensure a user can cancel an existing booking
        """
        self.client.force_authenticate(user=self.user)
        seat = cinema_models.CinemaSeat.objects.filter(cinema_id=self.cinema).first()
        booking_url = reverse("booking_seat", args=[self.slot.id])
        res = self.client.post(
            booking_url, {"status": "B", "seat_ids": [seat.id]}, format="json"
        )
        booking_id = res.data["id"]
        cancel_url = reverse("booking_cancel", args=[booking_id])
        response = self.client.patch(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_booking_and_cancel_require_auth(self):
        """
        Ensure booking and cancellation endpoints require authentication.
        Should return 401 UNAUTHORIZED for unauthenticated requests.
        """
        booking_url = reverse("booking_seat", args=[str(self.slot.id)])
        cancel_url = reverse("booking_cancel", args=[str(1)])

        response = self.client.post(booking_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_purchase_history_requires_auth_and_returns_empty_data_after_authentication(
        self,
    ):
        """
        Ensure purchase history:
        - Returns 401 UNAUTHORIZED when unauthenticated
        - Returns 200 OK and empty list (no purchases) when authenticated
        """
        url = reverse("purchase_history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if "results" in response.data:
            items = response.data["results"]
        else:
            items = response.data
        self.assertEqual(len(items), 0)
