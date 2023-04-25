from django.urls import path
from . import views

app_name = "building"

urlpatterns = [
    path("buildings/", views.BuildingList.as_view(), name="buildings"),
    path("building/<int:pk>", views.BuildingDetails.as_view(), name="details"),
    path("building/new/", views.BuildingCreate.as_view(), name="create"),
]
