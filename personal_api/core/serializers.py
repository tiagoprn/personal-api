# Your Django Rest Framework serializers must go here.
from rest_framework.serializers import ModelSerializer

from core.models import Link


class LinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields = ('name', 'original_link', 'user')
        read_only_fields = (
            'slug',
            'sanitized_link',
            'shortened_hash',
            'created_at',
            'updated_at',
        )
