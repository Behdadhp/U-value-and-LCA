import ast

import django_tables2 as tables
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from . import models


class BuildingTable(tables.Table):
    """Table for building model"""

    actions = tables.TemplateColumn(
        """
        <a class="btn btn-dark" href="{% url 'building:details' record.pk %}">Generieren</a>
        <br>
        <br>
        <a class="btn btn-primary" href="{% url 'building:updateBuilding' record.pk %}">Aktualisieren</a>
        <br>
        <br>
        <a class="btn btn-danger" href="{% url 'building:deleteBuilding' record.pk %}" ;">Löschen</a>
        """,
        verbose_name="",
        attrs={"td": {"class": "text-left"}},
    )

    wall = tables.Column(
        verbose_name="Außenwandkomponenten", attrs={"td": {"class": "text-left"}}
    )
    roof = tables.Column(
        verbose_name="Dachkomponenten", attrs={"td": {"class": "text-left"}}
    )
    floor = tables.Column(
        verbose_name="Bodenplattekomponenten", attrs={"td": {"class": "text-left"}}
    )

    def render_wall(self, value):
        return self.render_components(value)

    def render_roof(self, value):
        return self.render_components(value)

    def render_floor(self, value):
        return self.render_components(value)

    @staticmethod
    def render_components(value):
        return format_html_join(
            "",
            "<p> {} {}mm</p>",
            (
                (k, v["thickness"])
                for k, v in ast.literal_eval(value).items()
                if isinstance(v, dict)
            ),
        )

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Building
        exclude = (
            "id",
            "project",
            "wallUvalue",
            "roofUvalue",
            "floorUvalue",
            "lca",
            "project_json",
            "project_document",
        )
        attrs = {"class": "table table-striped"}


class BuildingDetail(tables.Table):
    """Table for building details"""

    wallUvalue = tables.Column(verbose_name="Außenwand U-Wert")
    roofUvalue = tables.Column(verbose_name="Dach U-Wert")
    floorUvalue = tables.Column(verbose_name="Bodenplatte U-Wert")

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Building
        fields = ("wallUvalue", "roofUvalue", "floorUvalue")
        attrs = {
            "class": "table table-striped",
            "td": {"class": "text-left"},
        }


class MaterialTable(tables.Table):
    """Table for material model"""

    actions = tables.TemplateColumn(
        """
        <a class="btn btn-primary" href="{% url 'building:updateMaterial' record.pk %}">Aktualisieren</a>
        <br>
        <br>
        <a  class="btn btn-danger" href="{% url 'building:deleteMaterial' record.pk %}";">Löschen</a>
        """,
        verbose_name="",
    )
    GWP = tables.Column(empty_values=(), verbose_name=mark_safe("GWP<br>(kg CO2-Äqv)"))
    ODP = tables.Column(empty_values=(), verbose_name=mark_safe("ODP<br>(kg R11-Äqv)"))
    POCP = tables.Column(
        empty_values=(), verbose_name=mark_safe("POCP<br>(kg Ethen-Äqv)")
    )
    AP = tables.Column(empty_values=(), verbose_name=mark_safe("AP<br>(kg SO2-Äqv)"))
    EP = tables.Column(
        empty_values=(), verbose_name=mark_safe("EP<br>(kg Phosphat-Äqv)")
    )
    items = tables.Column(
        empty_values=(), verbose_name="", attrs={"td": {"class": "text-left"}}
    )

    @staticmethod
    def render_items():
        items = [
            "Herstellungsphase (A1-A3)",
            "Erneuerung (B2 & B4)",
            "Energiebedarf (B6)",
            "Lebensendphase (C3 & C4)",
        ]
        return format_html_join("\n", "<p>{}: </p>", ((key,) for key in items))

    @staticmethod
    def render_GWP(record):
        return format_html_join(
            "\n", "<p>{} </p>", ((item,) for item in record.GWP.values())
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

    @staticmethod
    def render_EP(record):
        return format_html_join(
            "\n", "<p>{} </p>", ((item,) for item in record.EP.values())
        )

    @staticmethod
    def render_name(record):
        return format_html(
            "<a href={} target=_blank>{}</a>", record.url_to_oekobaudat, record.name
        )

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = models.Material
        exclude = ("id", "type", "url_to_oekobaudat")
        sequence = ("name", "rho", "lamb", "items")

        attrs = {
            "class": "table table-striped",
            "td": {"class": "text-left"},
        }


class ComponentTable(tables.Table):
    """Tables for components"""

    layer = tables.Column(
        empty_values=(), verbose_name="Material (von innen nach außen)"
    )
    thickness = tables.Column(empty_values=(), verbose_name="Dicke  mm")
    area = tables.Column(empty_values=(), verbose_name="Fläche m2")
    volume = tables.Column(empty_values=(), verbose_name="Volumen m3")
    mass = tables.Column(empty_values=(), verbose_name="Masse kg")

    @staticmethod
    def render_layer(record):
        """ "Gets the layers"""

        return format_html_join(
            "",
            "<b>{} </b>",
            ((key,) for key in record),
        )

    def render_thickness(self, record):
        """Gets the thickness of each layer"""

        return self.create_attr("thickness", record)

    def render_area(self, record):
        """Gets the area of each layer"""

        return self.create_attr("area", record)

    def render_volume(self, record):
        """Gets the volume of each layer"""

        return self.create_attr("volume", record)

    def render_mass(self, record):
        """Gets the mass of each layer"""

        return self.create_attr("mass", record)

    @staticmethod
    def create_attr(attr, record):
        """Creates the way of rendering for each layer"""
        return format_html_join(
            "",
            "<p>{} </p>",
            ((record[key][attr],) for key in record),
        )

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        sequence = ("layer", "thickness", "area", "volume", "mass")

        attrs = {
            "class": "table table-striped",
            "td": {"class": "text-left"},
        }


class LCATable(tables.Table):
    """Table for LCA"""

    phase = tables.Column(empty_values=(), attrs={"th": {"style": "width: 30%"}})
    layer = tables.Column(
        empty_values=(), verbose_name="Material (von innen nach außen)"
    )
    gwp = tables.Column(empty_values=(), verbose_name=mark_safe("GWP<br>(kgCO2-Äqv)"))
    odp = tables.Column(empty_values=(), verbose_name=mark_safe("ODP<br>(kgR11-Äqv)"))
    pocp = tables.Column(
        empty_values=(), verbose_name=mark_safe("POCP<br>(kgEthen-Äqv)")
    )
    ap = tables.Column(empty_values=(), verbose_name=mark_safe("AP<br>(kgSO2-Äqv)"))
    ep = tables.Column(
        empty_values=(), verbose_name=mark_safe("EP<br>(kg Phosphat-Äqv)")
    )

    @staticmethod
    def render_layer(record):
        """ "Gets the layers"""

        return format_html_join(
            "",
            "<b>{} </b>",
            ((key,) for key in record),
        )

    @staticmethod
    def render_phase():
        """Crates phases for each layer"""

        items = [
            "Herstellungsphase (A1-A3)",
            "Erneuerung (B2 & B4)",
            "Energiebedarf (B6)",
            "Lebensendphase (C3 & C4)",
        ]
        return format_html_join("\n", "<p>{}: </p>", ((key,) for key in items))

    def render_gwp(self, record):
        """Gets the gwp for each layer"""

        return self.get_phase_value("gwp", record)

    def render_odp(self, record):
        """Gets the odp for each layer"""

        return self.get_phase_value("odp", record)

    def render_pocp(self, record):
        """Gets the pocp for each layer"""

        return self.get_phase_value("pocp", record)

    def render_ap(self, record):
        """Gets the ap for each layer"""

        return self.get_phase_value("ap", record)

    def render_ep(self, record):
        """Gets the gwp for each layer"""

        return self.get_phase_value("ep", record)

    @staticmethod
    def get_phase_value(phase, record):
        layer = list(record.keys())
        phase_value = [key for key in record[layer[0]][phase].values()]

        return format_html_join(
            "",
            "<p>{} </p>",
            ((item,) for item in phase_value),
        )

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        sequence = ("layer", "phase")

        attrs = {
            "class": "table table-striped",
            "td": {"class": "text-left"},
        }


class LCARatingSystemTable(tables.Table):
    """Table for LCA"""

    phase = tables.Column(empty_values=())
    layer = tables.Column(
        empty_values=(), verbose_name="Material (von innen nach außen)"
    )
    gwp = tables.Column(empty_values=(), verbose_name="GWP")
    odp = tables.Column(empty_values=(), verbose_name="ODP")
    pocp = tables.Column(empty_values=(), verbose_name="POCP")
    ap = tables.Column(empty_values=(), verbose_name="AP")
    ep = tables.Column(empty_values=(), verbose_name="EP")

    @staticmethod
    def render_layer(record):
        """ "Gets the layers"""

        return format_html_join(
            "",
            "<b>{} </b>",
            ((key,) for key in record),
        )

    @staticmethod
    def render_phase():
        """Crates phases for each layer"""

        items = [
            "Herstellungsphase (A1-A3)",
            "Erneuerung (B2 & B4)",
            "Energiebedarf (B6)",
            "Lebensendphase (C3 & C4)",
        ]
        return format_html_join("\n", "<p>{}: </p>", ((key,) for key in items))

    def render_gwp(self, record):
        """Gets the gwp for each layer"""

        return self.get_phase_value("gwp", record)

    def render_odp(self, record):
        """Gets the odp for each layer"""

        return self.get_phase_value("odp", record)

    def render_pocp(self, record):
        """Gets the pocp for each layer"""

        return self.get_phase_value("pocp", record)

    def render_ap(self, record):
        """Gets the ap for each layer"""

        return self.get_phase_value("ap", record)

    def render_ep(self, record):
        """Gets the gwp for each layer"""

        return self.get_phase_value("ep", record)

    @staticmethod
    def get_phase_value(phase, record):
        layer = list(record.keys())
        phase_value = [
            key for key in record[layer[0]]["lca_rating_system"][phase].values()
        ]
        total = round(sum(phase_value), 15)

        if total == 0:
            total = 1
        return format_html_join(
            "",
            "<p>{} ({}%)</p>",
            ((item, round(item / total * 100, 2)) for item in phase_value),
        )

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        sequence = ("layer", "phase")

        attrs = {
            "class": "table table-striped",
            "td": {"class": "text-left"},
        }
