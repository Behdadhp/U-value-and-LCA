from django.urls import path
from . import views

app_name = "building"

urlpatterns = [
    path("buildings/", views.BuildingList.as_view(), name="buildings"),
    path("buildings/<int:pk>", views.BuildingDetails.as_view(), name="details"),
    path("buildings/new/", views.BuildingCreate.as_view(), name="create"),
    path("buildings/delete/<int:pk>", views.BuildingDelete.as_view(), name="delete"),
    path("buildings/update/<int:pk>", views.BuildingUpdate.as_view(), name="update"),
]
