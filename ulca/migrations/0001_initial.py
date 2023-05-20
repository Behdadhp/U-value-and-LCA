# Generated by Django 4.2 on 2023-05-20 10:34

from django.db import migrations, models
import ulca.calculation.data


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
                    models.JSONField(
                        default=ulca.calculation.data.building_default_value
                    ),
                ),
                ("wall", models.CharField(blank=True, max_length=128)),
                ("roof", models.CharField(blank=True, max_length=128)),
                ("floor", models.CharField(blank=True, max_length=128)),
                ("wallUvalue", models.CharField(blank=True, max_length=32)),
                ("roofUvalue", models.CharField(blank=True, max_length=32)),
                ("floorUvalue", models.CharField(blank=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="Material",
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
                ("rho", models.FloatField(max_length=8)),
                ("lamb", models.FloatField(max_length=8, verbose_name="lambda")),
                (
                    "GWP",
                    models.JSONField(
                        blank=True,
                        default=ulca.calculation.data.material_default_value,
                        help_text="Global warming potential",
                        null=True,
                    ),
                ),
                (
                    "ODP",
                    models.JSONField(
                        blank=True,
                        default=ulca.calculation.data.material_default_value,
                        help_text="Ozone layer depletion potential",
                        null=True,
                    ),
                ),
                (
                    "POCP",
                    models.JSONField(
                        blank=True,
                        default=ulca.calculation.data.material_default_value,
                        help_text="Ozone creation potential",
                        null=True,
                    ),
                ),
                (
                    "AP",
                    models.JSONField(
                        blank=True,
                        default=ulca.calculation.data.material_default_value,
                        help_text="Acidification potential",
                        null=True,
                    ),
                ),
                (
                    "EP",
                    models.JSONField(
                        blank=True,
                        default=ulca.calculation.data.material_default_value,
                        help_text="Fertilization potential",
                        null=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("mass", "Mass"),
                            ("volume", "Volume"),
                            ("area", "Area"),
                        ],
                        default="volume",
                        max_length=32,
                    ),
                ),
                ("url_to_oekobaudat", models.URLField(blank=True, null=True)),
            ],
        ),
    ]
