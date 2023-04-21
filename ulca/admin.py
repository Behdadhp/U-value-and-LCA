from django.contrib import admin

from . import models


class BuildingAdmin(admin.ModelAdmin):
    """Class representing of Building admin page"""

    list_display = ("name", "project")


admin.site.register(models.Building, BuildingAdmin)
