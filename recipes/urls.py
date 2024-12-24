from django.urls import path
from .views import home, RecipeDetailView, RecipeListView, get_chart, AddRecipeView
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),  # This is the home URL pattern
    path('list/<int:pk>', RecipeDetailView.as_view(), name='recipes_detail'),
    path('list/', RecipeListView.as_view(), name='recipes_list'),
    path("generate-chart/", get_chart, name="generate_chart"),
    path('add/', AddRecipeView.as_view(), name='add_recipe'),
    path('about/', views.about_me, name='about_me'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)