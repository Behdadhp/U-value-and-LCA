from django.urls import path
from . import views

app_name = "building"

urlpatterns = [
    path("buildings/", views.BuildingList.as_view(), name="buildings"),
    path("buildings/<int:pk>", views.BuildingDetails.as_view(), name="details"),
    path("buildings/new/", views.BuildingCreate.as_view(), name="createProject"),
    path("buildings/delete/<int:pk>", views.BuildingDelete.as_view(), name="delete"),
    path("buildings/update/<int:pk>", views.BuildingUpdate.as_view(), name="updateBuilding"),
    path("materials/", views.MateriaList.as_view(), name="materials"),
    path("materials/new/", views.MaterialCreate.as_view(), name="createMaterial"),
    path("materials/update/<int:pk>", views.MaterialUpdate.as_view(), name="updateMaterial"),

]
