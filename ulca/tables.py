import django_tables2 as tables
from django.utils.html import format_html, format_html_join, escape
from django_tables2 import A

from . import models


class BuildingTable(tables.Table):
    """Table for building model"""

    project = tables.JSONColumn()
    generate = tables.LinkColumn(
        "building:details", args=[A("pk")], verbose_name="", text="Generate"
    )
    update = tables.LinkColumn(
        "building:updateBuilding", args=[A("pk")], verbose_name="", text="Update"
    )
    Delete = tables.LinkColumn(
        "building:deleteBuilding",
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


class MaterialTable(tables.Table):
    """Table for material model"""

    update = tables.LinkColumn(
        "building:updateMaterial", args=[A("pk")], verbose_name="", text="Update"
    )
    Delete = tables.LinkColumn(
        "building:deleteMaterial",
        args=[A("pk")],
        text="Delete",
        verbose_name="",
        attrs={"a": {"style": "color: red;"}},
    )
    items = tables.Column(empty_values=(), verbose_name="")

    GWD = tables.Column()
    ODP = tables.Column()
    POCP = tables.Column()
    AP = tables.Column()
    EP = tables.Column()
    url_to_oekobaudat = tables.Column(verbose_name="Link")

    def render_items(self):
        items = [
            "Herstellungsphase",
            "Erneuerung",
            "Energiebedarf",
            "Lebensendphase",
        ]
        return format_html_join("\n", "<p>{}: </p>", ((key,) for key in items))

    def render_url_to_oekobaudat(self, value):
        return format_html(
            "<a href={} target=_blank>{}</a>", value, "Link to Ökobaudat"
        )

    @staticmethod
    def render_GWD(record):
        return format_html_join(
            "\n", "<p>{} </p>", ((item,) for item in record.GWD.values())
        )

    @staticmethod
    def render_ODP(record):
        return format_html_join(
            "\n", "<p>{} </p>", ((item,) for item in record.ODP.values())
        )

    @staticmethod
    def render_POCP(record):
        return format_html_join(
            "\n", "<p>{} </p>", ((item,) for item in record.POCP.values())
        )

    @staticmethod
    def render_AP(record):
        return format_html_join(
            "\n", "<p>{} </p>", ((item,) for item in record.AP.values())
        )

    def render_EP(self, record):
        return format_html_join(
            "\n", "<p>{} </p>", ((item,) for item in record.EP.values())
        )

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Material
        exclude = ("id",)
        sequence = ("name", "rho", "lamb", "items")
