from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Potion, Ingredient

# Create your views here.
def home(request):
    return render(request, 'home.html')

def cauldron(request):
    return render(request, 'cauldron.html')

def potion_detail(request, potion_id):
    potion = Potion.objects.get(id=potion_id)
    return render(request, 'potion/detail.html', {'potion':potion})

# @login_required
def potion_index(request):  
    potions = Potion.objects.all()
    return render(request, 'potion/index.html', {'potions': potions})

def ingredient_index(request):  
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient/index.html', {'ingredients': ingredients})

# @login_required
class PotionCreate(CreateView):
    model = Potion
    fields = ['name','purpose','effects','color']

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form) #calls form_valid in parent class

class IngredientCreate(CreateView):
    model = Ingredient
    fields = '__all__'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #save the user to the database
            login(request, user) #login the user
            return redirect('home')
        else:
            error_message = 'Invalid signup - Please try again.'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)