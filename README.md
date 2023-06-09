# Website

This website is going to be created for calculating the U value and LCA(Life Cycle Assessment).
The initial idea is to receive a JSON and read the data in order to calculate
and give the result in a PDF format.
Data is created by a plugin which is deployed in Revit and it converts the 3D model to 
a JSON. This website belongs to a Master Thesis in civil engineering.

[Click here ](https://github.com/Behdadhp/revit_plugin) for plugin.

# Data

Data for each project should be provided in this format:

```JSON
{
  "floor": {
    "material1": {
      "id": 1
      "thickness": "number in mm"
    },
    "material2": {
      "id": 2
      "thickness": "number in mm"
    },
    "...",
    "area": "number in m2"
  },
  "roofbase": {
    "material1": {
      "id": 1
      "thickness": "number in mm"
    },
    "...",
    "area": "number in m2"
  },
  "wall": {
    "material1": {
      "id": 1
      "thickness": "number in mm"
    },
    "...",
    "area": "number in m2"
  }
}

```

The "area" mentioned above is the total area of each component e.g. wall, floor and roof.

# Attention
This app is not synced with any databases yet, so before creating the project
you need to provide the infos for material in the app. The name of materials should
be exactly as same as the material in the project, otherwise it will raise an error.

# Calculating the LCA

The LCA (Life Cycle Assessment) is calculating base on "Assessment system for
sustainable building". [Click here ](https://www.bnb-nachhaltigesbauen.de/en/assessment-system/office-buildings/)
for more information.

# Source

Images used for layers in this project are coming from [eLCA](https://www.bauteileditor.de/)
