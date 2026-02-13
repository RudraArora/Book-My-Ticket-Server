from datetime import date, timedelta

from ddf import G
from rest_framework.test import APITestCase

from apps.movie import models as movie_models
from apps.movie import serializers as movie_serializers


class MovieSerializerTest(APITestCase):
    """Tests for MovieSerializer."""

    @classmethod
    def setUpTestData(cls):
        cls.language = G(movie_models.Language, language="hindi")
        cls.genre = G(movie_models.Genre, genre="thriller")
        cls.movie = G(
            movie_models.Movie,
            name="Jawaan",
            description="It is a shah rukh khan movie",
            duration=timedelta(hours=2, minutes=49),
            release_date=date(2025, 11, 16),
            languages=[cls.language],
            genres=[cls.genre],
        )

    def test_movie_serializer_returns_correct_data(self):
        """Serializer should return data for languages and genres."""
        serializer = movie_serializers.MovieSerializer(self.movie)
        data = serializer.data

        self.assertEqual(data["name"], "Jawaan")
        self.assertEqual(data["languages"][0], "hindi")
        self.assertEqual(data["genres"][0], "thriller")

    def test_language_serializer_returns_correct_data(self):
        """Serializer should return correct fields for a language."""
        language = G(movie_models.Language, language="english")
        serializer = movie_serializers.LanguageSerializer(language)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"language"})
        self.assertEqual(data["language"], "english")

    def test_genre_serializer_returns_correct_data(self):
        """Serializer should return correct fields for a genre."""
        genre = G(movie_models.Genre, genre="action")
        serializer = movie_serializers.GenreSerializer(genre)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"genre"})
        self.assertEqual(data["genre"], "action")
