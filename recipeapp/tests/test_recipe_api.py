from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from coreapp.models import Recipe
from coreapp.models import Tag
from coreapp.models import Ingredient

from recipeapp.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse("recipeapp:recipe-list")


# /api/recipe/recipes
# api/recipe/recipes/1

# ------HELPER FUNCTIONS----------
def get_detail_URL(recipe_id):
    """Return the recipe detail URL"""
    return reverse('recipeapp:recipe-detail', args=[recipe_id])


def create_sample_tag(user, name="spicy"):
    """Sample tag for testing"""
    return Tag.objects.create(custom_user=user, name=name)


def create_sample_ingredient(user, name="cinnamon"):
    """Sample tag for testing"""
    return Ingredient.objects.create(custom_user=user, name=name)


def create_sample_recipe(user, **params):
    defaults = {
        'title': 'Steak and eggs',
        'time_taken': 20,
        'price': 10.00
    }
    defaults.update(params)

    return Recipe.objects.create(custom_user=user, **defaults)


# ---------- TESTS --------------
class PublicRecipeApiTest(TestCase):
    """Tests the publicly available API"""

    def setUp(self):
        self.client = APIClient(self)

    def test_login_required(self):
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Tests the private API responses for list, create, update & delete"""

    def setUp(self):
        self.sample_user = get_user_model().objects.create_user(
            "test@test.com",
            "sample@123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.sample_user)

    def test_retrieve_recipes(self):
        create_sample_recipe(user=self.sample_user)
        create_sample_recipe(user=self.sample_user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_recipe_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            "test@123.com",
            "password@123"
        )

        create_sample_recipe(user=user2)
        create_sample_recipe(user=self.sample_user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(custom_user=self.sample_user)

        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_retrive_recipe_detail(self):
        """Test for viewing a recipe detail"""
        recipe = create_sample_recipe(user=self.sample_user)
        recipe.tag.add(create_sample_tag(user=self.sample_user))
        recipe.ingredient.add(create_sample_ingredient(user=self.sample_user))

        detail_URL = get_detail_URL(recipe.id)
        res = self.client.get(detail_URL)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_new_recipe(self):
        ingredient_steak = Ingredient.objects.create(
            name="steak",
            custom_user=self.sample_user
        )

        tag_non_veg = Tag.objects.create(
            name="non-veg",
            custom_user=self.sample_user
        )

        # recipe = get_sample_recipe(self.sample_user)
        # db_recipe =

        # self.assertEqual(recipe.title, )
