from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from coreapp.models import Tag
from recipeapp.serializers import TagSerializer


# - [modelname]-[list] syntax of Django Rest Framework
TAGS_URL = reverse("recipeapp:tag-list")


class PublicTagsApiTests(TestCase):
    """Tests the publicly available Tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Tests that login is required for listing tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Tests the authorized tags API"""

    # Note the syntax setUp(), it is called automatically
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@recipeapp.com",
            "password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving all tags"""

        Tag.objects.create(custom_user=self.user, name="meat")
        Tag.objects.create(custom_user=self.user, name="vegan")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Tests that tags are limited only to logged in User"""

        other_user = get_user_model().objects.create_user(
            "otheruser@recipeapp.com",
            "password123"
        )

        Tag.objects.create(custom_user=other_user, name="binge")
        tag = Tag.objects.create(custom_user=self.user, name="comfort food")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'], tag.name)


