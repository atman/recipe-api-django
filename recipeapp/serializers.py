from rest_framework import serializers

from coreapp.models import Tag
from coreapp.models import Ingredient
from coreapp.models import Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    """Model Serializer for Recipes"""
    ingredient = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'custom_user', 'time_taken', 'price', 'link', 'ingredient', 'tag')
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    ingredient = IngredientSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)
