from enum import Enum


class MaxLength:
    """
    Maximum allowed lengths in the models
    """

    NAME = 200
    LOCATION = 100


class ErrorMessage:
    """
    Error messages for cinema serializers
    """

    INVALID_SEAT = (
        "One or more seat IDs do not exist or does not belong to this cinema."
    )
    BOOKED_SEAT = "One or more seats are already booked."
    BOOKING_NOT_EXIST = "This booking or booking with this user does not exist."
    BOOKING_CANCEL = "This booking is already cancelled."
    SLOT_NOT_FOUND = "Slot with this id doesn`t exist."
    CINEMA_NOT_EXIST = "Cinema with this id doesn't exist."
    SLOT_PAST_SCHEDULE = "Cannot schedule a showtime in the past."
    SLOT_OVERLAPS = (
        "This slot overlaps with another slot in the same cinema on this date."
    )
    INVALID_SLOT_DATE = "Cannot schedule a slot for an unreleased movie."
    INVALID_DATE_FORMAT = "Invalid date format (YYYY-MM-DD)."
    PAST_BOOKING = "Past bookings cannot be cancelled"
    PAST_BOOKING_BOOKED = "Past slots cannot be booked"
    DATE_PARAM_REQUIRED = "Date query param is required"
    SLOT_NOT_BELONG_CINEMA = "Slot does not belong to this cinema"
    PAST_SLOT_SEATS = "Past Slot seats cannot be checked"


class HelpText:
    """
    Help Text for the model fields
    """

    START_TIME = (
        "Enter slot's start date in format YYYY-MM-DD and start time in format HH:MM:SS"
    )
    AUTO_GENERATE = "This field is automatically generated"
    SLUG = "Slug is an auto generated field"


class PurchaseParam(Enum):
    CANCEL = "cancel"
    PAST = "past"
    UPCOMING = "upcoming"


class BookingStatus(Enum):
    BOOKED = "B"
    CANCELLED = "C"
