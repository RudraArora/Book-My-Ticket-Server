from rest_framework import serializers

from apps.movie import models as movie_models


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Genre model.

    Handles converting Genre model instances to JSON.
    """

    class Meta:
        model = movie_models.Genre
        fields = ["genre"]


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Language model.

    Handles converting Language model instances to JSON.
    """

    class Meta:
        model = movie_models.Language
        fields = ["language"]


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.

    Handles converting Movie model instances to JSON.
    Includes nested 'languages' and 'genres' data using their
    respective serializers for read operations.
    """

    languages = serializers.SlugRelatedField(
        many=True, slug_field="language", read_only=True
    )
    genres = serializers.SlugRelatedField(many=True, slug_field="genre", read_only=True)

    class Meta:
        model = movie_models.Movie
        fields = [
            "id",
            "name",
            "description",
            "duration",
            "release_date",
            "languages",
            "genres",
            "slug",
        ]
