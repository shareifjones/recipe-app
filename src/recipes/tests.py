from django.test import TestCase
from .models import Recipe

# Create your tests here.

class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name='Pasta', 
            ingredients='sauce, noodles',
            cooking_time=15,
            difficulty='easy'
            )
        
    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, 'Pasta')
        self.assertEqual(self.recipe.ingredients, 'sauce, noodles')
        self.assertEqual(self.recipe.cooking_time, 15)
        self.assertEqual(self.recipe.difficulty, 'easy')

    def test_recipe_update(self):
        self.recipe.name = 'Update Recipe'
        self.recipe.save()
        updated_recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(updated_recipe.name, 'Update Recipe')

    def test_recipe_deletion(self):
        recipe_id = self.recipe.id
        self.recipe.delete()
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe_id)