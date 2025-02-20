from django.urls import path
from .views import search_articles,home

urlpatterns = [
    path("search/", search_articles, name="search_articles"),
    path('', home, name='home'),
]

