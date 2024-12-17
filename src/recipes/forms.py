from django import forms
from .models import Recipe

CHART__CHOICES = (
   ('', 'Select a chart type'),
   ('#1', 'Bar Chart: Cooking Time'),
   ('#2', 'Pie Chart: Recipes by Difficulty'),
   ('#3', 'Line Chart: Recipes Created Per Day')
)
#define class-based Form imported from Django forms
class RecipesSearchForm(forms.Form): 
   recipe_name= forms.CharField(max_length=120, required=False)
   ingredient_name = forms.CharField(max_length=120, required=False)
   chart_type = forms.ChoiceField(choices=CHART__CHOICES, required=False)

class RecipeForm(forms.ModelForm):
   class Meta:
      model = Recipe
      fields = ['name', 'ingredients', 'cooking_time', 'pic']