from django_filters import FilterSet

from . import models


class BuildingFilter(FilterSet):
    """Filter the projects"""

    class Meta:
        model = models.Building
        fields = {"name": ["exact", "contains"]}
