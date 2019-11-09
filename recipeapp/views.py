from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from coreapp.models import Tag
from recipeapp import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Tags in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(custom_user=self.request.user).order_by('-name')