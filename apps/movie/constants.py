class MaxLength:
    """
    Maximum allowed lengths in the models
    """

    NAME = 200
    SLUG = 200
    LATEST_DAYS = 7
    GENRE = 20
    LANGUAGE = 20
    DURATION = 8
    DURATION_MINUTES = 60
    DURATION_HOURS = 4


class ErrorMessage:
    DURATION = "Enter duration in valid format"
    INVALID_DATE_FORMAT = "Invalid date format (YYYY-MM-DD)."
    DATE_PARAM_REQUIRED = "Date query param is required"
    MOVIE_NOT_EXIST = "Movie with this id doesn't exist."


class ErrorCodes:
    DURATION = "invalid-duration"


class HelpText:
    DURATION = "Enter duration in the HH:MM:SS format"
    RELEASE_DATE = "Enter release date in format YYYY-MM-DD"
    SLUG = "Slug is an auto generated field"


truthy_values = ("true", "1", "t", "yes")
