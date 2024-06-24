# myapp/models.py
from django.db import models

class EntitiesMaster(models.Model):
    artist_name = models.CharField(max_length=255)
    program_name = models.CharField(max_length=255)
    artist_role = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    auditorium = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return f'{self.artist_name} - {self.program_name}'
