from django.urls import path
from .views import home, RecipeDetailView, RecipeListView, get_chart

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),  # This is the home URL pattern
    path('list/<int:pk>', RecipeDetailView.as_view(), name='recipes_detail'),
    path('list/', RecipeListView.as_view(), name='recipes_list'),
     path("generate-chart/", get_chart, name="generate_chart")
]
