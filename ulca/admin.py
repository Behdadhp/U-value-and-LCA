from django.contrib import admin

from . import models


class BuildingAdmin(admin.ModelAdmin):
    """Class representing of building admin page"""

    list_display = (
        "name",
        "project",
        "wall",
        "roof",
        "floor",
        "wallUvalue",
        "roofUvalue",
        "floorUvalue",
    )


class MaterialAdmin(admin.ModelAdmin):
    """Class representing of material admin page"""

    list_display = (
        "name",
        "rho",
        "lamb",
        "GWP",
        "ODP",
        "POCP",
        "AP",
        "EP",
        "url_to_oekobaudat",
    )


admin.site.register(models.Building, BuildingAdmin)
admin.site.register(models.Material, MaterialAdmin)
