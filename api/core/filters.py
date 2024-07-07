from django_filters import rest_framework as filters

from .models import Database


class DatabaseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Database
        fields = ["name", "workspace"]
