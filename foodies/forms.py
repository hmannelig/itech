from django import forms
from foodies.models import Meal, Category, UserProfile
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

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    isCooker = forms.BooleanField()
    isDinner = forms.BooleanField()

    class Meta:
        model = User
        fields = ('username', 'email',)

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)