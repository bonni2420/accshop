import django_filters
from .models import GameAccount


class GameAccountFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.NumberFilter(field_name="category_id")
    is_sold = django_filters.BooleanFilter()

    class Meta:
        model = GameAccount
        fields = ["category", "is_sold"]
