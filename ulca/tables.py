import django_tables2 as tables

from . import models


class BuildingTable(tables.Table):
    """Table for building model"""

    name = tables.Column()
    project = tables.Column()
    # wall = tables.Column()
    # roof = tables.Column()
    # floor = tables.Column()

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Building
