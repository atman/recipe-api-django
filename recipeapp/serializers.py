from rest_framework import serializers

from coreapp.models import Tag
from coreapp.models import Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag Objects"""

# Only include fields that are relevant for creating and updating

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredients Serializer"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)