from django_tables2 import SingleTableView, MultiTableMixin
from . import models, tables
from django.views import generic


class BuildingList(SingleTableView):
    """View for listing all buildings"""

    table_class = tables.BuildingTable
    table_pagination = {"per_page": 30}
    queryset = models.Building.objects.all()
    template_name = "building_list.html"


class BuildingDetails(generic.DetailView, MultiTableMixin):
    """View for showing the result of calculations"""

    template_name = "building_details.html"
    queryset = models.Building.objects.all()
    table_class = tables.BuildingDetail

    def get_building_id(self):
        return self.kwargs["pk"]

    def create_data_query(self):
        return models.Building.objects.filter(id=self.get_building_id())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"] = tables.BuildingDetail(self.create_data_query())
        return context
