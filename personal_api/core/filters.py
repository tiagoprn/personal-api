from django_filters.rest_framework import CharFilter, DateTimeFilter, FilterSet


class LinkFilter(FilterSet):
    class Meta:
        fields = [
            'name',
            'original_link',
            'username',
            'slug',
            'sanitized_link',
            'shortened_hash',
            'min_created_at',
            'max_created_at',
            'min_updated_at',
            'max_updated_at',
        ]

    name = CharFilter(lookup_expr='icontains')
    original_link = CharFilter(lookup_expr='icontains')
    username = CharFilter(field_name='user.username', lookup_expr='icontains')
    slug = CharFilter(lookup_expr='icontains')
    sanitized_link = CharFilter(lookup_expr='icontains')
    shortened_hash = CharFilter(lookup_expr='icontains')
    min_created_at = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    max_created_at = DateTimeFilter(field_name='created_at', lookup_expr='lte')
    min_updated_at = DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    max_updated_at = DateTimeFilter(field_name='updated_at', lookup_expr='lte')
