from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        ordering = ['name']

