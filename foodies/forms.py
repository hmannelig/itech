from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from betterforms.multiform import MultiModelForm
from foodies.models import Meal, Category, UserProfile, Ingredient
from django.contrib.auth.models import User


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
    title = forms.CharField(max_length=Meal.TITLE_MAX_LENGTH,
                            help_text="Please enter the title of the meal.")
    price = forms.FloatField(help_text="Please enter the price for this meal")
    url = forms.URLField(max_length=Meal.URL_MAX_LENGTH,
                         help_text="Please enter the URL of the meal page.")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Meal
        exclude = ('category',)
        fields = ('title', 'price', 'url',)

class IngredientsForm(forms.ModelForm):
    name = forms.CharField(required=True, help_text="Please enter one ingredient")
    vegetable = forms.CharField(required=False, help_text="Please enter the vegetables")
    typeofmeat = forms.CharField(required=False, help_text="Please enter the type of meat")
    meal = MealForm

    class Meta:
        model = Ingredient
        fields = ('name', 'vegetable', 'typeofmeat','meal')

# This form takes the IngredientsForm and the MealForm at the same time for being handled in views
class mealIngredientMultiForm(MultiModelForm):
    form_classes = {
        'meal': MealForm,
        'ingredients': IngredientsForm,
    }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

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
        fields = ('name',)