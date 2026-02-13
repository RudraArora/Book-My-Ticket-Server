from django.contrib import admin

from apps.slot import models as slot_models


class BookingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(slot_models.Booking, BookingAdmin)
admin.site.register(slot_models.BookingSeat, BookingAdmin)
admin.site.register(slot_models.Slot)
