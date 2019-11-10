from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from coreapp.models import Ingredient
from recipeapp.serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipeapp:ingredient-list")


class PublicIngredientsApiTest(TestCase):
    """Test that unautorized requests are rejected"""

    def setUp(self):
        self.client = APIClient()

    def test_ingredients_public_acess_denied(self):
        """Tests that login is required for listing ingredients"""

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase):
    """Test private Ingredients API for logged in user"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@testapp.com",
            "pass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_all_ingredients(self):
        """Test if ingredients are listed"""

        Ingredient.objects.create(custom_user=self.user, name="cucumber")
        Ingredient.objects.create(custom_user=self.user, name="tomatoes")

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for logged in user are retrieved"""

        other_user = get_user_model().objects.create_user(
            "other_user@testapp.com",
            "pass1234"
        )
        Ingredient.objects.create(custom_user=other_user, name="lemons")
        ingredient = Ingredient.objects.create(custom_user=self.user, name="watermelon")

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredients(self):
        """Test that ingredients are created"""

        payload = {'name': 'onion'}
        response = self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            custom_user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_ingredient(self):
        """Test the creation of an invalid ingredient"""

        payload = {
            'name': ''
        }
        response = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)