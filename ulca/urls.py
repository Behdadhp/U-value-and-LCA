from django.urls import path
from . import views

app_name = "building"

urlpatterns = [
    path("buildings/", views.BuildingList.as_view(), name="buildings"),
    path("buildings/<int:pk>", views.BuildingDetails.as_view(), name="details"),
    path("buildings/new/", views.BuildingCreate.as_view(), name="createProject"),
    path(
        "buildings/delete/<int:pk>",
        views.BuildingDelete.as_view(),
        name="deleteBuilding",
    ),
    path(
        "buildings/update/<int:pk>",
        views.BuildingUpdate.as_view(),
        name="updateBuilding",
    ),
    path(
        "buildings/compare/<str:first_building>/<str:second_building>",
        views.BuildingCompare.as_view(),
        name="compareBuilding",
    ),
    path("materials/", views.MateriaList.as_view(), name="materials"),
    path("materials/new/", views.MaterialCreate.as_view(), name="createMaterial"),
    path(
        "materials/update/<int:pk>",
        views.MaterialUpdate.as_view(),
        name="updateMaterial",
    ),
    path(
        "materials/delete/<int:pk>",
        views.MaterialDelete.as_view(),
        name="deleteMaterial",
    ),
    path(
        "buildings/changespdf/<str:first_building>/<str:second_building>",
        views.PDFView.as_view(),
        name="pdf",
    ),
]
