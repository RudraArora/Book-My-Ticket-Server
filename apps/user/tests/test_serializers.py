from ddf import G
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.user import constants as user_constants
from apps.user import serializers as user_serializers

User = get_user_model()


class SignupSerializerTestCase(APITestCase):
    """
    Test case class for testing the serializers
    """

    @classmethod
    def setUpTestData(cls):
        """
        For setting up the data
        """
        cls.user_object_data = {
            "email": "test@gmail.com",
            "name": "test",
            "phone_number": "3333333333",
            "password": "Test@1234",
        }

        cls.valid_data = {
            "email": "test@gmail.com",
            "name": "test",
            "phone_number": "3333333333",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
        }

        cls.invalid_data = {
            "name": "rudra",
            "email": "rudragmail.com",
            "password": "rudra1234",
            "phone_number": "1234567890",
        }

        cls.invalid_password_data = {
            "email": "test1@gmail.com",
            "name": "test1",
            "phone_number": "3333333333",
            "password": "Test12345",
        }

    def test_signupserializer_valid_data(self):
        """
        Test case for validating that the SignupSerializer accepts valid data.
        Ensures that the serializer returns no validation errors when correct input is provided.
        """
        serializer = user_serializers.SignupSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertEqual(serializer.errors, {})

    def test_serializer_invalid_data(self):
        """
        Test case for validating that the SignupSerializer rejects invalid data.
        Ensures that the serializer correctly flags invalid input as not valid.
        """
        serializer = user_serializers.SignupSerializer(data=self.invalid_data)

        self.assertFalse(serializer.is_valid())

    def test_signupserializer_duplicate_email(self):
        """
        Test case for validating duplicate email handling in SignupSerializer.
        Ensures that a user cannot register with an email that already exists in the database.
        """
        User.objects.create(**self.user_object_data)

        serializer = user_serializers.SignupSerializer(data=self.valid_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["email"][0],
            user_constants.ErrorMessage.EMAIL_ALREADY_EXIST,
        )

    def test_signupserializer_duplicate_phone_nummber(self):
        """
        Test case for validating duplicate phone number handling in SignupSerializer.
        Ensures that a user cannot register with a phone number that already exists in the database.
        """
        User.objects.create(**self.user_object_data)

        serializer = user_serializers.SignupSerializer(data=self.valid_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["phone_number"][0],
            user_constants.ErrorMessage.PHONE_NUMBER_ALREADY_EXIST,
        )

    def test_signup_serializer_password_validation(self):
        """
        Test case for validating password rules in SignupSerializer.
        Ensures that password validators are correctly enforced.
        """
        serializer = user_serializers.SignupSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["password"][0], user_constants.ErrorMessage.PASSWORD_ERROR
        )


class UserProfileSerializerTestCase(APITestCase):
    """Tests for the UserProfileSerializer"""

    @classmethod
    def setUpTestData(cls):
        cls.USER_DATA = {
            "email": "test@example.com",
            "name": "Test User",
            "phone_number": "1236567891",
            "password": "Testpassword@123",
        }
        cls.user = G(User, **cls.USER_DATA)

    def test_serializer_returns_expected_fields(self):
        """Serializer should include only expected fields"""
        serializer = user_serializers.UserSerializer(self.user)
        data = serializer.data
        expected_data = {
            "email": self.user.email,
            "name": self.user.name,
            "phone_number": self.user.phone_number,
        }
        self.assertEqual(data, expected_data)

    def test_email_field_is_read_only(self):
        """Email should not be editable"""
        serializer = user_serializers.UserSerializer(self.user)
        self.assertIn("email", serializer.fields)
        self.assertTrue(serializer.fields["email"].read_only)
