from django.urls import path
from .views import RecipeViewSet

urlpatterns = [
    path('alldata', RecipeViewSet.as_view(), name='alldata')
]