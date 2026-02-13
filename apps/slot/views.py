from django.db.models import Case, When
from django.utils import timezone
from rest_framework import exceptions, generics, permissions, response, status, viewsets

from django.utils import timezone

from apps.cinema import models as cinema_models
from apps.slot import (
    constants as slot_constants,
    models as slot_models,
    serializers as slot_serializer,
)


class SeatAvailabilityView(generics.ListAPIView):
    """
    View for finding the seat availaibility
    """

    serializer_class = slot_serializer.SeatAvailabilitySerializer

    def get_queryset(self):
        slot_id = self.kwargs["slot_id"]

        slot = slot_models.Slot.objects.filter(id=slot_id)

        if not slot.exists():
            raise exceptions.NotFound(slot_constants.ErrorMessage.SLOT_NOT_FOUND)

        if slot[0].start_time < timezone.now():
            raise exceptions.PermissionDenied(
                slot_constants.ErrorMessage.PAST_SLOT_SEATS
            )

        booked_seats = slot_models.BookingSeat.objects.filter(
            booking__slot_id=slot_id,
            booking__status=slot_constants.BookingStatus.BOOKED.value,
        ).values_list("cinema_seat", flat=True)

        queryset = (
            cinema_models.CinemaSeat.objects.filter(cinema_id_id__slot=slot_id)
            .annotate(
                available=Case(When(id__in=booked_seats, then=False), default=True)
            )
            .select_related("cinema_id")
        )

        return queryset

    def list(self, request, *args, **kwargs):
        slot_id = self.kwargs["slot_id"]
        seats_queryset = self.get_queryset()
        seats_data = self.get_serializer(seats_queryset, many=True).data

        slot = slot_models.Slot.objects.select_related("movie").get(id=slot_id)

        cinema_name = seats_queryset[0].cinema_id.name
        cinema_location = seats_queryset[0].cinema_id.location.city
        cinema_rows = seats_queryset[0].cinema_id.rows
        cinema_seats_per_row = seats_queryset[0].cinema_id.seats_per_row

        return response.Response(
            {
                "cinema": cinema_name,
                "location": cinema_location,
                "rows": cinema_rows,
                "seats_per_row": cinema_seats_per_row,
                "movie": slot.movie.name,
                "slot_price": slot.price,
                "slot_start_time": slot.start_time.astimezone(),
                "seats": seats_data,
            }
        )


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return slot_serializer.BookingCancelSerializer
        elif self.request.method == "POST":
            return slot_serializer.BookingSeatSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        slot_id = self.kwargs["slot_id"]
        slot = slot_models.Slot.objects.select_related("movie", "cinema").get(
            id=slot_id
        )

        booked_seats = slot_models.BookingSeat.objects.select_related(
            "cinema_seat"
        ).filter(booking=booking)

        return response.Response(
            {
                "booking": booking.id,
                "cinema_name": slot.cinema.name,
                "cinema_location": slot.cinema.location.city,
                "movie_name": slot.movie.name,
                "slot_time": slot.start_time,
                "slot_price": slot.price,
                "seats": [
                    {
                        "row": seat.cinema_seat.row_number,
                        "seat": seat.cinema_seat.seat_number,
                    }
                    for seat in booked_seats
                ],
            }
        )

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
