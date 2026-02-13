import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from apps.user import constants as user_constants

# phone number regex validator
phone_number_validator = RegexValidator(
    regex=r"^\d{10}$",
    message=user_constants.ErrorMessage.PHONE_NUMBER_LENGTH,
    code=user_constants.ErrorCodes.MOBILE_ERROR,
)


class CustomPasswordValidator:
    """
    Validate the password has at least:
        - password must contain one uppercase letter
        - password must contain one lowercase letter
        - password must contain one lowercase letter
        - password must contain one special character
    """

    def validate(self, password, user=None):
        if not re.search(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{0,}$", password
        ):
            raise ValidationError(
                user_constants.ErrorMessage.PASSWORD_ERROR,
                code=user_constants.ErrorCodes.PASSWORD_ERROR,
            )

    def get_help_text(self):
        return user_constants.ErrorMessage.PASSWORD_ERROR
