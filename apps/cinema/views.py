from datetime import datetime

from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import exceptions, generics

from apps.cinema import (
    constants as cinema_constants,
)
from apps.cinema import (
    filters as cinema_filters,
)
from apps.cinema import (
    models as cinema_models,
)
from apps.cinema import (
    serializers as cinema_serializers,
)
from apps.common import pagination as common_pagination
from apps.movie import models as movie_models
from apps.slot import models as slot_models


class CinemaView(generics.ListAPIView):
    """
    Cinema list view with location filter
    """

    serializer_class = cinema_serializers.CinemaSerializer
    pagination_class = common_pagination.CustomCursorPagination

    def get_queryset(self):
        queryset = cinema_models.Cinema.objects.select_related("location")
        manager = cinema_filters.CinemaFilterManager()
        return manager.apply_filters(self.request, queryset)


class CinemaSpecificView(generics.RetrieveAPIView):
    """
    Specific cinema view
    """

    queryset = cinema_models.Cinema.objects.all()
    serializer_class = cinema_serializers.CinemaSerializer
    lookup_field = "slug"


class LocationView(generics.ListAPIView):
    """
    Location list View
    """

    queryset = cinema_models.Location.objects.all()
    serializer_class = cinema_serializers.LocationSerializer


class CinemaMovieSlotView(generics.ListAPIView):
    """
    View for finding all the slots for a specific cinema
    """

    serializer_class = cinema_serializers.CinemaMovieSlotSerializer

    def get_queryset(self):
        """
        Function which filter the slots of given date.
        then attach them in their respective cinema data.
        """

        cinema_id = self.kwargs["cinema_id"]

        date = self.request.query_params.get("date")

        if not date:
            raise exceptions.ValidationError(
                cinema_constants.ErrorMessage.DATE_PARAM_REQUIRED
            )
        else:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise exceptions.ValidationError(
                    cinema_constants.ErrorMessage.INVALID_DATE_FORMAT
                )

        if not cinema_models.Cinema.objects.filter(id=cinema_id).exists():
            raise exceptions.NotFound(cinema_constants.ErrorMessage.CINEMA_NOT_EXIST)

        now = timezone.now()

        if now.date() == date:
            slots_qs = slot_models.Slot.objects.filter(
                cinema_id=cinema_id,
                start_time__date=date,
                start_time__time__gte=now.time(),
            )
        else:
            slots_qs = slot_models.Slot.objects.filter(
                cinema_id=cinema_id, start_time__date=date
            )

        return (
            movie_models.Movie.objects.filter(slot__in=slots_qs)
            .distinct()
            .prefetch_related(Prefetch("slot_set", queryset=slots_qs, to_attr="slots"))
        )
