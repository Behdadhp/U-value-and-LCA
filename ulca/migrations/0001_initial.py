# Generated by Django 4.2 on 2023-04-25 19:09

from django.db import migrations, models
import ulca.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Building",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                (
                    "project",
                    models.JSONField(default=ulca.models.jsonfield_default_value),
                ),
                ("wall", models.CharField(blank=True, max_length=128)),
                ("roof", models.CharField(blank=True, max_length=128)),
                ("floor", models.CharField(blank=True, max_length=128)),
                ("wallUvalue", models.CharField(blank=True, max_length=32)),
                ("roofUvalue", models.CharField(blank=True, max_length=32)),
                ("floorUvalue", models.CharField(blank=True, max_length=32)),
            ],
        ),
    ]
