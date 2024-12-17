from django.urls import path
from .views import home, RecipeDetailView, RecipeListView, get_chart, AddRecipeView

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),  # This is the home URL pattern
    path('list/<int:pk>', RecipeDetailView.as_view(), name='recipes_detail'),
    path('list/', RecipeListView.as_view(), name='recipes_list'),
    path("generate-chart/", get_chart, name="generate_chart"),
    path('add/', AddRecipeView.as_view(), name='add_recipe'),
]
