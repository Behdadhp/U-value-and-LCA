from django_tables2 import SingleTableView
from . import models, tables


class BuildingList(SingleTableView):
    """View for listing all buildings"""

    table_class = tables.BuildingTable
    table_pagination = {"per_page": 30}
    queryset = models.Building.objects.all()
    template_name = "building_list.html"
