from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Potion(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=1300)
    effects = models.CharField(max_length=1300)
    color = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cauldron', kwargs={'pk': self.id})


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(
        default="https://s3-us-west-2.amazonaws.com/potionmaster/b20738.png", blank=True, null=True, max_length=2000)

    def get_absolute_url(self):
        return reverse('cauldron', kwargs={'pk': self.id})


class Recipe(models.Model):
    quantity = models.IntegerField(MinValueValidator(1))
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    potion = models.ForeignKey(Potion, on_delete=models.CASCADE, default=1)
