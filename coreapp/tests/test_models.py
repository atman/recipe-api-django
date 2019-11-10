from django.test import TestCase
from django.contrib.auth import get_user_model
from coreapp import models


def sample_user(email='test@druk.com', password='testpass'):
    """Creates a sample User"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """"Test creating a new user with an email is successful"""
        email = "test@druk.com"
        password = "Test@123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if new user email is normalized"""
        email = "Badman@GMAIL.com"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test Creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'testsuperuser@druk.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # ---------------------- FOR RECIPE APP -------------------

    def test_tag_str(self):
        """Test the tag if it it returns a string or not"""
        tag = models.Tag.objects.create(
            custom_user=sample_user(),
            name='vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_self(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            custom_user=sample_user(),
            name="cucumber"
        )
        self.assertEqual(str(ingredient), ingredient.name)