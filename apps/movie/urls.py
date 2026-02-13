from django.urls import path

from apps.movie import views as movie_views

urlpatterns = [
    path("", movie_views.MoviesView.as_view(), name="movies"),
    path("genres/", movie_views.GenresView.as_view(), name="genres"),
    path("languages/", movie_views.LanguageView.as_view(), name="languages"),
    path(
        "<slug:slug>/", movie_views.MovieSpecificView.as_view(), name="specific_movie"
    ),
    path(
        "<int:movie_id>/slots/",
        movie_views.MovieCinemaSlotView.as_view(),
        name="movie_cinema_slots",
    ),
]
