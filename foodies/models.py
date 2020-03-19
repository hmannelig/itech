from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    name = models.CharField(max_length=30, blank=True)
    adress = models.CharField(max_length=100, blank=True)
    personalDescription = models.CharField(max_length=200,  blank=True)
    isCooker = models.BooleanField( default=False) # user needs to select from a box if he is gonna be a cooker or a dinner
    isDnner = models.BooleanField( default=False)
    isBestCooker= models.BooleanField( default=False)
    #role_id= models.ForeignKey()

    def __str__(self):
        return self.user.username

class Review(models.Model):
    title = models.CharField(max_length=50 )
    date = models.DateField()
    # rating = models.PositiveSmallIntegerField(default=0, max=5)
    content = models.CharField(max_length=200)
    #user = models.ForeignKey() #NEEDS TO BE SPECIFIED

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.title

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

class Request(models.Model):
    title = models.CharField(max_length=30, unique=True)
    date = models.DateField()
   #price = models.ForeignKey() #NEEDS TO BE SPECIFIED
    name = models.CharField(max_length=30)
    email = models.EmailField()
    content = models.CharField(max_length=200)
    message = models.TextField()
    #user = models.ForeignKey() #NEEDS TO BE SPECIFIED
    #meal = models.ForeignKey() #NEEDS TO BE SPECIFIED

    class Meta:
        verbose_name_plural = 'Requests'

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=30, unique= True)
    #meal = models.ManyToManyField() #NEEDS TO BE SPECIFIED

    def __str__(self):
        return self.name