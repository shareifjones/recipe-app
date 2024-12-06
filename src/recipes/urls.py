from django.urls import path
from .views import home, RecipeDetailView, RecipeListView

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),  # This is the home URL pattern
    path('list/<pk>', RecipeDetailView.as_view(), name='recipes_detail'),
    path('list/', RecipeListView.as_view(), name='recipes_list'),
]
