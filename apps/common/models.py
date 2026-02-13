from django.db import models


class TimeStampModel(models.Model):
    """
    Abstract base model that provides self-updating
    `created_at` and `updated_at` fields.

    This model is inherited by other models
    to automatically include timestamps.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the record was last updated."
    )

    class Meta:
        # Prevents Django from creating a separate database table for this model
        abstract = True
