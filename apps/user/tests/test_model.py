from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    """
    Test case class for testing the models
    """

    @classmethod
    def setUpTestData(cls):
        """
        For setting up the data
        """
        cls.data = {
            "email": "kushal@gmail.com",
            "name": "kushal raj pareek",
            "phone_number": "1234567890",
            "password": "Krp@123456",
        }

        cls.admin_data = {
            "email": "admin@gmail.com",
            "name": "Admin",
            "phone_number": "9876543210",
            "password": "Admin@123",
        }

    def test_create_user(self):
        """
        Test case for creating a regular user.
        Ensures that the user is created successfully with the correct fields,
        and that the password is properly hashed.
        Verifies that 'is_staff' and 'is_superuser' flags are False for normal users.
        """
        user = User.objects.create(**self.data)

        self.assertEqual(user.email, self.data["email"])
        self.assertEqual(user.name, self.data["name"])
        self.assertEqual(user.phone_number, self.data["phone_number"])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.password, self.data["password"])

    def test_create_superuser(self):
        """
        Test case for creating a superuser.
        Ensures that the superuser is created successfully with correct fields,
        and that the password is properly hashed.
        """
        user = User.objects.create_superuser(**self.admin_data)

        self.assertEqual(user.email, self.admin_data["email"])
        self.assertEqual(user.name, self.admin_data["name"])
        self.assertEqual(user.phone_number, self.admin_data["phone_number"])
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(self.admin_data["password"]))
