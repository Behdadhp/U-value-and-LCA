from django import forms
from . import models
from django.utils.translation import gettext_lazy as _

from .utils import sort_project

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Building


class CreateBuilding(forms.ModelForm):
    """Form for creating building"""

    class Meta:
        model = models.Building
        fields = ("name", "project_json", "project_document")

        help_texts = {
            "name": _("Give a name to this project."),
            "project_json": _("Either paste the JSON direct here"),
            "project_document": _("Or upload the .txt file here"),
        }


class UpdateBuilding(forms.ModelForm):
    """Form for updating building"""

    class Meta:
        model = models.Building
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        """Creates dynamic forms"""

        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})
        project = instance.project

        super().__init__(*args, **kwargs)
        self.populate_fields(project.get("floor"), initial, "floor")
        self.populate_fields(project.get("wall"), initial, "wall")
        self.populate_fields(project.get("roofbase"), initial, "roof")

    def populate_fields(self, data, initial, component):
        """Populates the fields for each component"""

        for material, thickness in data.items():
            field_name = f"{component}_{material}"
            material_of_layers = f"{material}_{component}"
            field_id = f"id_{component}_{material}"

            field_label = f"{material}"
            initial[field_name] = thickness

            if isinstance(data[material], dict):
                self.fields[field_name] = forms.IntegerField(
                    label=field_label,
                    initial=initial[field_name]["thickness"],
                )

                self.fields[field_id] = forms.IntegerField(
                    label=initial[field_name]["id"],
                    initial=initial[field_name]["id"],
                )

                self.fields[material_of_layers] = forms.CharField(
                    label=field_label, initial=material
                )

    def save_component(self, component, instance):
        """Loops through all fields. If any change is present,
        the model should get updated"""

        component_data = {}

        for field_name, value in self.cleaned_data.items():
            # Checks if the thickness has been changed.
            if field_name.startswith(f"{component}_"):
                material = field_name[len(f"{component}_") :]
                component_data[material] = value

                instance[material]["thickness"] = value

            # Checks if the id has been changed.
            elif field_name.startswith(f"id_{component}_"):
                material = field_name[len(f"{component}_") + 3 :]
                component_data[material] = value
                instance[material]["id"] = value

            # Checks if the material has been changed.
            elif field_name.endswith(f"{component}"):
                material = field_name[: -len(f"{component}") - 1]
                if material != value:
                    instance[value] = instance[material]
                    del instance[material]

    def save(self, commit=True):
        """Saves the updated fields into model"""

        building = super().save(commit=False)
        self.save_component("floor", building.project["floor"])
        self.save_component("wall", building.project["wall"])
        self.save_component("roof", building.project["roofbase"])

        if commit:
            # Sort the project before saving in database
            sorted_dict = {}
            for component in building.project:
                sorted_dict[component] = sort_project(building.project, component)
            building.project = sorted_dict

            building.save()

        return building


class UpdateMaterial(forms.ModelForm):
    """Form for updating material"""

    class Meta:
        model = models.Material
        fields = ("name", "rho", "lamb", "type", "url_to_oekobaudat")

    def __init__(self, *args, **kwargs):
        """Creates dynamic forms"""

        super().__init__(*args, **kwargs)
        self.populate_fields("GWP")
        self.populate_fields("ODP")
        self.populate_fields("POCP")
        self.populate_fields("AP")
        self.populate_fields("EP")

    def populate_fields(self, field_name):
        """Populates the fields for the specified module"""

        data = getattr(self.instance, field_name)

        for module, value in data.items():
            field_label = f"{module} "

            self.fields[f"{field_name}_{module}"] = forms.FloatField(
                label=field_label, initial=value
            )

    def save_module(self, module_name, instance):
        """Loops through all fields. If any change is present,
        the model should get updated"""

        module_data = {}

        for field_name, value in self.cleaned_data.items():
            if field_name.startswith(f"{module_name}_"):
                module = field_name[len(f"{module_name}_") :]
                module_data[module] = value

                instance[module] = value

    def save(self, commit=True):
        """Saves the updated fields into model"""

        material = super().save(commit=False)

        self.save_module("GWP", material.GWP)
        self.save_module("ODP", material.ODP)
        self.save_module("POCP", material.POCP)
        self.save_module("AP", material.AP)
        self.save_module("EP", material.EP)

        if commit:
            material.save()

        return material

    @receiver(post_save, sender=models.Material)
    def update_buildings(sender, **kwargs):
        """Retrieve all Building instances and saves all of them again"""

        buildings = Building.objects.all()
        for building in buildings:
            building.save()


class CompareBuildings(forms.Form):
    """Form to compare buildings"""

    first_building = forms.CharField()
    second_building = forms.CharField()
