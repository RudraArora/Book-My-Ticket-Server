from django.contrib import admin

from apps.cinema import models as cinema_models


class CinemaModelAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)


class CinemaSeatModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class BookingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(cinema_models.Cinema, CinemaModelAdmin)
admin.site.register(cinema_models.Location)
admin.site.register(cinema_models.CinemaSeat, CinemaSeatModelAdmin)
# admin.site.register(cinema_models.Booking, BookingAdmin)
# admin.site.register(cinema_models.BookingSeat, BookingAdmin)
# admin.site.register(cinema_models.Slot)
