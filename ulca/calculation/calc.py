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

    def get_nett_area(self):
        """Gets nett area of project"""

        return self.project["wall"]["nett_area"]


class Compare:
    def __init__(self, first_building, second_building):
        """Initialize first and second building model"""

        self.first_building = first_building
        self.second_building = second_building

    def first_project(self):
        """Gets first building project"""

        return self.first_building.project

    def second_project(self):
        """Gets second building project"""

        return self.second_building.project

    @staticmethod
    def get_project_key(component):
        """Returns keys of each component"""

        return list(component.keys())


class CreateProject(Calc):
    def calc_nett_area(self):
        """Calculate the nett area of building"""

        project = self.project
        total_wall_length = project["wall"]["total_wall_length"]
        total_thickness = 0
        for layer in project["wall"]:
            if isinstance(project["wall"][layer], dict):
                thickness = project["wall"][layer]["thickness"]
                total_thickness += thickness
        construction_area = total_thickness / 1000 * float(total_wall_length)
        gross_area = float(project["roofbase"]["area"])

        return gross_area - construction_area

    def create_dictionary_for_each_layer(self, component):
        """Creates a dictionary for attributes of each layer of requested components"""

        project = self.project
        area = float(self.get_area_of_component(component))

        for layer in project[component]:
            if isinstance(project[component][layer], dict):
                material = self.get_material(layer)
                project[component][layer]["lambda"] = material.lamb
                project[component][layer]["area"] = round(area, 3)  # m2
                project[component][layer]["volume"] = round(
                    area * project[component][layer]["thickness"] * 10**-3, 3
                )  # m2 * mm
                project[component][layer]["mass"] = round(
                    area
                    * project[component][layer]["thickness"]
                    * 10**-3
                    * material.rho,
                    3,
                )  # m2 * mm * rho
        project[component]["nett_area"] = round(self.calc_nett_area(), 3)

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
        """Adds a dictionary containing material's balance multiply in multiplier"""

        return {
            "Herstellungsphase": round(material["Herstellungsphase"] * multiplier, 3),
            "Erneuerung": round(material["Erneuerung"] * multiplier, 3),
            "Energiebedarf": round(material["Energiebedarf"] * multiplier, 3),
            "Lebensendphase": round(material["Lebensendphase"] * multiplier, 3),
        }

    def gets_multiplier(self, component, layer, material):
        """Creates multiplier based on the type of material"""

        project = self.project_with_attr()
        if material.type == "area":
            return project[component][layer]["area"]
        elif material.type == "volume":
            return project[component][layer]["volume"]
        else:
            return project[component][layer]["mass"]

    def lca_rating_system(self, component, layer, phase):
        """Calculates the lca rating system for each material"""

        project = self.project_with_attr()
        dic = {}
        lca_rating_system_dic = {}
        lca_rating_gwp = project[component][layer][phase]
        for key, value in lca_rating_gwp.items():
            lca_calculation = value / self.get_nett_area() * 2 / 100
            dic.update({key: lca_calculation})
        lca_rating_system_dic.update(dic)
        return lca_rating_system_dic

    def calc_lca(self, component):
        """Creates a dictionary for each environmental impacts and adds them
        to each layer in the project"""

        project = self.project_with_attr()

        # Calculate the LCA for each material
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

        # Calculate the total LCA for each material
        for layer in project[component]:
            if isinstance(project[component][layer], dict):
                total_gwp = sum(project[component][layer]["gwp"].values())
                total_odp = sum(project[component][layer]["odp"].values())
                total_pocp = sum(project[component][layer]["pocp"].values())
                total_ap = sum(project[component][layer]["ap"].values())
                total_ep = sum(project[component][layer]["ep"].values())

                project[component][layer]["total_lca"] = {
                    "gwp": round(total_gwp, 3),
                    "odp": round(total_odp, 3),
                    "pocp": round(total_pocp, 3),
                    "ap": round(total_ap, 3),
                    "ep": round(total_ep, 3),
                }

        total_gwp_in_component = 0
        total_odp_in_component = 0
        total_pocp_in_component = 0
        total_ap_in_component = 0
        total_ep_in_component = 0

        # Calculate the total LCA for each component
        for layer in project[component]:
            if isinstance(project[component][layer], dict):
                total_gwp_in_component += project[component][layer]["total_lca"]["gwp"]
                total_odp_in_component += project[component][layer]["total_lca"]["odp"]
                total_pocp_in_component += project[component][layer]["total_lca"][
                    "pocp"
                ]
                total_ap_in_component += project[component][layer]["total_lca"]["ap"]
                total_ep_in_component += project[component][layer]["total_lca"]["ep"]

        project[component]["total_gwp_component"] = round(total_gwp_in_component, 3)
        project[component]["total_odp_component"] = round(total_odp_in_component, 3)
        project[component]["total_pocp_component"] = round(total_pocp_in_component, 3)
        project[component]["total_ap_component"] = round(total_ap_in_component, 3)
        project[component]["total_ep_component"] = round(total_ep_in_component, 3)

        # Create the lca rating system for each layer
        for layer in project[component]:
            if isinstance(project[component][layer], dict):
                if "lca_rating_system" not in project[component][layer]:
                    project[component][layer]["lca_rating_system"] = {}

                project[component][layer]["lca_rating_system"].update(
                    {"gwp": self.lca_rating_system(component, layer, "gwp")}
                )
                project[component][layer]["lca_rating_system"].update(
                    {"odp": self.lca_rating_system(component, layer, "odp")}
                )
                project[component][layer]["lca_rating_system"].update(
                    {"pocp": self.lca_rating_system(component, layer, "pocp")}
                )
                project[component][layer]["lca_rating_system"].update(
                    {"ap": self.lca_rating_system(component, layer, "ap")}
                )
                project[component][layer]["lca_rating_system"].update(
                    {"ep": self.lca_rating_system(component, layer, "ep")}
                )

        # Create the total lca rating system for each component
        total_gwp_lca_rating_system = self.calc_total_value_of_rating_system(
            project[component]["total_gwp_component"]
        )
        total_odp_lca_rating_system = self.calc_total_value_of_rating_system(
            project[component]["total_odp_component"]
        )
        total_pocp_lca_rating_system = self.calc_total_value_of_rating_system(
            project[component]["total_pocp_component"]
        )
        total_ap_lca_rating_system = self.calc_total_value_of_rating_system(
            project[component]["total_ap_component"]
        )
        total_ep_lca_rating_system = self.calc_total_value_of_rating_system(
            project[component]["total_ep_component"]
        )

        project[component]["total_gwp_lca_rating_system"] = round(
            total_gwp_lca_rating_system, 3
        )
        project[component]["total_odp_lca_rating_system"] = round(
            total_odp_lca_rating_system, 3
        )
        project[component]["total_pocp_lca_rating_system"] = round(
            total_pocp_lca_rating_system, 3
        )
        project[component]["total_ap_lca_rating_system"] = round(
            total_ap_lca_rating_system, 3
        )
        project[component]["total_ep_lca_rating_system"] = round(
            total_ep_lca_rating_system, 3
        )

        return project

    def calc_total_value_of_rating_system(self, total_value_of_rating_system):
        return total_value_of_rating_system / self.get_nett_area() * 2 / 100


class CompareBuildings(Compare):
    def get_different_materials_name(self, project_one, project_two, component):
        """Loops through 2 components and returns the different materials' name"""

        project_one_keys = self.get_project_key(project_one[component])
        project_two_keys = self.get_project_key(project_two[component])

        list_of_different_materials = []
        for item in project_two_keys:
            material_index = project_two_keys.index(item)
            if project_one_keys[material_index] != project_two_keys[material_index]:
                list_of_different_materials.append(project_one_keys[material_index])

        return list_of_different_materials

    def get_different_materials_thickness(self, project_one, project_two, component):
        """Loops through 2 components and returns the different materials' thickness"""

        project_one_keys = self.get_project_key(project_one[component])
        project_two_keys = self.get_project_key(project_two[component])

        list_of_different_materials = []
        for item in project_two_keys:
            material_index = project_two_keys.index(item)
            if project_one_keys[material_index] == item and isinstance(
                self.second_building.project[component][item], dict
            ):
                if (
                    self.second_building.project[component][item]["thickness"]
                    != self.first_building.project[component][item]["thickness"]
                ):
                    list_of_different_materials.append(item)

        return list_of_different_materials

    @staticmethod
    def merge_two_list(material_list, thickness_list):
        """Merges the material's differences"""

        return material_list + thickness_list

    @staticmethod
    def get_id_of_different_materials(list_of_different_materials, first_project):
        """Gets the id of each different material present in list_of_different_materials"""

        list_of_ids = []
        for item in list_of_different_materials:
            list_of_ids.append(first_project[item]["id"])

        return list_of_ids


class CreateDictOfDifferences(CompareBuildings):
    def differences_in_wall(self):
        """Creates a dict for each component"""

        return self.merge_two_list(
            self.get_different_materials_name(
                self.first_project(), self.second_project(), "wall"
            ),
            self.get_different_materials_thickness(
                self.first_project(), self.second_project(), "wall"
            ),
        )

    def differences_in_roof(self):
        """Creates a dict for each component"""

        return self.merge_two_list(
            self.get_different_materials_name(
                self.first_project(), self.second_project(), "roofbase"
            ),
            self.get_different_materials_thickness(
                self.first_project(), self.second_project(), "roofbase"
            ),
        )

    def differences_in_floor(self):
        """Creates a dict for each component"""

        return self.merge_two_list(
            self.get_different_materials_name(
                self.first_project(), self.second_project(), "floor"
            ),
            self.get_different_materials_thickness(
                self.first_project(), self.second_project(), "floor"
            ),
        )

    def create_dict_of_differences(self):
        return {
            "wall": {
                "diff": self.get_id_of_different_materials(
                    self.differences_in_wall(), self.first_project()["wall"]
                )
            },
            "roof": {
                "diff": self.get_id_of_different_materials(
                    self.differences_in_roof(), self.first_project()["roofbase"]
                )
            },
            "floor": {
                "diff": self.get_id_of_different_materials(
                    self.differences_in_floor(), self.first_project()["floor"]
                )
            },
        }


class FilterDifferences(Compare):
    def create_instance(self):
        instance = CreateDictOfDifferences(self.first_building, self.second_building)
        return instance.create_dict_of_differences()

    def filter_wall(self, first_model, second_model):
        first_project_key = self.get_project_key(self.first_project()["wall"])
        second_project_key = self.get_project_key(self.second_project()["wall"])
        comparison_wall = {}
        counter = 1
        for material_id in self.create_instance()["wall"]["diff"]:
            n = material_id - 1
            comparison_wall[counter] = [
                {
                    first_project_key[n]: first_model.project["wall"].get(
                        first_project_key[n]
                    )
                },
                {
                    second_project_key[n]: second_model.project["wall"].get(
                        second_project_key[n]
                    )
                },
            ]
            counter += 1

        return comparison_wall

    def filter_roof(self, first_model, second_model):
        first_project_key = self.get_project_key(self.first_project()["roofbase"])
        second_project_key = self.get_project_key(self.second_project()["roofbase"])
        comparison_roof = {}
        counter = 1
        for material_id in self.create_instance()["roof"]["diff"]:
            n = material_id - 1
            comparison_roof[counter] = [
                {
                    first_project_key[n]: first_model.project["roofbase"].get(
                        first_project_key[n]
                    )
                },
                {
                    second_project_key[n]: second_model.project["roofbase"].get(
                        second_project_key[n]
                    )
                },
            ]
            counter += 1
        return comparison_roof

    def filter_floor(self, first_model, second_model):
        first_project_key = self.get_project_key(self.first_project()["floor"])
        second_project_key = self.get_project_key(self.second_project()["floor"])
        comparison_floor = {}
        counter = 1
        for material_id in self.create_instance()["floor"]["diff"]:
            n = material_id - 1
            comparison_floor[counter] = [
                {
                    first_project_key[n]: first_model.project["floor"].get(
                        first_project_key[n]
                    )
                },
                {
                    second_project_key[n]: second_model.project["floor"].get(
                        second_project_key[n]
                    )
                },
            ]
            counter += 1

        return comparison_floor
