from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title
