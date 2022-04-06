from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Potion, Ingredient, Recipe, IngredientQuantity
import json
import uuid
import boto3
import ast


S3_BASE_URL = 'https://s3-us-west-2.amazonaws.com/'
BUCKET = 'potionmaster'



# Create your views here.
def home(request):
    return render(request, 'home.html')

def cauldron(request, pk):
    potion = Potion.objects.get(id=pk)
    ingredients = Ingredient.objects.all()
    ingredient_list = []
    for ingredient in ingredients:
        new_ingredient={
            "id" : ingredient.id,
            "name" : ingredient.name,
            "image" : ingredient.image,
        }
        ingredient_list.append(new_ingredient)
    return render(request, 'cauldron.html', {'potion': potion, 'ingredients': ingredient_list})

def potion_detail(request, pk):
    potion = Potion.objects.get(id=pk)
    return render(request, 'potion/detail.html', {'potion':potion})

# @login_required
def potion_index(request):  
    potions = Potion.objects.all()
    return render(request, 'potion/index.html', {'potions': potions})

def ingredient_index(request):  
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient/index.html', {'ingredients': ingredients})

def ingredient_detail(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    return render (request, 'ingredient/detail.html', {'ingredient':ingredient})

def add_photo(request, ingredient_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient.image = url
            ingredient.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('ingredient_detail', ingredient_id=ingredient_id)


# @login_required
class PotionCreate(CreateView):
    # prompt = input("Do you want to create a potion?")
    model = Potion
    fields = []



    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form) #calls form_valid in parent class

class IngredientCreate(CreateView):
    model = Ingredient
    fields = ['name']

    # def form_valid(self,form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form) #calls form_valid in parent class

class PotionDelete(LoginRequiredMixin, DeleteView):
    model = Potion
    success_url = '/potion/index/'

class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = '/ingredient/index/'

# class PotionUpdate(LoginRequiredMixin, UpdateView):
#     model = Potion
#     fields = ['name', 'purpose', 'effects']

def potion_update(request, potion_id):
    #quantity comes from the frontend
    recipe = Recipe.objects.create(potion=potion_id)
    print(request.POST['recipeData'])
    print(ast.literal_eval(request.POST['recipeData']))
    for obj in ast.literal_eval(request.POST['recipeData']):
        print(type(obj))
        # print(type(obj['ingredient']['id']))
        ingredient = Ingredient.objects.get(id=int(obj['ingredient']))
        ingredient_quantity = IngredientQuantity.objects.create(quantity=int(obj['quantity']), ingredient=ingredient)

        print(ingredient)
        print(ingredient_quantity)

        recipe.quantity = ingredient_quantity
        # recipe.quantity.add(ingredient_quantity)
    return reverse('potion_detail',pk=potion_id)

   
# @login_required
def assoc_ingredient(request, recipe_id, ingredient_id):
    Potion.objects.get(recipe_id).ingredient.add(ingredient_id)
    return render('potion/detail', {'potion'})

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