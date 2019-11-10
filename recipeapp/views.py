from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from coreapp.models import Tag
from coreapp.models import Ingredient
from recipeapp import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    """Manage Tags in the database"""

    # setting the REST framework authentication on a per-class basis
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(custom_user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new tags for authenticated users"""
        serializer.save(custom_user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    """Manage Ingredients in the database"""

    # setting the REST framework authentication on a per-class basis
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(custom_user=self.request.user).order_by('-name')

    # Called before save; Goes up to the parent context and assigns the current user as the object creator
    def perform_create(self, serializer):
        serializer.save(custom_user=self.request.user)
