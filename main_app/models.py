from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from .seed import potion_bottles

# Create your models here.
color_choices = [
    (potion_bottles[0], "Purple"),
    (potion_bottles[1], "Pink"),
    (potion_bottles[2], "Blue"),
    (potion_bottles[3], "Green"),
    (potion_bottles[4], "Red"),
    (potion_bottles[5], "Yellow"),
    (potion_bottles[6], "Orange")
]


class Potion(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=1300)
    effects = models.CharField(max_length=1300)
    color = models.CharField(
        max_length=100, choices=color_choices, default=color_choices[0][0])
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
