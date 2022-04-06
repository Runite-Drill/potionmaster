from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("cauldron/<int:pk>",views.cauldron, name="cauldron"),
    path("potion/create/",views.PotionCreate.as_view(), name="potion_create"),
    path("ingredient/create/",views.IngredientCreate.as_view(), name="ingredient_create"),
    path("ingredient/detail/<int:ingredient_id>/", views.ingredient_detail, name="ingredient_detail"),
    path('ingredient/<int:ingredient_id>/add_photo/', views.add_photo, name='add_photo'),

    #URL for signup
    path('accounts/signup/', views.signup, name="signup"), 

    path("potion/index/", views.potion_index, name="potion_index"),
    path("potion/detail/delete/<int:pk>", views.PotionDelete.as_view(), name="potion_delete"),
    path("potion/detail/edit/<int:potion_id>", views.potion_update, name="potion_edit"),
    path("potion/detail/<int:pk>", views.potion_detail, name="potion_detail"),
    path("ingredient/index/", views.ingredient_index, name="ingredient_index"),
    path("ingredient/delete/<int:ingredient_id>", views.IngredientDelete.as_view(), name="ingredient_delete"),
]