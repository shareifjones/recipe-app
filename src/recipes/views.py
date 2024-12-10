from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from .models import Recipe
from .forms import RecipesSearchForm
import pandas as pd
from django.utils.safestring import mark_safe
# To protect class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Home View
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Recipe List View with Search Functionality
# views.py
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    context_object_name = "recipes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RecipesSearchForm(self.request.GET or None)
        context['form'] = form

        if form.is_valid():
            recipe_name = form.cleaned_data.get('recipe_name')
            ingredient_name = form.cleaned_data.get('ingredient_name')

            # Filter recipes based on user input
            queryset = Recipe.objects.all()
            if recipe_name:
                queryset = queryset.filter(name__icontains=recipe_name)
            if ingredient_name:
                queryset = queryset.filter(ingredients__icontains=ingredient_name)

            # Convert QuerySet to Pandas DataFrame
            recipes_df = pd.DataFrame.from_records(
                queryset.values('id', 'name', 'ingredients', 'cooking_time')
            )

            # Modify 'name' to include a clickable link to the recipe details page
            recipes_df['name'] = recipes_df.apply(
                lambda row: f'<a href="{reverse("recipes:recipes_detail", args=[row["id"]])}">{row["name"]}</a>', axis=1
)


            context['table'] = recipes_df.to_html(classes='table table-striped', index=False, escape=False)

        return context




# Recipe Detail View
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipes_detail.html'


