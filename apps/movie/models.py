import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models as db_models
from django.utils.text import slugify

from apps.common import models as common_models
from apps.movie import constants as movie_constants


class Genre(db_models.Model):
    """
    Model used to represent a genre

    This model stores different genre in lowercase
    to maintain consistency across records

    Attributes:
    -----------
        genre (str): the name of the genre
    """

    genre = db_models.CharField(max_length=movie_constants.MaxLength.GENRE, unique=True)

    def clean(self):
        self.genre = self.genre.lower().strip()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.genre


class Language(db_models.Model):
    """
    Model used to represent a language

    This model stores different languages in lowercase
    to maintain consistency across records

    Attributes:
    -----------
        language (str): the name of the language
    """

    language = db_models.CharField(
        max_length=movie_constants.MaxLength.LANGUAGE, unique=True
    )

    def clean(self):
        self.language = self.language.lower().strip()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.language


class Movie(common_models.TimeStampModel):
    """
    A Movie model used to represent a movie in a  database

    Attributes:
    -----------
        name (str): The name of the movie
        description (text): A brief description of the movie
        duration (time) :  The total runtime of the movie
        release_date (date): The release date of the movie
        languages (list[Language]) : The set of languages in
        which movie is available
        genre (list[Genre]): The set of genres the movie is classified as
        slug (str): A unique, URL - friendly identifier automatically generated from the movie's name
    """

    name = db_models.CharField(max_length=movie_constants.MaxLength.NAME, unique=True)
    description = db_models.TextField()
    duration = db_models.DurationField(
        validators=[
            MinValueValidator(
                datetime.timedelta(minutes=movie_constants.MaxLength.DURATION_MINUTES)
            ),
            MaxValueValidator(
                datetime.timedelta(hours=movie_constants.MaxLength.DURATION_HOURS)
            ),
        ],
        max_length=movie_constants.MaxLength.DURATION,
        help_text=movie_constants.HelpText.DURATION,
    )
    release_date = db_models.DateField(help_text=movie_constants.HelpText.RELEASE_DATE)
    languages = db_models.ManyToManyField("Language")
    genres = db_models.ManyToManyField("Genre")
    slug = db_models.SlugField(
        unique=True,
        blank=True,
        max_length=movie_constants.MaxLength.SLUG,
        help_text=movie_constants.HelpText.SLUG,
    )

    def clean(self):
        self.slug = slugify(self.name)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
