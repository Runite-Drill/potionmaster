import ast
import boto3
import uuid
import json
from .models import Potion, Ingredient, Recipe
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from tkinter import *
import tkinter.messagebox
from threading import Thread


S3_BASE_URL = 'https://s3-us-west-2.amazonaws.com/'
BUCKET = 'potionmaster'



# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def cauldron(request, pk):
    potion = Potion.objects.get(id=pk)
    ingredients = Ingredient.objects.all()
    ingredient_list = []
    for ingredient in ingredients:
        new_ingredient = {
            "id": ingredient.id,
            "name": ingredient.name,
            "image": ingredient.image,
        }
        ingredient_list.append(new_ingredient)
    return render(request, 'cauldron.html', {'potion': potion, 'ingredients': ingredient_list})


@login_required
def potion_detail(request, pk):
    potion = Potion.objects.get(id=pk)
    return render(request, 'potion/detail.html', {'potion': potion})


def potion_index(request):
    # potions = Potion.objects.filter(user=request.user)
    potions = Potion.objects.all()
    # print(potions)
    # for pot in potions:
    #     print(pot.id)
    return render(request, 'potion/index.html', {'potions': potions})


def ingredient_index(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient/index.html', {'ingredients': ingredients})


@login_required
def ingredient_detail(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    return render(request, 'ingredient/detail.html', {'ingredient': ingredient})


def add_photo(photo_file, ingredient_id):
    # photo-file will be the "name" attribute on the <input type="file">
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
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


class PotionCreate(LoginRequiredMixin, CreateView):
    # prompt = input("Do you want to create a potion?")
    model = Potion
    fields = []

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)  # calls form_valid in parent class


@login_required
def ingredient_create_get(request):
    return render(request, 'ingredient/create.html')


@login_required
def ingredient_create_post(request):
    try:
        ingredient = Ingredient.objects.create(name=request.POST['name'])
        photo_file = request.FILES.get('photo-file', None)
        add_photo(photo_file, ingredient.id)
        return redirect('ingredient_index')

    except:
        root = tkinter.Tk()
        tkinter.messagebox.showerror("Duplicate Ingredient Name",
                             "Duplicate Ingredient Name.\n Please try again")
        root.withdraw()
        root.mainloop()
        return redirect('ingredient_get')


class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = '__all__'


class PotionDelete(LoginRequiredMixin, DeleteView):
    model = Potion
    success_url = '/potion/index/'


class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = '/ingredient/index/'


class PotionUpdate(LoginRequiredMixin, UpdateView):
    model = Potion
    fields = ['name', 'purpose', 'effects', 'color']

    def get_success_url(self):
        return reverse('potion_detail', kwargs={'pk': self.kwargs['pk']})


@ login_required
def potion_submit(request, potion_id):
    # quantity comes from the frontend
    if 'recipeData' in request.POST:
        data = ast.literal_eval(request.POST['recipeData'])
        # print(request.POST['recipeData'])
        # print(type(data))
        if type(data) == dict:
            ingredient = Ingredient.objects.get(id=data['ingredient'])
            Recipe.objects.create(
                quantity=data['quantity'], ingredient=ingredient, potion_id=potion_id)
            return redirect('potion_edit', pk=potion_id)
        else:
            for obj in data:
                ingredient = Ingredient.objects.get(id=obj['ingredient'])
                Recipe.objects.create(
                    quantity=obj['quantity'], ingredient=ingredient, potion_id=potion_id)
        return redirect('potion_edit', pk=potion_id)
    else:
        data = False

    # @login_required


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # save the user to the database
            login(request, user)  # login the user
            return redirect('home')
        else:
            error_message = 'Invalid signup - Please try again.'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


# t = Thread(target=ingredient_create_post)
# t.setDaemon(True)
# t.start()
# 