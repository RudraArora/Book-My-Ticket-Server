from datetime import datetime

from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import exceptions, generics

from apps.cinema import models as cinema_models, serializers as cinema_serializers
from apps.common import pagination as common_pagination
from apps.movie import (
    constants as movie_constants,
    filters as movie_filters,
    models as movie_models,
    serializers as movie_serializers,
)
from apps.slot import models as slot_models


class MoviesView(generics.ListAPIView):
    """
    Movies view to fetch all movies or filter them on the basis of params
    """

    serializer_class = movie_serializers.MovieSerializer
    pagination_class = common_pagination.CustomCursorPagination

    def get_queryset(self):
        valid_slots = slot_models.Slot.objects.filter(end_time__gte=timezone.now())

        queryset = movie_models.Movie.objects.filter(
            slot__end_time__gte=timezone.now()
        ).prefetch_related(
            "languages", "genres", Prefetch("slot_set", queryset=valid_slots)
        )

        manager = movie_filters.MovieFilteringManager()

        return manager.apply_filters(self.request, queryset).distinct()


class MovieSpecificView(generics.RetrieveAPIView):
    """
    Specific movie view
    """

    queryset = movie_models.Movie.objects.all()
    serializer_class = movie_serializers.MovieSerializer
    lookup_field = "slug"


class GenresView(generics.ListAPIView):
    """
    All genres view
    """

    queryset = movie_models.Genre.objects.all()
    serializer_class = movie_serializers.GenreSerializer


class LanguageView(generics.ListAPIView):
    """
    All languages view
    """

    queryset = movie_models.Language.objects.all()
    serializer_class = movie_serializers.LanguageSerializer


class MovieCinemaSlotView(generics.ListAPIView):
    """
    View for finding all the slots for a specific movie
    """

    serializer_class = cinema_serializers.MovieCinemaSlotSerializer

    def get_queryset(self):
        """
        Function which filter the slots of given date.
        then attach them in their respective cinema data.
        """

        movie_id = self.kwargs["movie_id"]

        date = self.request.query_params.get("date")

        if not date:
            raise exceptions.ValidationError(
                movie_constants.ErrorMessage.DATE_PARAM_REQUIRED
            )
        else:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise exceptions.ValidationError(
                    movie_constants.ErrorMessage.INVALID_DATE_FORMAT
                )

        if not movie_models.Movie.objects.filter(id=movie_id).exists():
            raise exceptions.NotFound(movie_constants.ErrorMessage.MOVIE_NOT_EXIST)

        now = timezone.now()

        if now.date() == date:
            slots_qs = slot_models.Slot.objects.filter(
                movie_id=movie_id,
                start_time__gte=now,
                start_time__date=date,
            )
        else:
            slots_qs = slot_models.Slot.objects.filter(
                movie_id=movie_id, start_time__date=date
            )

        return (
            cinema_models.Cinema.objects.filter(slot__in=slots_qs)
            .distinct()
            .prefetch_related(Prefetch("slot_set", queryset=slots_qs, to_attr="slots"))
        )
