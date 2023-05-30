from django import forms
from . import models
from django.utils.translation import gettext_lazy as _


class CreateBuilding(forms.ModelForm):
    """Form for creating building"""

    class Meta:
        model = models.Building
        fields = ("name", "project")

        help_texts = {
            "name": _("Give a name to this project."),
            "project": _("Paste the json coming from 3D-Model here."),
        }


class CreateMaterial(forms.ModelForm):
    """Form for creating material"""

    class Meta:
        model = models.Material
        fields = (
            "name",
            "rho",
            "lamb",
            "type",
            "GWP",
            "ODP",
            "POCP",
            "AP",
            "EP",
            "url_to_oekobaudat",
        )


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
            field_label = f"{material}"
            initial[field_name] = thickness

            if isinstance(data[material], dict):
                self.fields[field_name] = forms.IntegerField(
                    label=field_label,
                    initial=initial[field_name]["thickness"],
                )

    def save_component(self, component, instance):
        """Loops through all fields. If any change is present,
        the model should get updated"""

        component_data = {}
        for field_name, thickness in self.cleaned_data.items():
            if field_name.startswith(f"{component}_"):
                material = field_name[len(f"{component}_") :]
                component_data[material] = thickness

                instance[material]["thickness"] = thickness

    def save(self, commit=True):
        """Saves the updated fields into model"""

        building = super().save(commit=False)

        self.save_component("floor", building.project["floor"])
        self.save_component("wall", building.project["wall"])
        self.save_component("roof", building.project["roofbase"])

        if commit:
            building.save()

        return building
