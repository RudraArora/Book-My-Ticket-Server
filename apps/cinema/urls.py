from django.urls import path

from apps.cinema import views as cinema_views

urlpatterns = [
    path("", cinema_views.CinemaView.as_view(), name="cinemas"),
    path("locations/", cinema_views.LocationView.as_view(), name="locations"),
    path(
        "<slug:slug>/", cinema_views.CinemaSpecificView.as_view(), name="cinema_detail"
    ),
    path(
        "<int:cinema_id>/slots/",
        cinema_views.CinemaMovieSlotView.as_view(),
        name="cinema_movie_slots",
    ),
]
