from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
    
# model for the user profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profile_images', blank=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    specialty = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    personalDescription = models.TextField(max_length=200, blank=True, verbose_name="Personal Description")
    isCooker = models.BooleanField(default=False, verbose_name="Cooker")
    isDinner = models.BooleanField(default=False, verbose_name="Diner")
    isBestCooker = models.BooleanField(default=False, verbose_name="Best Cooker")

    def __str__(self):
        return u'{0}'.format(self.user.username)

# model for the categories
class Category(models.Model):
    NAME_MAX_LENGTH = 30
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, default="Category Not Selected")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    # defining the auto creation of the slug
    def save(self, *args, **kwargs):
       self.slug = slugify(self.name)
       super(Category, self).save(*args, **kwargs)

    # setting the plural of categorys
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# model for the meals
class Meal(models.Model):
    TITLE_MAX_LENGTH = 30
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    price = models.FloatField(default=0)
    picture = models.ImageField()
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default="Category Not Selected")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    ingredients = models.CharField(max_length=250, default="")
    recipe = models.TextField(max_length=250, default="")

    def __str__(self):
        return self.title

# model for the ingredient
class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    vegetable = models.CharField(max_length=128, blank=True)
    typeofmeat = models.CharField(max_length=128, blank=True, verbose_name="Type of Meat")
    meal = models.ManyToManyField(Meal)

    def __str__(self):
        return self.name

# model for the review
class Review(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    rating = models.PositiveIntegerField(default=5)
    content = models.CharField(max_length=200)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)

    # setting the plural of review
    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.title

# model for the allergy
class Allergy(models.Model):
    name = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(UserProfile)

    # setting the plural of allergy
    class Meta:
        verbose_name_plural = 'Allergies'

    def __str__(self):
        return self.name

# model for the request
class Request(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField()
    name = models.CharField(max_length=30)
    email = models.EmailField()
    content = models.CharField(max_length=200)
    message = models.TextField()
    dinner = models.PositiveIntegerField(default=None)
    cooker = models.PositiveIntegerField(default=None)

    # setting the plural of request
    class Meta:
        verbose_name_plural = 'Requests'

    def __str__(self):
        return self.name

# model for the tag
class Tags(models.Model):
    name = models.CharField(max_length=30, unique= True)
    meal = models.ManyToManyField(Meal)

    def __str__(self):
        return self.name