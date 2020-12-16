# Your Django Rest Framework serializers must go here.
from rest_framework.serializers import ModelSerializer

from core.models import Url


class UrlSerializer(ModelSerializer):
    class Meta:
        model = Url
        fields = ('name', 'original_url', 'user')
        read_only_fields = (
            'slug',
            'sanitized_url',
            'shortened_hash',
            'created_at',
            'updated_at',
        )
