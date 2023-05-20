from . import data


class UValue:
    def __init__(self, project, material):
        self.project = project
        self.material = material

    def get_each_component(self, component):
        project = self.project

        for item in project[component]:
            if isinstance(project[component][item], dict):
                try:
                    material = self.material.objects.get(name=item)
                    project[component][item]["lambda"] = material.lamb
                except:
                    pass

        return project[component]

    def create_dict(self):
        result_dict = {}
        project = self.project
        for item in project:
            component = self.get_each_component(item)
            result_dict.update({item: component})
        return result_dict

    def calc_heat_transfer_resistance(self):
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

    def calc_rt(self, component):
        rt = 0
        project = self.calc_heat_transfer_resistance()
        project_data = project[component]
        values = project_data.values()
        for item in values:
            if isinstance(item, dict):
                # input is in mm, it needs to convert to m
                rt += (item["thickness"] / 1000) / item["lambda"]
        rt += project_data["Rsi"] + project_data["Rse"]

        return rt

    def calc_u(self, component):
        return round(1 / self.calc_rt(component), 3)
