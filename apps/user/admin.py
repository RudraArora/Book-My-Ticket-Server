from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.user import models as user_models


class CustomUserAdmin(BaseUserAdmin):
    """
    Custom User Admin that displays data using email and is_staff,
    allows filtering by is_staff and is_superuser field
    and defines custom fields while adding user.
    """

    model = user_models.User
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("name", "email", "password", "phone_number")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "password1",
                    "password2",
                    "phone_number",
                    "is_staff",
                ),
            },
        ),
    )


admin.site.register(user_models.User, CustomUserAdmin)
