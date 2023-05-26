from . import data


class Calc:
    def __init__(self, project, material):
        """Initialize project and material"""

        self.project = project
        self.material = material

    def get_material(self, layer):
        """Gets the material, if not present raises and error"""

        try:
            return self.material.objects.get(name=layer)
        except self.material.DoesNotExist:
            raise NameError(
                "Material '{}' does not exist. You need to first add it to the material.".format(
                    layer
                )
            )

    def get_area_of_component(self, component):
        """Gets the area of each component, if not present raises and error"""
        try:
            return self.project[component]["area"]
        except KeyError:
            raise KeyError(
                "Area for '{}' does not exist. You need to first add it to the component.".format(
                    component
                )
            )


class CreateProject(Calc):
    def create_dictionary_for_each_layer(self, component):
        """Creates a dictionary for attributes of each layer of requested components"""

        project = self.project
        area = float(self.get_area_of_component(component))

        for layer in project[component]:
            if isinstance(project[component][layer], dict):
                material = self.get_material(layer)
                project[component][layer]["lambda"] = material.lamb
                project[component][layer]["area"] = area  # m2
                project[component][layer]["volume"] = (
                    area * project[component][layer]["thickness"] * 10**-3
                )  # m2 * mm
                project[component][layer]["mass"] = (
                    area
                    * project[component][layer]["thickness"]
                    * 10**-3
                    * material.rho
                )  # m2 * mm * rho

        return project[component]

    def create_dict(self):
        """Creates a dictionary from projects based on attributes of layers"""

        project_dict = {}
        project = self.project
        for item in project:
            component = self.create_dictionary_for_each_layer(item)
            project_dict.update({item: component})
        return project_dict

    def heat_transfer_resistance(self):
        """Adds heat transfer resistance based on the type of components to the dictionary"""

        project = self.create_dict()

        for el in project:
            if el == "wall":
                project["wall"]["Rsi"] = data.heat_transfer_resistance["Rsi"][
                    "horizontal"
                ]
                project["wall"]["Rse"] = data.heat_transfer_resistance["Rse"]
            elif el == "roofbase":
                project["roofbase"]["Rsi"] = data.heat_transfer_resistance["Rsi"][
                    "upward"
                ]
                project["roofbase"]["Rse"] = data.heat_transfer_resistance["Rse"]
            else:
                project["floor"]["Rsi"] = data.heat_transfer_resistance["Rsi"][
                    "downward"
                ]
                project["floor"]["Rse"] = 0

        return project

    def project_with_attr(self):
        """Returns the final dictionary of projects with the added attributes"""

        return self.heat_transfer_resistance()


class CalcUValue(CreateProject):
    def calc_rt(self, component):
        """Calculates the rt"""
        rt = 0
        project = self.project_with_attr()
        project_data = project[component]
        values = project_data.values()
        for item in values:
            if isinstance(item, dict):
                # input is in mm, it needs to convert to m
                rt += (item["thickness"] / 1000) / item["lambda"]
        rt += project_data["Rsi"] + project_data["Rse"]

        return rt

    def calc_u(self, component):
        """Calculates the U"""

        return round(1 / self.calc_rt(component), 3)


class CalcLCA(CreateProject):
    @staticmethod
    def calc_for_each_balance(material, multiplier):
        """adds a dictionary containing material's balance multiply in multiplier"""

        return {
            "Herstellungsphase": round(material["Herstellungsphase"] * multiplier, 3),
            "Erneuerung": round(material["Erneuerung"] * multiplier, 3),
            "Energiebedarf": round(material["Energiebedarf"] * multiplier, 3),
            "Lebensendphase": round(material["Lebensendphase"] * multiplier, 3),
        }

    def gets_multiplier(self, component, layer, material):
        """creates multiplier based on the type of material"""

        project = self.project_with_attr()
        if material.type == "area":
            return project[component][layer]["area"]
        elif material.type == "volume":
            return project[component][layer]["volume"]
        else:
            return project[component][layer]["mass"]

    def calc_lca(self, component):
        """creates a dictionary for each environmental impacts and adds them
        to each layer in the project"""

        project = self.project_with_attr()
        for layer in project[component]:
            if isinstance(project[component][layer], dict):
                material = self.get_material(layer)

                multiplier = self.gets_multiplier(component, layer, material)
                project[component][layer]["gwp"] = self.calc_for_each_balance(
                    material.GWP, multiplier
                )
                project[component][layer]["odp"] = self.calc_for_each_balance(
                    material.ODP, multiplier
                )
                project[component][layer]["pocp"] = self.calc_for_each_balance(
                    material.POCP, multiplier
                )
                project[component][layer]["ap"] = self.calc_for_each_balance(
                    material.AP, multiplier
                )
                project[component][layer]["ep"] = self.calc_for_each_balance(
                    material.EP, multiplier
                )

        return project
