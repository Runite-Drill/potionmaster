from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("cauldron/",views.cauldron, name="cauldron"),
    path("cauldron/create/",views.PotionCreate.as_view(), name="potion_create"),
    path("ingredient/create/",views.IngredientCreate.as_view(), name="ingredient_create"),

    #URL for signup
    path('accounts/signup/', views.signup, name="signup"), 

    path("potion/index/", views.potion_index, name="potion_index"),
    path("potion/detail/<int:pk>", views.potion_detail, name="potion_detail"),
    path("ingredient/index/", views.ingredient_index, name="ingredient_index"),
]