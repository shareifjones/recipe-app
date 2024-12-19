from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView 
from .models import Recipe
from .forms import RecipesSearchForm, RecipeForm
import pandas as pd
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from io import BytesIO 
import base64
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.contrib import messages
from django.views import View

# Home View
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Function to Generate Chart
def get_chart(chart_type, data):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111)

    if chart_type == '#1':  # Bar Chart for Cooking Time
        ax.bar(data['name'], data['cooking_time'])
        plt.title('Cooking Time by Recipe')
        plt.xlabel('Recipes')
        plt.ylabel('Cooking Time (minutes)')
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()  # Automatically adjust spacing to prevent cutoff
    elif chart_type == '#2':  # Pie Chart for Recipe Difficulty
        difficulty_counts = data['difficulty'].value_counts()
        ax.pie(difficulty_counts, labels=difficulty_counts.index, autopct='%1.1f%%')
        plt.title('Recipes by Difficulty')
    elif chart_type == '#3':  # Line Chart for Recipes Created Per Day
        data['created_date'] = pd.to_datetime(data['created_date'])
        daily_counts = data['created_date'].value_counts().sort_index()
        ax.plot(daily_counts.index, daily_counts.values, marker='o')
        plt.title('Number of Recipes Created Per Day')
        plt.xlabel('Date')
        plt.ylabel('Number of Recipes')
    else:
        return None

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    return graphic

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    context_object_name = "recipes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RecipesSearchForm(self.request.GET or None)
        context['form'] = form

        # Load all recipes by default
        queryset = Recipe.objects.all()

        if form.is_valid():
            recipe_name = form.cleaned_data.get('recipe_name')
            ingredient_name = form.cleaned_data.get('ingredient_name')
            chart_type = form.cleaned_data.get('chart_type')

            # Filter recipes based on search criteria
            if recipe_name:
                queryset = queryset.filter(name__icontains=recipe_name)
            print(f"Filtered by recipe_name: {queryset}")
            if ingredient_name:
                queryset = queryset.filter(ingredients__icontains=ingredient_name)
            print(f"Filtered by ingredient_name: {queryset}")


            # context['recipes'] = queryset

            # Generate chart if recipes exist and a chart type is selected
             # Check if a chart type is selected
            if chart_type:
                recipes_df = pd.DataFrame.from_records(
                    queryset.values('name', 'cooking_time', 'difficulty', 'created_date')
                )
                if not recipes_df.empty:
                    chart = get_chart(chart_type, recipes_df)
                    context['chart'] = chart
            else:
                # Optional: Add a message to prompt the user
                messages.warning(self.request, "Please select a chart type to generate a chart.")


        # Update context with recipes
        context['filtered_recipes'] = queryset
        return context





# Recipe Detail View
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipes_detail.html'


class AddRecipeView(LoginRequiredMixin, View):
    template_name = 'recipes/add_recipe.html'

    def get(self, request):
        form = RecipeForm()
        return render(request, self.template_name, {'form': form})  # Pass as a dictionary

    def post(self, request):
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()  # Save recipe to the database
            return redirect('recipes:recipes_list')  # Redirect to the recipe list
        return render(request, self.template_name, {'form': form})  # Pass as a dictionary

def about_me(request):
    return render(request, 'recipes/about_me.html')

