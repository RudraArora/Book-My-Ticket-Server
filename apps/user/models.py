from django.contrib.auth import models as auth_models
from django.db import models as db_models

from apps.common import models as common_models
from apps.user import constants as user_constants
from apps.user import managers
from apps.user import validators as user_validators


class User(
    auth_models.AbstractBaseUser,
    auth_models.PermissionsMixin,
    common_models.TimeStampModel,
):
    """
    Custom user model made on the top of Django AbstractUser

    It uses email as the identifier for authentication

    Attributes
    ----------
    name : str
        Name of the user (default: 'Guest')
    email : str
        Unique email address for the authentication
    phone_number : str
        Unique 10-digit phone number
    """

    name = db_models.CharField(max_length=user_constants.MaxLength.NAME)
    phone_number = db_models.CharField(
        max_length=user_constants.MaxLength.PHONE_NUMBER,
        unique=True,
        validators=[user_validators.phone_number_validator],
    )
    email = db_models.EmailField(
        blank=False, unique=True, max_length=user_constants.MaxLength.EMAIL
    )
    is_staff = db_models.BooleanField(default=False)
    objects = managers.UserManager()

    # Setting authentication field to 'email'
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_number"]

    def __str__(self):
        return self.name
