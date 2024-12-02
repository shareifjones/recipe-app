from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=255)
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return f"Recipe ID: {self.id} - {self.name}"