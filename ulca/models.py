from django.db import models

from .calculation.data import building_default_value, material_default_value

from .calculation import calc


class Building(models.Model):
    """ORM representation of the Projects"""

    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    project = models.JSONField(default=building_default_value, blank=False, null=False)
    wall = models.TextField(blank=True)
    roof = models.TextField(blank=True)
    floor = models.TextField(blank=True)
    wallUvalue = models.CharField(max_length=32, blank=True)
    roofUvalue = models.CharField(max_length=32, blank=True)
    floorUvalue = models.CharField(max_length=32, blank=True)
    lca = models.CharField(max_length=256, blank=True, null=True, default="")

    def __str__(self):
        return self.name

    def get_wall(self):
        """Gets the wall from Project"""
        return self.project["wall"]

    def get_roof(self):
        """Gets the roof from Project"""
        return self.project["roofbase"]

    def get_floor(self):
        """Gets the floor from Project"""
        return self.project["floor"]

    def get_uvalue(self, component):
        """Gets the value of U"""
        instance = calc.CalcUValue(self.project, Material)
        return instance.calc_u(component)

    def get_lca(self):
        """Gets the environmental impact"""
        project = {}
        for layer in ["wall", "floor", "roofbase"]:
            instance = calc.CalcLCA(self.project, Material)
            dic = instance.calc_lca(layer)
            project.update(dic[layer])
        return project

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """Save the elements to model"""

        # get the wall
        self.wall = self.get_wall()

        # get the roof
        self.roof = self.get_roof()

        # get the floor
        self.floor = self.get_floor()

        # get the u-value for wall
        self.wallUvalue = self.get_uvalue("wall")

        # get the u-value for roof
        self.roofUvalue = self.get_uvalue("roofbase")

        # get the u-value for floor
        self.floorUvalue = self.get_uvalue("floor")

        # get the environmental impact for all layers
        self.lca = self.get_lca()

        super().save(force_insert, force_update, using, update_fields)


class Material(models.Model):
    """ORM representation of the materials"""

    MASS = "mass"
    VOLUME = "volume"
    AREA = "area"

    type_choices = ((MASS, "Mass"), (VOLUME, "Volume"), (AREA, "Area"))

    name = models.CharField(max_length=64, blank=False, null=False)
    rho = models.FloatField(max_length=8)
    lamb = models.FloatField(
        max_length=8, blank=False, null=False, verbose_name="lambda"
    )
    GWP = models.JSONField(
        default=material_default_value,
        blank=True,
        null=True,
        help_text="Global warming potential",
    )
    ODP = models.JSONField(
        default=material_default_value,
        blank=True,
        null=True,
        help_text="Ozone layer depletion potential",
    )
    POCP = models.JSONField(
        default=material_default_value,
        blank=True,
        null=True,
        help_text="Ozone creation potential",
    )
    AP = models.JSONField(
        default=material_default_value,
        blank=True,
        null=True,
        help_text="Acidification potential",
    )
    EP = models.JSONField(
        default=material_default_value,
        blank=True,
        null=True,
        help_text="Fertilization potential",
    )
    type = models.CharField(max_length=32, choices=type_choices, default=VOLUME)
    url_to_oekobaudat = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
