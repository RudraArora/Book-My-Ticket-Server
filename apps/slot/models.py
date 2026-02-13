from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models as db_models
from django.utils import timezone

from apps.cinema import models as cinema_models
from apps.common import models as common_models
from apps.movie import models as movie_models

from apps.slot import constants as slot_constants

User = get_user_model()


class Slot(common_models.TimeStampModel):
    """
    Represents a showtime for a movie in a cinema.
    - Stores date, start time and ticket price.
    - Validates that the slot is not in the past and does not overlap with other slots in the same cinema.
    """

    cinema = db_models.ForeignKey(cinema_models.Cinema, on_delete=db_models.CASCADE)
    movie = db_models.ForeignKey(movie_models.Movie, on_delete=db_models.CASCADE)
    start_time = db_models.DateTimeField(help_text=slot_constants.HelpText.START_TIME)
    end_time = db_models.DateTimeField(
        blank=True, help_text=slot_constants.HelpText.AUTO_GENERATE
    )
    price = db_models.DecimalField(max_digits=8, decimal_places=2)

    def clean(self):
        self.end_time = self.start_time + self.movie.duration

        if self.start_time <= timezone.now():
            raise ValidationError(slot_constants.ErrorMessage.SLOT_PAST_SCHEDULE)

        if self.start_time.date() < self.movie.release_date:
            raise ValidationError(slot_constants.ErrorMessage.INVALID_SLOT_DATE)

        overlapping_slots = Slot.objects.filter(
            db_models.Q(
                start_time__lte=self.start_time,
                end_time__gte=self.start_time,
                cinema=self.cinema,
            )
            | db_models.Q(
                start_time__lte=self.end_time,
                end_time__gte=self.end_time,
                cinema=self.cinema,
            )
        )

        if overlapping_slots.exists():
            raise ValidationError(slot_constants.ErrorMessage.SLOT_OVERLAPS)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.name}-{self.cinema.name}-{self.start_time}"


class Booking(common_models.TimeStampModel):
    """
    Represents a user's booking for a slot.
    - Stores booking status (Booked/Cancelled).
    - Linked to a user and a slot.
    """

    SEAT_STATUS_CHOICES = [("B", "Booked"), ("C", "Cancelled")]
    status = db_models.CharField(max_length=1, choices=SEAT_STATUS_CHOICES)
    user = db_models.ForeignKey(User, on_delete=db_models.CASCADE)
    slot = db_models.ForeignKey(Slot, on_delete=db_models.CASCADE)

    def __str__(self):
        return f"{self.user.name}-{self.slot.cinema.slug}-{self.slot.movie.slug}"


class BookingSeat(common_models.TimeStampModel):
    """
    Represents an individual seat under a booking.
    - Connects a booking to a specific cinema seat.
    """

    cinema_seat = db_models.ForeignKey(
        cinema_models.CinemaSeat, on_delete=db_models.CASCADE
    )
    booking = db_models.ForeignKey(
        Booking, on_delete=db_models.CASCADE, null=True, related_name="seats"
    )

    def __str__(self):
        return f"{self.cinema_seat}"
