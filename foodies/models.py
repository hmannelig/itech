from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 30
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
       self.slug = slugify(self.name)
       super(Category, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Meal(models.Model):
    TITLE_MAX_LENGTH = 30
    URL_MAX_LENGTH = 200
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField(max_length=URL_MAX_LENGTH)
    price = models.FloatField(default=0)
    views = models.IntegerField(default=0)
    #Foreign Key from Meal class to Meal Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    vegetable = models.CharField(max_length=128, blank=True)
    typeofmeat = models.CharField(max_length=128, blank=True)
    #ForeignKey from Ingredient Class to Meal
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Allergy(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Allergies'

    def __str__(self):
        return self.name
