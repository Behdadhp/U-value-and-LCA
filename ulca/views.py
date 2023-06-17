import json
import os

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

from django.http import HttpResponse
from reportlab.pdfgen import canvas

import tkinter as tk
from tkinter import filedialog


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
        context["model"] = models.Building.objects.get(id=self.get_building_id())
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
        if form.instance.project_document and not form.instance.project_document.open(
            "r"
        ).name.endswith(".txt"):
            raise ValueError("Please provide a valid file. It should be .txt.")

        sorted_dict = {}
        for component in form.instance.choose_project():
            sorted_dict[component] = sort_project(
                form.instance.choose_project(), component
            )
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

    def save_model_to_file(self):
        current_model = self.get_object().project

        # Create the Tkinter root window
        root = tk.Tk()
        root.withdraw()

        # Prompt the user to select the save location
        save_location = filedialog.asksaveasfilename(
            initialdir="/",
            title="Select the path and file name to save the file",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if save_location:
            save_location = os.path.splitext(save_location)[0] + ".txt"
            with open(save_location, "w") as file:
                file.write(str(current_model))
            print(f"Model saved to {save_location}.")
        else:
            return reverse("building:buildings")

    def post(self, request, *args, **kwargs):
        if "save_model_button" in request.POST:
            self.save_model_to_file()
        return super().post(request, *args, **kwargs)


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
    form_class = forms.UpdateMaterial

    template_name = "material_update.html"

    def get_success_url(self):
        current_model = self.get_object()
        if current_model:
            return reverse("building:updateMaterial", args=[current_model.pk])
        else:
            return reverse("building:materials")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Convert the project data to JSON and pass it to the template
        context["material"] = self.object

        return context


class PDFView(generic.View):
    @staticmethod
    def get(request, *args, **kwargs):
        first_building = models.Building.objects.get(name=kwargs["first_building"])
        second_building = models.Building.objects.get(name=kwargs["second_building"])
        # Filter the components based on the changes:

        wall = calc.FilterDifferences(first_building, second_building).filter_wall(
            second_building, first_building
        )

        floor = calc.FilterDifferences(first_building, second_building).filter_floor(
            second_building, first_building
        )

        roof = calc.FilterDifferences(first_building, second_building).filter_roof(
            second_building, first_building
        )

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="changes.pdf"'

        p = canvas.Canvas(response)

        textobject = p.beginText(20, 750)

        textobject.textLine(f"Name of new project: {second_building.name}")

        # Check if there is any changes in the component:
        if len(wall) > 0:
            textobject.textLine(f"{len(wall)} Change(s) for Wall:")

            for key, value in wall.items():
                material = next(iter(value[0]))
                textobject.textLine(
                    f'      {key}: {material} thickness: {value[0][material]["thickness"]} mm, layer:{value[0][material]["id"]} '
                )
        else:
            textobject.textLine("No changes for Wall")

        if len(roof) > 0:
            textobject.textLine(f"{len(roof)} Change(s) for Roof:")

            for key, value in roof.items():
                material = next(iter(value[0]))
                textobject.textLine(
                    f'      {key}: {material} thickness: {value[0][material]["thickness"]} mm, layer:{value[0][material]["id"]} '
                )
        else:
            textobject.textLine("No changes for Roof")

        if len(floor) > 0:
            textobject.textLine(f"{len(floor)} Change(s) for Floor:")

            for key, value in floor.items():
                material = next(iter(value[0]))
                textobject.textLine(
                    f'      {key}: {material} thickness: {value[0][material]["thickness"]} mm, layer:{value[0][material]["id"]} '
                )
        else:
            textobject.textLine("No changes for Floor")

        # Generate the changes
        p.drawText(textobject)

        p.showPage()
        p.save()

        return response
