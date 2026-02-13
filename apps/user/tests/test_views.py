from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.user import constants as user_constants

User = get_user_model()


class SignUpViewTestCase(APITestCase):
    """
    Test case class for testing the Signup and Login API views
    """

    @classmethod
    def setUpTestData(cls):
        """
        For setting up the data
        """
        cls.signup_data = {
            "email": "test@gmail.com",
            "name": "test",
            "phone_number": "8877665544",
            "password": "Test@123",
            "confirm_password": "Test@123",
        }

        cls.user_object_data = {
            "email": "test@gmail.com",
            "name": "test",
            "phone_number": "3333333333",
            "password": "Test@1234",
        }

        cls.signup_invalid_data = {
            "name": "",
            "email": "rudra-gmail.com",
            "password": "rudra123",
            "phone_number": "11111111",
        }

        cls.login_data = {"email": "test@gmail.com", "password": "Test@123"}

        cls.login_invalid_data = {"email": "test2@gmail.com", "password": "Test@123"}

    def test_signup_view_success(self):
        """
        Test case for successful user Signup
        """
        url = reverse("signup")
        response = self.client.post(url, self.signup_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.signup_data["name"])
        self.assertEqual(response.data["email"], self.signup_data["email"])
        self.assertEqual(
            response.data["phone_number"], self.signup_data["phone_number"]
        )

    def test_signup_view_inavlid_data(self):
        """
        Test case for signup with invalid data
        """
        url = reverse("signup")
        response = self.client.post(url, self.signup_invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_view_duplicate_data(self):
        """
        Test case for signup with duplicate data
        """
        User.objects.create(**self.user_object_data)
        url = reverse("signup")
        response = self.client.post(url, self.signup_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_success(self):
        """
        Test case for successful user login
        """
        url = reverse("login")
        url_signup = reverse("signup")
        self.client.post(url_signup, self.signup_data, format="json")
        response = self.client.post(url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cookies = response.client.cookies
        self.assertIn("refresh-token", cookies)
        self.assertTrue(cookies["refresh-token"].value)

        data = response.data
        self.assertIn("access", data)
        self.assertTrue(len(response.data["access"]) > 0)

    def test_login_view_invalid_credentials(self):
        """
        Test case for login with invalid credentials
        """
        url = reverse("login")
        url_signup = reverse("signup")
        self.client.post(url_signup, self.signup_data, format="json")
        response = self.client.post(url, self.login_invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], user_constants.ErrorMessage.LOGIN_INVALID
        )

    def test_token_refresh_view(self):
        """
        Test case for refreshing access token using a valid refresh token
        """
        url = reverse("login")
        url_signup = reverse("signup")
        self.client.post(url_signup, self.signup_data, format="json")
        response = self.client.post(url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token_url = reverse("token_refresh")
        token_url_response = self.client.post(token_url)
        self.assertEqual(token_url_response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(token_url_response.data["access"]) > 0)

    def test_refresh_token_deleted(self):
        """
        Test case for access token refresh after the refresh token is deleted from cookies
        """
        url = reverse("login")
        url_signup = reverse("signup")
        self.client.post(url_signup, self.signup_data, format="json")
        self.client.post(url, self.login_data, format="json")
        self.client.cookies.pop("refresh-token")

        url = reverse("token_refresh")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],
            user_constants.ErrorMessage.REFRESH_TOKEN_NOT_FOUND,
        )


class UserProfileViewTest(APITestCase):
    """Test for the User Profile API for:
    - Retrieving user authenticated user profile details (GET)
    - Updating user profile information (PATCH)"""

    def setUp(self):
        self.USER_PROFILE_DATA = {
            "email": "test@example.com",
            "password": "password123",
            "name": "test",
            "phone_number": "1234567890",
        }
        self.user = User.objects.create(**self.USER_PROFILE_DATA)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("user_profile")

    def test_get_user_profile(self):
        """Ensure GET/users/profile/
        returns the correct user information."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.USER_PROFILE_DATA["email"])

    def test_update_user_profile(self):
        """Ensure PATCH/user/profile/
        successfully updates editable fields (name,phone number)"""
        data = {
            "email": "test2@email.com",
            "name": "test user",
            "phone_number": "1234554321",
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["phone_number"], data["phone_number"])
        # email is not changed
        self.assertEqual(response.data["email"], self.USER_PROFILE_DATA["email"])
