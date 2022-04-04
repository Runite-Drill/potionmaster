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
    path("potion/delete/<int:potion_id>", views.PotionDelete.as_view(), name="potion_delete"),
    path("potion/detail/edit/<int:pk>", views.PotionUpdate.as_view(), name="potion_edit"),
    path("potion/detail/<int:pk>", views.potion_detail, name="potion_detail"),
    path("ingredient/index/", views.ingredient_index, name="ingredient_index"),
    path("ingredient/delete/<int:ingredient_id>", views.IngredientDelete.as_view(), name="ingredient_delete"),
]