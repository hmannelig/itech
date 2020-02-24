from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128
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

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField(max_length=URL_MAX_LENGTH)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    name = models.CharField(max_length=30, unique=True)
    adress = models.CharField(max_length=100, unique=True)
    personalDescription = models.CharField(max_length=200,  blank=True)
    isCooker = models.CheckboxInput( null=False) # user needs to select from a box if he is gonna be a cooker or a dinner
    isDnner = models.CheckboxInput( null=False)
    isBestCooker= models.CheckboxInput( null=False)
    role_id= models.ForeignKey() #NEEDS TO BE SPECIFIED
    

    def __str__(self):
        return self.user.username

class Review(models.Model):
    title = models.CharField(max_length=50 )
    date = models.DateField()
    rating = model.PositiveSmallIntegerField (default=0, max=5)
    content = models.CharField(max_length=200)
    user = models.ForeignKey() #NEEDS TO BE SPECIFIED

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.title



class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    vegetable = models.CharField(max_length=128, blank=True)
    typeofmeat = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

class Allergy(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Allergies'

    def __str__(self):
        return self.name
