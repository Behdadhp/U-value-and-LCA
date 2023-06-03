import json

from django.urls import reverse_lazy
from django_filters.views import FilterView
from django_tables2 import SingleTableView, MultiTableMixin
from . import models, tables
from django.views import generic

from . import filters
from . import forms
from .calculation import calc
from .utils import sort_project


class BuildingList(FilterView, SingleTableView):
    """View for listing all buildings"""

    table_class = tables.BuildingTable
    table_pagination = {"per_page": 5}
    model = models.Building
    template_name = "building_list.html"

    filterset_class = filters.BuildingFilter


class BuildingDetails(generic.DetailView, MultiTableMixin):
    """View for showing the result of calculations"""

    template_name = "building_details.html"
    queryset = models.Building.objects.all()
    table_class = tables.BuildingDetail

    def get_building_id(self):
        """Gets the pk of the current page"""

        return self.kwargs["pk"]

    def create_data_query(self):
        """Creates query to building"""

        return models.Building.objects.filter(id=self.get_building_id())

    def create_building_table(self, component):
        """Provides data for creating tables"""

        building = self.get_object()

        return [
            {key: building.project[component][key]}
            for key in building.project[component].keys()
            if isinstance(building.project[component][key], dict)
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"] = tables.BuildingDetail(self.create_data_query())
        context["wall_component"] = tables.ComponentTable(
            self.create_building_table("wall")
        )
        context["wall_lca"] = tables.LCATable(self.create_building_table("wall"))
        context["floor_component"] = tables.ComponentTable(
            self.create_building_table("floor")
        )
        context["floor_lca"] = tables.LCATable(self.create_building_table("floor"))
        context["roofbase_component"] = tables.ComponentTable(
            self.create_building_table("roofbase")
        )
        context["roofbase_lca"] = tables.LCATable(
            self.create_building_table("roofbase")
        )
        return context


class BuildingCreate(generic.CreateView):
    """View for creating new project"""

    template_name = "building_form.html"
    model = models.Building
    form_class = forms.CreateBuilding
    success_url = reverse_lazy("building:buildings")

    def form_valid(self, form):
        form.instance.project = sort_project(form.instance.project)
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class BuildingDelete(generic.DeleteView):
    """Delete an existing building"""

    template_name = "building_confirm_delete.html"
    model = models.Building
    success_url = reverse_lazy("building:buildings")


class BuildingUpdate(generic.UpdateView):
    """Update existing buildings"""

    model = models.Building
    form_class = forms.UpdateBuilding
    template_name = "building_update.html"
    success_url = reverse_lazy("building:buildings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Convert the project data to JSON and pass it to the template
        context["project_json"] = json.dumps(self.object.project)

        return context

    @staticmethod
    def get_uvalue(project: dict, component: str):
        instance = calc.CalcUValue(project, models.Material)
        return instance.calc_u(component)


class MateriaList(FilterView, SingleTableView):
    """View for showing the materials"""

    table_class = tables.MaterialTable
    table_pagination = {"per_page": 10}
    template_name = "material_list.html"

    filterset_class = filters.MaterialFilter

    def get_queryset(self):
        return models.Material.objects.all()


class MaterialCreate(generic.CreateView):
    template_name = "material_form.html"
    models = models.Material
    form_class = forms.CreateMaterial
    success_url = reverse_lazy("building:materials")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class MaterialDelete(generic.DeleteView):
    """Delete an existing material"""

    template_name = "material_confirm_delete.html"
    model = models.Material
    success_url = reverse_lazy("building:materials")


class MaterialUpdate(generic.UpdateView):
    """Update existing material"""

    model = models.Material
    fields = "__all__"
    template_name = "material_update.html"
    success_url = reverse_lazy("building:materials")
