from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from .models import Recipe
from .forms import RecipesSearchForm
import pandas as pd
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from io import BytesIO 
import base64
import matplotlib.pyplot as plt
from django.http import JsonResponse

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
            if ingredient_name:
                queryset = queryset.filter(ingredients__icontains=ingredient_name)

            # Generate chart if recipes exist and a chart type is selected
            recipes_df = pd.DataFrame.from_records(
                queryset.values('name', 'cooking_time', 'difficulty', 'created_date')
            )
            if not recipes_df.empty and chart_type:
                chart = get_chart(chart_type, recipes_df)
                context['chart'] = chart

        # Update context with recipes
        context['filtered_recipes'] = queryset
        return context





# Recipe Detail View
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipes_detail.html'
