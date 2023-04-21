from django.db import models


class Building(models.Model):
    """ORM representation of the Projects"""

    name = models.CharField(max_length=64, blank=False, null=False)
    project = models.JSONField(blank=False, null=False)
    wall = models.CharField(max_length=128, blank=True)
    roof = models.CharField(max_length=128, blank=True)
    floor = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def get_wall(self):
        """Get the wall from Project"""
        return self.project["wall"]

    def get_roof(self):
        """Get the roof from Project"""
        return self.project["roof"]

    def get_floor(self):
        """Get the floor from Project"""
        return self.project["floor"]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """Save the elements to model"""

        # get the wall
        self.wall = self.get_wall()

        # get the roof
        self.roof = self.get_roof()

        # get the floor
        self.floor = self.get_floor()

        super().save(force_insert, force_update, using, update_fields)
