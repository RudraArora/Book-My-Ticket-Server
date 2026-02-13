from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):
    """
    Custom user model manager used to create superuser
    using email
    """

    def create_superuser(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user
