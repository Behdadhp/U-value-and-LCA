import django_tables2 as tables
from django_tables2 import A

from . import models


class BuildingTable(tables.Table):
    """Table for building model"""

    project = tables.JSONColumn()
    generate = tables.LinkColumn(
        "building:details", args=[A("pk")], verbose_name="", text="Generate"
    )
    update = tables.LinkColumn(
        "building:update", args=[A("pk")], verbose_name="", text="Update"
    )
    Delete = tables.LinkColumn(
        "building:delete",
        args=[A("pk")],
        text="Delete",
        verbose_name="",
        attrs={"a": {"style": "color: red;"}},
    )

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Building
        exclude = ("wallUvalue", "roofUvalue", "floorUvalue")


class BuildingDetail(tables.Table):
    """Table for building details"""

    wallUvalue = tables.Column(verbose_name="Wall U-value")
    roofUvalue = tables.Column(verbose_name="Roof U-value")
    floorUvalue = tables.Column(verbose_name="Floor U-value")

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Building
        fields = ("wallUvalue", "roofUvalue", "floorUvalue")
