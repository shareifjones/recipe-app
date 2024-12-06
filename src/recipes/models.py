from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=255)
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=20, blank=True) # Optional or default value
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')


    
    def get_absolute_url(self):
       return reverse ('recipes:detail', kwargs={'pk': self.pk})
    
    def calc_difficulty(self):
        """Calculate the difficulty of the recipe based on cooking time and ingredients"""
        if self.cooking_time < 10 and len(self.ingredients.split(',')) < 4:
            return "Easy"
        elif self.cooking_time < 10 and len(self.ingredients.split(',')) >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients.split(',')) < 4:
            return "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients.split(',')) >= 4:
            return "Hard"

    def save(self, *args, **kwargs):
        """Override save method to automatically set the difficulty"""
        self.difficulty = self.calc_difficulty()  # Set the difficulty based on the calculation
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"Recipe ID: {self.id} - {self.name}"
