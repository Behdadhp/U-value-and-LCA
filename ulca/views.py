import json

from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["compare_form"] = forms.CompareBuildings()
        return context

    def post(self, request, *args, **kwargs):
        form = forms.CompareBuildings(request.POST)
        if form.is_valid():
            first_building = form.cleaned_data.get("first_building")
            second_building = form.cleaned_data.get("second_building")
            return redirect(
                "building:compareBuilding",
                first_building=first_building,
                second_building=second_building,
            )
        else:
            return self.get(request, *args, **kwargs)


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

    def get_success_url(self):
        latest_building = models.Building.objects.last()
        if latest_building:
            return reverse("building:updateBuilding", args=[latest_building.pk])
        else:
            return reverse("building:buildings")

    def form_valid(self, form):
        sorted_dict = {}
        for component in form.instance.project:
            sorted_dict[component] = sort_project(form.instance.project, component)
        form.instance.project = sorted_dict
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

    def get_success_url(self):
        current_model = self.get_object()
        if current_model:
            return reverse("building:updateBuilding", args=[current_model.pk])
        else:
            return reverse("building:buildings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Convert the project data to JSON and pass it to the template
        context["project_json"] = json.dumps(self.object.project)

        return context


class BuildingCompare(generic.TemplateView, MultiTableMixin):
    """Comparing two projects"""

    template_name = "building_compare.html"

    @staticmethod
    def create_building_table(building, component):
        """Provides data for creating tables"""

        return [
            {key: building.project[component][key]}
            for key in building.project[component].keys()
            if isinstance(building.project[component][key], dict)
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        first_building = models.Building.objects.get(
            name=self.kwargs.get("first_building")
        )
        second_building = models.Building.objects.get(
            name=self.kwargs.get("second_building")
        )

        filter_first_building = models.Building.objects.filter(
            name=self.kwargs.get("first_building")
        )
        filter_second_building = models.Building.objects.filter(
            name=self.kwargs.get("second_building")
        )

        context["uvalue_table_first_building"] = tables.BuildingDetail(
            filter_first_building
        )

        context["uvalue_table_second_building"] = tables.BuildingDetail(
            filter_second_building
        )

        context["first_building"] = first_building
        context["second_building"] = second_building

        context["wall"] = calc.FilterDifferences(
            first_building, second_building
        ).filter_wall(first_building, second_building)

        context["roof"] = calc.FilterDifferences(
            first_building, second_building
        ).filter_roof(first_building, second_building)

        context["floor"] = calc.FilterDifferences(
            first_building, second_building
        ).filter_floor(first_building, second_building)

        context["wall_lca_first_building"] = tables.LCATable(
            self.create_building_table(first_building, "wall")
        )
        context["wall_lca_second_building"] = tables.LCATable(
            self.create_building_table(second_building, "wall")
        )

        context["roof_lca_first_building"] = tables.LCATable(
            self.create_building_table(first_building, "roofbase")
        )
        context["roof_lca_second_building"] = tables.LCATable(
            self.create_building_table(second_building, "roofbase")
        )

        context["floor_lca_first_building"] = tables.LCATable(
            self.create_building_table(first_building, "floor")
        )
        context["floor_lca_second_building"] = tables.LCATable(
            self.create_building_table(second_building, "floor")
        )

        return context


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
