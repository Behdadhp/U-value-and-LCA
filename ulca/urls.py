from django.urls import path
from . import views

app_name = "building"

urlpatterns = [path("building/", views.BuildingList.as_view(), name="building")]
