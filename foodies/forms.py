from django import forms
from betterforms.multiform import MultiModelForm
from foodies.models import Meal, Category, UserProfile, Ingredient, Request, Allergy, Review
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Categories form, help creating new categories in the public views
# Although we don't use this form since users are not able to create categories
# Only super admins can create categories from the admin panel
class CategoryForm(forms.ModelForm):

    # Defining the fields to show, wiht the type of field, length of field
    # help text, required flag and or initial value
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = Category
        fields = ('name',)

# form to create meals
class MealForm(forms.ModelForm):

    # Defining the fields to show, wiht the type of field, length of field
    # help text, required flag and or initial value
    title = forms.CharField(max_length=Meal.TITLE_MAX_LENGTH, help_text="Please enter the title of the meal.", label="Meal Name")
    price = forms.FloatField(help_text="Please enter the price for this meal")
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), help_text="Please select the category for this meal")

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = Meal
        fields = ('title', 'picture', 'price', 'category', 'ingredients', 'recipe')

# form to create ingredients
class IngredientsForm(forms.ModelForm):

    # Defining the fields to show, wiht the type of field, length of field
    # help text, required flag and or initial value
    name = forms.CharField(required=True, help_text="Please enter one ingredient", label="Ingredient Name")
    vegetable = forms.CharField(required=False, help_text="Please enter the vegetables")
    typeofmeat = forms.CharField(required=False, help_text="Please enter the type of meat", label="Type of Meat")
    meal = MealForm

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = Ingredient
        fields = ('name', 'vegetable', 'typeofmeat',)

# This form takes the IngredientsForm and the MealForm at the same time for being handled in views
class mealIngredientMultiForm(MultiModelForm):
    form_classes = {
        'meal': MealForm,
        'ingredients': IngredientsForm,
    }

# form to for the register of the users
# this part send the info for the user model
class UserForm(forms.ModelForm):

    # setting the password field in the form
    password = forms.CharField(widget=forms.PasswordInput())

    # Validation to check is entered email already exists
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("This email already exists")
       return self.cleaned_data

    # defining required fields
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = User
        fields = ('username', 'email','password',)

# form to update the user model info
# this part send the info for the user profile model
class UserProfileForm(forms.ModelForm):

    # defining the fields (check buttons) for the form
    isCooker = forms.BooleanField(initial=False, required=False, label='Are you a cooker?')
    isDinner = forms.BooleanField(initial=False, required=False, label='Are you a dinner?')

    # setting the field name as a requires field
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = UserProfile
        fields = ('name', 'isCooker', 'isDinner')

# form to update the user model info
class UserUpdateForm(forms.ModelForm):

    # hidding the password field
    password = None

    # setting the field name as a requires field
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = User
        exclude = ['username', 'password']
        fields = ('email',)

# form to update the user profile model info
class UserProfileUpdateForm(forms.ModelForm):

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = UserProfile
        fields = ('name', 'picture', 'address', 'city', 'specialty', 'phone', 'personalDescription', 'isCooker', 'isDinner',)

# form to create the requests meals
class RequestAMealForm(forms.ModelForm):

    # editing the type of field, and help text of the message
    message = forms.CharField(widget=forms.Textarea, help_text="Write any specifications and the number of orders you want")

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = Request
        fields = ('content', 'message',)

# form to register the allergies of the diners
class AllergiesForm(forms.ModelForm):

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = Allergy
        fields = ('name',)

# form to for the reviews of the users
class ReviewsForm(forms.ModelForm):

    # editing the fields rating and content
    rating = forms.IntegerField(required=True, help_text="Rate the cooker", label="Rating")
    content = forms.CharField(required=True, help_text="Rating description", label="Description")

    # defining the class is going to be used in the form and the values passed to the view
    class Meta:
        model = Review
        fields = ('title', 'rating','content',)

