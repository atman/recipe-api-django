from rest_framework import serializers

from coreapp.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for listing Tag Objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'custom_user')
        read_only_fields = ('id',)
