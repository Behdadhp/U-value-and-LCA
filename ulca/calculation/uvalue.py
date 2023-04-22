from . import data


class UValue:
    def __init__(self, project):
        self.project = project

    def create_json(self):
        project = self.project

        for key in data.material:
            if key in self.project["wall"]:
                self.project["wall"][key]["rho"] = data.material[key]["rho"]
                self.project["wall"][key]["lambda"] = data.material[key]["lambda"]
            elif key in self.project["roof"]:
                self.project["roof"][key]["rho"] = data.material[key]["rho"]
                self.project["roof"][key]["lambda"] = data.material[key]["lambda"]
            elif key in self.project["floor"]:
                self.project["floor"][key]["rho"] = data.material[key]["rho"]
                self.project["floor"][key]["lambda"] = data.material[key]["lambda"]

        return project

    def calc_heat_transfer_resistance(self):
        project = self.create_json()

        for el in project:
            if el == "wall":
                project["wall"]["Rsi"] = data.heat_transfer_resistance["Rsi"][
                    "horizontal"
                ]
                project["wall"]["Rse"] = data.heat_transfer_resistance["Rse"]
            elif el == "roof":
                project["roof"]["Rsi"] = data.heat_transfer_resistance["Rsi"]["upward"]
                project["roof"]["Rse"] = data.heat_transfer_resistance["Rse"]
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
                rt += item["thickness"] / item["lambda"]
        rt += project_data["Rsi"] + project_data["Rse"]

        return rt

    def calc_u(self, component):
        return 1 / self.calc_rt(component)
