from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.



class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(default="https://s3-us-west-2.amazonaws.com/potionmaster/b20738.png",blank=True, null=True, max_length=2000) 
    # image = models.ImageField(default=None, blank=True, null=True, upload_to="main_app/static/images")

    def get_absolute_url(self):
        return reverse('cauldron', kwargs = {'pk': self.id})

class IngredientQuantity(models.Model):
    quantity = models.IntegerField(MinValueValidator(1))
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

class Recipe(models.Model):
    quantity = models.ForeignKey(IngredientQuantity, on_delete=models.CASCADE,blank=True, null=True)

class Potion(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=1300)
    effects = models.CharField(max_length=1300)
    color = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True, default=None) 
    
    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse('cauldron', kwargs = {'pk': self.id})

