from django.test import TestCase
from .models import Recipe
from django.urls import reverse

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
        self.assertEqual(self.recipe.difficulty, 'Intermediate')

    def test_recipe_update(self):
        """Tests the functionality of updating a recipe"""
        self.recipe.name = 'Update Recipe'
        self.recipe.save()
        updated_recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(updated_recipe.name, 'Update Recipe')

    def test_recipe_deletion(self):
        """Tests the functionality of deleting a recipe"""
        recipe_id = self.recipe.id
        self.recipe.delete()
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe_id)

    def test_recipe_list_view(self):
        """Test that the recipe list view renders and includes the recipe name and photo."""
        response = self.client.get(reverse('recipes:recipes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.pic.url)

    def test_recipe_detail_view(self):
        """Test that the recipe detail view renders and displays the correct recipe details."""
        response = self.client.get(reverse('recipes:recipes_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_detail.html')
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.ingredients)
        self.assertContains(response, self.recipe.cooking_time)
        self.assertContains(response, self.recipe.difficulty)
        self.assertContains(response, self.recipe.pic.url)

    def test_home_page(self):
        """Test that the home page renders correctly."""
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

    def test_calc_difficulty_method(self):
        """Test the calc_difficulty method for recipes."""
        self.recipe.ingredients = "pasta, garlic"  # Only 2 ingredients
        self.recipe.cooking_time = 5  # Short cooking time
        self.recipe.calc_difficulty()
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, "Easy")