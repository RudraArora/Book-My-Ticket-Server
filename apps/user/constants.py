from enum import Enum


class MaxLength:
    """
    Maximum allowed lengths in the models
    """

    NAME = 100
    PHONE_NUMBER = 10
    EMAIL = 254


class ErrorMessage:
    """
    Error messages
    """

    EMAIL = "Email is required"
    NAME = "Name is required"
    PHONE_NUMBER = "Phone number is required"
    PASSWORD = "Password is required"
    PASSWORD_ERROR = "Password must contain at least one lowercase letter, one uppercase letter, one number and one special character"
    PHONE_NUMBER_LENGTH = "Phone number must be exactly 10 digits"
    EMAIL_ALREADY_EXIST = "user with this email already exists."
    REFRESH_TOKEN_EXPIRY = "Refresh token not found in cookies"
    REFRESH_TOKEN_NOT_FOUND = "Refresh token not found in cookies"
    LOGIN_INVALID = "No active account found with the given credentials"
    EMAIL_ALREADY_EXIST = "user with this email already exists."
    PHONE_NUMBER_ALREADY_EXIST = "user with this phone number already exists."
    PASSWORD_NOT_MATCH = "Passwords does not match"


class SuccessMessage:
    """
    Success messages.
    """

    USER_CREATED = "User registered successfully"


class ErrorCodes:
    """
    Constants for error codes
    """

    PASSWORD_ERROR = "invalid-password"
    MOBILE_ERROR = "invalid-phone-number"


class PurchaseParam(Enum):
    CANCEL = "cancel"
    PAST = "past"
    UPCOMING = "upcoming"


class BookingStatus(Enum):
    BOOKED = "B"
    CANCELLED = "C"
