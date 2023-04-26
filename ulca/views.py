from django.urls import reverse_lazy
from django_filters.views import FilterView
from django_tables2 import SingleTableView, MultiTableMixin
from . import models, tables
from django.views import generic

from .filters import BuildingFilter
from .forms import CreateBuilding


class BuildingList(FilterView, SingleTableView):
    """View for listing all buildings"""

    table_class = tables.BuildingTable
    table_pagination = {"per_page": 5}
    model = models.Building
    template_name = "building_list.html"

    filterset_class = BuildingFilter


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


class BuildingCreate(generic.CreateView):
    """View for creating new project"""

    template_name = "building_details.html"
    model = models.Building
    form_class = CreateBuilding
    success_url = reverse_lazy("building:buildings")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class BuildingDelete(generic.DeleteView):
    """View for deleting existing project"""

    template_name = "building_confirm_delete.html"
    model = models.Building
    success_url = reverse_lazy("building:buildings")
