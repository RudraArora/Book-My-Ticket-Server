from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.slot import models as slot_models, constants as slot_constants
from apps.cinema import models as cinema_models


class SeatAvailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for seat availaiblity.

    Handles the conversion of Cinema Seat model instances to and from
    JSON representations.
    """

    available = serializers.BooleanField()

    class Meta:
        model = cinema_models.CinemaSeat
        fields = [
            "id",
            "row_number",
            "seat_number",
            "available",
        ]


class BookingSeatSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a seat booking.
    - Validates seat IDs, slot existence, and booking conflicts.
    - Creates Booking and BookingSeat entries on success.
    """

    seat_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate(self, attrs):
        slot_id = self.context["view"].kwargs.get("slot_id")
        seat_ids = attrs.get("seat_ids")

        try:
            slot = slot_models.Slot.objects.get(id=slot_id)
        except slot_models.Slot.DoesNotExist:
            raise NotFound(slot_constants.ErrorMessage.SLOT_NOT_FOUND)

        valid_seats = cinema_models.CinemaSeat.objects.filter(id__in=seat_ids).filter(
            cinema_id=slot.cinema
        )

        if valid_seats.count() != len(seat_ids):
            raise ValidationError(slot_constants.ErrorMessage.INVALID_SEAT)

        booked_seats = slot_models.BookingSeat.objects.filter(
            booking__slot_id=slot_id,
            cinema_seat__in=seat_ids,
            booking__status=slot_constants.BookingStatus.BOOKED.value,
        )

        if booked_seats:
            raise ValidationError(
                    slot_constants.ErrorMessage.BOOKED_SEAT,
            )

        if slot.start_time < timezone.now():
            raise PermissionDenied(slot_constants.ErrorMessage.PAST_BOOKING_BOOKED)

        attrs["slot"] = slot
        return super().validate(attrs)

    class Meta:
        model = slot_models.Booking
        fields = ["id", "seat_ids"]

    def create(self, validated_data):
        slot = validated_data["slot"]
        booking = slot_models.Booking.objects.create(
            user=self.context["request"].user,
            slot=slot,
            status=slot_constants.BookingStatus.BOOKED.value,
        )

        seat_ids = validated_data["seat_ids"]
        booking_seats = [
            slot_models.BookingSeat(cinema_seat_id=seat_id, booking=booking)
            for seat_id in seat_ids
        ]

        slot_models.BookingSeat.objects.bulk_create(booking_seats)
        return booking


class BookingCancelSerializer(serializers.Serializer):
    """
    Serializer for cancelling a booking.
    Validates:
    - Booking exists
    - Booking belongs to the logged-in user
    - Booking is not already cancelled
    """

    def validate(self, attrs):
        booking_id = self.context["view"].kwargs["booking_id"]
        user = self.context["request"].user
        # Check if booking exists
        try:
            booking = slot_models.Booking.objects.get(id=booking_id, user_id=user.id)
        except slot_models.Booking.DoesNotExist:
            raise ValidationError(slot_constants.ErrorMessage.BOOKING_NOT_EXIST)

        if booking.status == slot_constants.BookingStatus.CANCELLED.value:
            raise ValidationError(slot_constants.ErrorMessage.BOOKING_CANCEL)

        if booking.slot.start_time < timezone.now():
            raise PermissionDenied(slot_constants.ErrorMessage.PAST_BOOKING)

        attrs["booking"] = booking
        return attrs

    def create(self, validated_data):
        booking = validated_data["booking"]
        booking.status = slot_constants.BookingStatus.CANCELLED.value
        booking.save()
        return booking


class SlotSerializer(serializers.ModelSerializer):
    """
    Serializer for Slot Model.
    Converts slot model instances to/from JSON.
    """

    class Meta:
        model = slot_models.Slot
        fields = [
            "id",
            "start_time",
            "end_time",
            "price",
        ]
