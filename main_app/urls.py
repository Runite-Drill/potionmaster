from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),

    #URL for signup
    path('accounts/signup/', views.signup, name="signup")
]