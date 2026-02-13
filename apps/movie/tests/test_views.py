from datetime import date, timedelta

from ddf import G
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.movie import models as movie_models


class MovieViewTests(APITestCase):
    """Tests for MovieView and related movie APIs."""

    @classmethod
    def setUpTestData(cls):
        # movie base data
        cls.language_model_tamil = G(movie_models.Language, language="tamil")
        cls.language_model_hindi = G(movie_models.Language, language="hindi")

        cls.genre_model_drama = G(movie_models.Genre, genre="drama")
        cls.genre_model_action = G(movie_models.Genre, genre="action")

        # Old movie
        cls.old_movie_data = {
            "name": "Jawaan",
            "description": "It is a shah rukh khan movie",
            "duration": timedelta(hours=2),
            "release_date": date(2025, 11, 2),
            "languages": [cls.language_model_tamil],
            "genres": [cls.genre_model_drama],
        }

        # New (latest) movie released within 7 days
        cls.new_movie_data = {
            "name": "Dangal",
            "description": "It is a amir khan movie",
            "duration": timedelta(hours=3),
            "release_date": timezone.now() - timedelta(days=2),
            "languages": [cls.language_model_hindi],
            "genres": [cls.genre_model_action],
        }

        cls.old_movie = G(movie_models.Movie, **cls.old_movie_data)
        cls.new_movie = G(movie_models.Movie, **cls.new_movie_data)

    def test_all_movies_list(self):
        """GET /movies/ should return a list of all movies."""
        url = reverse("movies")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_all_genres_list(self):
        url = reverse("genres")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_all_languages_list(self):
        url = reverse("languages")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_specific_movie_by_slug(self):
        """GET /movies/<slug>/ should return correct movie details."""
        url = reverse("specific_movie", kwargs={"slug": self.old_movie.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.old_movie_data["name"])

    def test_filter_movies_by_language(self):
        """GET /movies/?language=hindi should return Hindi movie."""
        url = reverse("movies") + "?language=hindi"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["name"], self.new_movie_data["name"]
        )

    def test_filter_movies_by_genre(self):
        """GET /movies/?genre=drama should return Drama movie only."""
        url = reverse("movies") + "?genre=drama"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["name"], self.old_movie_data["name"]
        )

    def test_filter_movies_by_language_and_genre(self):
        """GET /movies/?language=tamil&genre=drama should combine filters."""
        url = reverse("movies") + "?language=tamil&genre=drama"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["name"], self.old_movie_data["name"]
        )

    def test_filter_latest_movies(self):
        """GET /movies/?latest=true should return only movies released in last 7 days."""
        url = reverse("movies") + "?latest=true"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movie_names = [movie["name"] for movie in response.data["results"]]

        # Only new movie is recent
        self.assertIn(self.new_movie_data["name"], movie_names)
        self.assertNotIn(self.old_movie_data["name"], movie_names)
