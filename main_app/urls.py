from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("cauldron/",views.cauldron, name="cauldron"),

    #URL for signup
    path('accounts/signup/', views.signup, name="signup"), 

    path("potions/index/", views.potions_index, name="potions_index") 
]