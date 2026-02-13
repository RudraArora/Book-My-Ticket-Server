from datetime import datetime, timedelta

from apps.common import strategies as common_strategies
from apps.movie import constants as movie_constants


class LanguageFilteringStrategy(common_strategies.FilteringStrategy):
    def apply(self, request, queryset):
        languages = request.GET.getlist("language")
        languages = [lang.strip().lower() for lang in languages if lang.strip()]
        if not languages:
            return queryset

        return queryset.filter(languages__language__in=languages)


class GenreFilteringStrategy(common_strategies.FilteringStrategy):
    def apply(self, request, queryset):
        genres = request.GET.getlist("genre")
        if not genres:
            return queryset

        genres = [genre.strip().lower() for genre in genres if genre.strip()]
        return queryset.filter(genres__genre__in=genres)


class LatestMovieFilteringStrategy(common_strategies.FilteringStrategy):
    def apply(self, request, queryset):
        latest_movie = request.query_params.get("latest")
        truthy_values = movie_constants.truthy_values

        if not latest_movie:
            return queryset

        if latest_movie.strip().lower() in truthy_values:
            today = datetime.now().date()
            latest_time = today - timedelta(days=movie_constants.MaxLength.LATEST_DAYS)
            return queryset.filter(release_date__range=(latest_time, today))

        else:
            return queryset


class MovieFilteringManager(common_strategies.FilteringManager):
    def __init__(self):
        strategies = [
            LanguageFilteringStrategy(),
            GenreFilteringStrategy(),
            LatestMovieFilteringStrategy(),
        ]
        super().__init__(strategies)
