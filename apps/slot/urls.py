from django.urls import path

from apps.slot import views as slot_views

urlpatterns = [
    path(
        "<int:slot_id>/seats/",
        slot_views.SeatAvailabilityView.as_view(),
        name="available_seats",
    ),
    path(
        "<int:slot_id>/bookings/",
        slot_views.BookingViewSet.as_view(
            {
                "post": "create",
            }
        ),
        name="booking_seat",
    ),
    path(
        "bookings/<int:booking_id>/",
        slot_views.BookingViewSet.as_view(
            {
                "patch": "partial_update",
            }
        ),
        name="booking_cancel",
    ),
]
