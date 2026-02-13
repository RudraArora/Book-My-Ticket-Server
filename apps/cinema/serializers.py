from rest_framework import serializers

from apps.cinema import models as cinema_models
from apps.movie import models as movie_models
from apps.slot import serializers as slot_serializers


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Location model.

    Handles the conversion of Location model instances to and from
    JSON representations for API transport.
    """

    class Meta:
        model = cinema_models.Location
        fields = ["city"]


class CinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cinema model.

    Handles the conversion of Cinema model instances to and from
    JSON representations for API transport.
    """

    location = serializers.SlugRelatedField(slug_field="city", read_only=True)

    class Meta:
        model = cinema_models.Cinema
        fields = ["id", "name", "location", "rows", "seats_per_row", "slug"]


class CinemaMovieSlotSerializer(serializers.ModelSerializer):
    """
    Serializer for CinemaMovieSlots.
    Convert python objects to/from JSON, and also add
    'slots' field in movie model (by reverse relation).
    """

    slots = slot_serializers.SlotSerializer(many=True)
    languages = serializers.SlugRelatedField(
        many=True, slug_field="language", read_only=True
    )

    class Meta:
        model = movie_models.Movie
        fields = ["id", "name", "languages", "duration", "slots"]


class MovieCinemaSlotSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(slug_field="city", read_only=True)
    slots = slot_serializers.SlotSerializer(many=True)

    class Meta:
        model = cinema_models.Cinema
        fields = ["id", "name", "location", "rows", "seats_per_row", "slots"]
