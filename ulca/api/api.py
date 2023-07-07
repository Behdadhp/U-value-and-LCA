from fastapi import FastAPI
import os
import django
from django.core import serializers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from ulca import models

app = FastAPI()


@app.get("/building-model/", tags=["building"])
async def building_model():
    """Endpoint to get building model"""

    model = models.Building.objects.all()
    serialized_model = serializers.serialize("json", model)
    return serialized_model


@app.get("/building-model/{building_id}", tags=["building"])
def building_model_id(building_id: int):
    """Endpoint to get one building"""

    model = models.Building.objects.get(id=building_id)
    return model


@app.get("/material-model/", tags=["material"])
async def material_model():
    """Endpoint to get material model"""

    model = models.Building.objects.all()
    serialized_model = serializers.serialize("json", model)
    return serialized_model


@app.get("/material-model/{material_id]", tags=["material"])
def material_model_id(material_id: int):
    """Endpoint to get one material"""

    model = models.Material.objects.get(id=material_id)
    return model
