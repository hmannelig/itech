from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from betterforms.multiform import MultiModelForm
from foodies.models import Meal, Category, UserProfile, Ingredient, Request, Allergy, Review
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
    # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class MealForm(forms.ModelForm):
    title = forms.CharField(max_length=Meal.TITLE_MAX_LENGTH, help_text="Please enter the title of the meal.", label="Meal Name")
    price = forms.FloatField(help_text="Please enter the price for this meal")
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), help_text="Please select the category for this meal")

    class Meta:
        model = Meal
        fields = ('title', 'picture', 'price', 'category', 'ingredients', 'recipe')

class IngredientsForm(forms.ModelForm):
    name = forms.CharField(required=True, help_text="Please enter one ingredient", label="Ingredient Name")
    vegetable = forms.CharField(required=False, help_text="Please enter the vegetables")
    typeofmeat = forms.CharField(required=False, help_text="Please enter the type of meat", label="Type of Meat")
    meal = MealForm

    class Meta:
        model = Ingredient
        fields = ('name', 'vegetable', 'typeofmeat',)

# This form takes the IngredientsForm and the MealForm at the same time for being handled in views
class mealIngredientMultiForm(MultiModelForm):
    form_classes = {
        'meal': MealForm,
        'ingredients': IngredientsForm,
    }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("This email already exists")
       return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'email','password',)

class UserProfileForm(forms.ModelForm):
    isCooker = forms.BooleanField(initial=False, required=False, label='Are you a cooker?')
    isDinner = forms.BooleanField(initial=False, required=False, label='Are you a dinner?')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    class Meta:
        model = UserProfile
        fields = ('name', 'isCooker', 'isDinner')

class UserUpdateForm(forms.ModelForm):
    password = None

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        exclude = ['username', 'password']
        fields = ('email',)


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'picture', 'address', 'city', 'specialty', 'phone', 'personalDescription', 'isCooker', 'isDinner',)

class RequestAMealForm(forms.ModelForm):

    message = forms.CharField(widget=forms.Textarea, help_text="Write any specifications and the number of orders you want")

    class Meta:
        model = Request
        fields = ('content', 'message',)

class AllergiesForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ('name',)


class ReviewsForm(forms.ModelForm):
    rating = forms.IntegerField(required=True, help_text="Rate the cooker", label="Rating")
    content = forms.CharField(required=True, help_text="Rating description", label="Description")

    class Meta:
        model = Review
        fields = ('title', 'rating','content',)

