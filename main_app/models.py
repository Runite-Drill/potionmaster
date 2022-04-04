from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(default=None, blank=True, null=True, max_length=2000) 
    

class Potions(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=1300)
    effects = models.CharField(max_length=1300)
    color = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    ingredients = models.ManyToManyField(Ingredient)
    
    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse('cauldron', kwargs = {})

