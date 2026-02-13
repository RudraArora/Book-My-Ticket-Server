from apps.cinema import constants as cinema_constants
from apps.common import strategies as common_strategies


class LocationFilterStrategy(common_strategies.FilteringStrategy):
    def apply(self, request, queryset):
        location = request.query_params.get("location")
        if not location:
            return queryset
        return queryset.filter(location__city__iexact=location)


class CinemaFilterManager(common_strategies.FilteringManager):
    def __init__(self):
        strategies = [LocationFilterStrategy()]
        super().__init__(strategies)
