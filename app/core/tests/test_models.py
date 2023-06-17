"""Test for models"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test for models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = "test@example.com"
        password = "1234"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        test_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.Com", "Test2@example.com"],
        ]

        for email, expected in test_emails:
            user = get_user_model().objects.create_user(email=email, password="1234")
            self.assertEqual(user.email, expected)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="1234")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser("test@exampl.com", "1234")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def create_recipe(self):
        user = get_user_model().objects.create_user("test@example.com", "1234")
        recipe = models.Recipe.objects.create(
            user=user,
            title="Steak and mushroom sauce",
            time_minutes=5,
            price=Decimal("5.00"),
            description="test description",
        )
        self.assertEqual(str(recipe), recipe.title)
