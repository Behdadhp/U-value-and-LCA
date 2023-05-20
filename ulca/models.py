from django.db import models

from .calculation.data import building_default_value, material_default_value

from .calculation.uvalue import UValue

from .calculation import data


class Building(models.Model):
    """ORM representation of the Projects"""

    name = models.CharField(max_length=64, blank=False, null=False)
    project = models.JSONField(default=building_default_value, blank=False, null=False)
    wall = models.CharField(max_length=128, blank=True)
    roof = models.CharField(max_length=128, blank=True)
    floor = models.CharField(max_length=128, blank=True)
    wallUvalue = models.CharField(max_length=32, blank=True)
    roofUvalue = models.CharField(max_length=32, blank=True)
    floorUvalue = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name

    def get_wall(self):
        """Get the wall from Project"""
        return self.project["wall"]

    def get_roof(self):
        """Get the roof from Project"""
        return self.project["roofbase"]

    def get_floor(self):
        """Get the floor from Project"""
        return self.project["floor"]

    def get_uvalue(self, component):
        """Get the value of U"""
        instance = UValue(self.project, Material)
        return instance.calc_u(component)

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

        super().save(force_insert, force_update, using, update_fields)


class Material(models.Model):
    """ORM represntation of the materials"""

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
