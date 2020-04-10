from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    edition = models.IntegerField()
    publication_year = models.DateField()
    authors = models.ManyToManyField('Author', related_name='books')


class Author(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        ordering = ['name']

