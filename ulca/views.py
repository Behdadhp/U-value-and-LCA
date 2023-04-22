from django_tables2 import SingleTableView
from . import models, tables
from django.views import generic


class BuildingList(SingleTableView):
    """View for listing all buildings"""

    table_class = tables.BuildingTable
    table_pagination = {"per_page": 30}
    queryset = models.Building.objects.all()
    template_name = "building_list.html"


class BuildingDetails(generic.DetailView):
    """View for showing the result of calculations"""

    template_name = "building_details.html"
    queryset = models.Building.objects.all()
