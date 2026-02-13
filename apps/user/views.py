from django.contrib.auth import get_user_model, models
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from apps.user import serializers as user_serializers, filters as user_filters
from apps.common import pagination as common_pagination
from apps.slot import models as slot_models


User = get_user_model()


class SignupView(generics.CreateAPIView):
    """
    Class based view for the Signup API
    """

    serializer_class = user_serializers.SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = tokens.RefreshToken.for_user(user)

        models.update_last_login(None, user)

        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
        )


class UserView(generics.RetrieveUpdateAPIView):
    """
    User view for fetching details of a user and updating basic details of a user
    """

    serializer_class = user_serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    # Overridden http methods
    http_method_names = [
        "get",
        "patch",
        # HTTP method requests the metadata of a resource
        "head",
        #  HTTP method requests permitted communication options for a given URL
        "options",
    ]

    def get_object(self):
        # Returns the authenticated user
        return self.request.user


class PurchaseHistoryView(generics.ListAPIView):
    """
    View for retrieving the purchase history for a user
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = user_serializers.PurchaseHistorySerializer
    pagination_class = common_pagination.CustomCursorPagination

    def get_queryset(self):
        user = self.request.user
        queryset = (
            slot_models.Booking.objects.filter(user=user)
            .select_related("slot", "slot__cinema__location")
            .prefetch_related("seats")
        )

        manager = user_filters.PurchaseHistoryFilterManager()

        return manager.apply_filters(self.request, queryset)
