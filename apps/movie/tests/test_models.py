from datetime import date, timedelta

from ddf import G
from django.test import TestCase
from django.utils.text import slugify

from apps.movie import models as movie_models


class MovieModelsTest(TestCase):
    """Tests for the Language model."""

    @classmethod
    def setUpTestData(cls):
        cls.language_model = G(movie_models.Language, language="english")
        cls.genre_model = G(movie_models.Genre, genre="thriller")

        cls.movie_data = {
            "name": "Jawaan",
            "description": "It is a shah rukh khan movie",
            "duration": timedelta(hours=3),
            "release_date": date(2025, 11, 1),
            "languages": [cls.language_model],
            "genres": [cls.genre_model],
        }
        cls.movie_model = G(movie_models.Movie, **cls.movie_data)

    def test_language_mode(self):
        """
        Testing language model
        """
        self.assertEqual(self.language_model.language, "english")

    def test_genre_model(self):
        """
        Testing genre model
        """
        self.assertEqual(self.genre_model.genre, "thriller")

    def test_movie_model(self):
        """
        Testing movie model
        """
        self.assertEqual(self.movie_model.name, self.movie_data["name"])
        self.assertEqual(self.movie_model.description, self.movie_data["description"])
        self.assertEqual(self.movie_model.duration, self.movie_data["duration"])
        self.assertEqual(self.movie_model.release_date, self.movie_data["release_date"])

    def test_language_is_lowercased_and_stripped_on_save(self):
        """
        Testing language is lowercased and whitespaces are removed on save
        """
        language_model = G(movie_models.Language, language="  Hindi  ")
        self.assertEqual(language_model.language, "hindi")

    def test_genre_is_lowercased_and_stripped_on_save(self):
        """
        Testing genre is lowercased and whitespaces are removed on save
        """
        genre_model = G(movie_models.Genre, genre="  Action  ")
        self.assertEqual(genre_model.genre, "action")

    def test_slug_is_generated_from_name(self):
        """
        Slug will be auto-generated from name.
        """
        self.assertEqual(self.movie_model.slug, slugify(self.movie_model.name))
