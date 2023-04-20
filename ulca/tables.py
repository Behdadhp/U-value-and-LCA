import django_tables2 as tables

from . import models


class BuildingTable(tables.Table):
    name = tables.Column
    project = tables.Column

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Building
