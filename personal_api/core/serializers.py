# Your Django Rest Framework serializers must go here.
from rest_framework.serializers import ModelSerializer

from core.models import Link


class LinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields = (
            'id',
            'name',
            'original_link',
            'user',
            'slug',
            'sanitized_link',
            'shortened_hash',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'slug',
            'sanitized_link',
            'shortened_hash',
            'created_at',
            'updated_at',
        )
