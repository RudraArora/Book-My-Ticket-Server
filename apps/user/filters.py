from django.utils import timezone

from apps.cinema import constants as cinema_constants
from apps.common import strategies as common_strategies


class PurchaseFilterStrategy(common_strategies.FilteringStrategy):
    """
    Filter cancelled bookings
    """

    def apply(self, request, queryset):
        purchase = request.query_params.get("purchase")
        if not purchase:
            return queryset

        if purchase.lower().strip() == cinema_constants.PurchaseParam.CANCEL.value:
            queryset = queryset.filter(
                status=cinema_constants.BookingStatus.CANCELLED.value
            )

        elif purchase.lower().strip() == cinema_constants.PurchaseParam.UPCOMING.value:
            now = timezone.now()
            queryset = queryset.filter(
                status=cinema_constants.BookingStatus.BOOKED.value,
                slot__start_time__gte=now,
            )

        elif purchase.lower().strip() == cinema_constants.PurchaseParam.PAST.value:
            now = timezone.now()
            queryset = queryset.filter(
                status=cinema_constants.BookingStatus.BOOKED.value,
                slot__start_time__lt=now,
            )

        return queryset


class PurchaseHistoryFilterManager(common_strategies.FilteringManager):
    def __init__(self):
        strategies = [PurchaseFilterStrategy()]
        super().__init__(strategies)
