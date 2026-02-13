from datetime import date, timedelta

from ddf import G
from django.contrib.auth import get_user_model
from django.utils import text, timezone
from rest_framework.fields import DateTimeField
from rest_framework.test import APITestCase

from apps.cinema import models as cinema_models
from apps.cinema import serializers as cinema_serializers
from apps.movie import models as movie_models

User = get_user_model()


class CinemaSerializersTest(APITestCase):
    """
    Tests for the Cinema serializers
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
            "slug": text.slugify(f"{'PVR'}-{cls.location}"),
        }
        cls.cinema = G(cinema_models.Cinema, **cls.cinema_data)

    def test_location_serializer(self):
        """
        Test LocationSerializer:
        - Ensures the serializer correctly returns the city field
        matching the expected location data.
        """
        serializer = cinema_serializers.LocationSerializer(self.location)
        data = serializer.data

        self.assertEqual(data["city"], self.location_data["city"])

    def test_cinema_serializer(self):
        """
        Test CinemaSerializer:
        - Validates that cinema name is serialized correctly
        - Ensures location data is included and correct
        """
        serializer = cinema_serializers.CinemaSerializer(self.cinema)
        data = serializer.data
        expected_data = {
            "id": self.cinema.id,
            "name": self.cinema.name,
            "location": self.cinema.location.city,
            "rows": self.cinema.rows,
            "seats_per_row": self.cinema.seats_per_row,
            "slug": self.cinema.slug,
        }

        self.assertEqual(data, expected_data)
