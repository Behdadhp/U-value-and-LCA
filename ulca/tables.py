import django_tables2 as tables
from django_tables2 import A

from . import models


class BuildingTable(tables.Table):
    """Table for building model"""

    project = tables.JSONColumn()
    generate = tables.LinkColumn("building:details", args=[A("pk")], text="Generate")

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Building
