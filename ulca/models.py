from django.db import models


class Building(models.Model):
    """ORM representation of the Projects"""

    name = models.CharField(max_length=64, blank=False, null=False)
    project = models.JSONField(blank=False,null=False)

    def __str__(self):
        return self.name
