from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers

from apps.user import constants as user_constants
from apps.slot import models as slot_models

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for handling the user signup data

    - It validates the user's phone number and password using regex.
    - It ensures that email, phone number, and name are properly captured.
    - It uses the `create_user()` method from the custom `UserManager` to create a new user.
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        """
        class that defines the fields of the model to be serialized
        """

        model = User
        fields = ("name", "email", "phone_number", "password", "confirm_password")

    def validate(self, attrs):
        password1 = attrs["password"]
        password2 = attrs.pop("confirm_password")

        if password1 != password2:
            raise exceptions.ValidationError(
                {"message": user_constants.ErrorMessage.PASSWORD_NOT_MATCH}
            )

        return attrs

    def validate_email(self, value):
        """
        Validating Email to avoid integrity error
        """
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError(
                user_constants.ErrorMessage.EMAIL_ALREADY_EXIST
            )
        return lower_email

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data=validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    To serialize user data to and from JSON
    """

    class Meta:
        model = User
        fields = ["name", "email", "phone_number"]
        extra_kwargs = {"email": {"read_only": True}}


class PurchaseHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user's purchase history.
    Includes:
    - Detailed slot info
    - List of booked seats
    - Total booking price
    """

    seats = serializers.SerializerMethodField()
    slot = serializers.SerializerMethodField()

    def get_seats(self, obj):
        return [
            {
                "row": seat.cinema_seat.row_number,
                "seat": seat.cinema_seat.seat_number,
            }
            for seat in obj.seats.all()
        ]

    def get_slot(self, obj):
        slot = obj.slot
        return [
            {
                "cinema": slot.cinema.name,
                "location": slot.cinema.location.city,
                "movie": slot.movie.name,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "price": slot.price,
            }
        ]

    class Meta:
        model = slot_models.Booking
        fields = ["id", "status", "created_at", "slot", "seats"]
