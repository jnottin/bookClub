from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    release_date = models.DateField()
    pages = models.IntegerField()
    description = models.TextField()
    photo_url = models.TextField()

    def __str__(self):
        return self.name