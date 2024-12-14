from django.test import TestCase
from .models import Recipe
from .forms import RecipesSearchForm
from django.urls import reverse
from django.contrib.auth.models import User

class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name='Pasta', 
            ingredients='sauce, noodles',
            cooking_time=15,
            difficulty='Intermediate'
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, 'Pasta')
        self.assertEqual(self.recipe.ingredients, 'sauce, noodles')
        self.assertEqual(self.recipe.cooking_time, 15)
        self.assertEqual(self.recipe.difficulty, 'Intermediate')

    def test_recipe_update(self):
        self.recipe.name = 'Updated Recipe'
        self.recipe.save()
        updated_recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(updated_recipe.name, 'Updated Recipe')

    def test_recipe_deletion(self):
        recipe_id = self.recipe.id
        self.recipe.delete()
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe_id)

    def test_calc_difficulty_method(self):
        self.recipe.ingredients = "pasta, garlic"
        self.recipe.cooking_time = 5
        self.recipe.calc_difficulty()
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, "Easy")


class RecipeFormTest(TestCase):
    def test_valid_form(self):
        form = RecipesSearchForm(data={
            'recipe_name': 'Pasta',
            'ingredient_name': 'Noodles',
            'chart_type': '#1'
        })
        self.assertTrue(form.is_valid())


    def test_field_constraints(self):
        form = RecipesSearchForm(data={
            'recipe_name': 'A' * 121,  # Exceed max_length
            'ingredient_name': 'Noodles',
            'chart_type': '#1'
        })
        self.assertFalse(form.is_valid())


class RecipeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        Recipe.objects.create(name='Pasta', ingredients='sauce, noodles', cooking_time=15, difficulty='Easy')
        Recipe.objects.create(name='Pizza', ingredients='cheese, dough', cooking_time=30, difficulty='Medium')

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_recipe_list_view_accessible(self):
        response = self.client.get(reverse('recipes:recipes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')

    def test_search_functionality(self):
        response = self.client.get(reverse('recipes:recipes_list'), {'recipe_name': 'Pasta'})
        self.assertContains(response, 'Pasta')
        self.assertNotContains(response, 'Pizza')

    def test_chart_display(self):
        response = self.client.get(reverse('recipes:recipes_list'), {'chart_type': '#1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('chart', response.context)


class RecipeDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.recipe = Recipe.objects.create(
            name='Pasta', 
            ingredients='sauce, noodles', 
            cooking_time=15, 
            difficulty='Easy'
        )

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:recipes_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_detail.html')
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.ingredients)
        self.assertContains(response, self.recipe.cooking_time)
        self.assertContains(response, self.recipe.difficulty)

    def test_invalid_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:recipes_detail', args=[999]))
        self.assertEqual(response.status_code, 404)


class HomePageTest(TestCase):
    def test_home_page_accessible(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

