from django.urls import path, include
from . import views
from .views import typeFly






urlpatterns = [
    path("", views.index, name='index'),
    path("pokemonList/", views.pokemonList, name='pokemonList'),
    path("weightPokemon/", views.weightPokemon, name='weightPokemon'),
    path("typePokemon/<str:pokemon_type>", views.typeGrass, name='filterPokemonByType'),
    path("typeFly/", views.typeFly, name='typeFly'),
    path("pokemonReverse/", views.pokemonReverse, name='pokemonReverse'),
    
]

