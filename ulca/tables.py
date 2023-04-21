import django_tables2 as tables

from . import models


class BuildingTable(tables.Table):
    """Table for building model"""

    project = tables.JSONColumn()

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Building
