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
            difficulty='Easy'
        )
        self.recipe2 = Recipe.objects.create(
            name='Pizza',
            ingredients='cheese, dough',
            cooking_time=20,
            difficulty="Intermediate"
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

    def test_invalid_form(self):
        form = RecipesSearchForm(data={
            'recipe_name': '',
            'ingredient_name': '',
            'chart_type': ''
        })
        self.assertFalse(form.is_valid())

    def test_field_constraints(self):
        form = RecipesSearchForm(data={
            'recipe_name': 'A' * 121,  # Exceed max_length by 1
            'ingredient_name': 'Noodles',
            'chart_type': '#1'
        })
        self.assertFalse(form.is_valid(), "Form should be invalid for recipe_name exceeding max_length.")



class RecipeFormTest(TestCase):
    def test_valid_form(self):
        form = RecipesSearchForm(data={
            'recipe_name': 'Pasta',
            'ingredient_name': 'sauce',
            'chart_type': '#1'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = RecipesSearchForm(data={
            'recipe_name': '',
            'ingredient_name': '',
            'chart_type': ''
        })
        self.assertFalse(form.is_valid())

class RecipeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.recipe1 = Recipe.objects.create(name="Pasta", ingredients="sauce, noodles", cooking_time=20, difficulty="Easy")
        cls.recipe2 = Recipe.objects.create(name="Pizza", ingredients="dough, cheese", cooking_time=30, difficulty="Medium")

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_recipe_list_view_accessible(self):
        response = self.client.get(reverse('recipes:recipes_list'))
        self.assertEqual(response.status_code, 200)

    def test_search_functionality(self):
        response = self.client.get(reverse('recipes:recipes_list'), {'recipe_name': 'Pasta'})
        self.assertContains(response, "Pasta", msg_prefix="Search results should include 'Pasta'.")
        self.assertNotContains(response, "Pizza", msg_prefix="Search results should not include 'Pizza'.")

    def test_chart_display(self):
        response = self.client.get(reverse('recipes:recipes_list'), {'chart_type': '#1'})
        self.assertEqual(response.status_code, 200)
