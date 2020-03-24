import unittest
import os
import warnings
import importlib
import re
import inspect
import tempfile
import foodies.models

from foodies import forms
from django.test import TestCase
from foodies.models import Category, Meal, UserProfile, Ingredient
from django.urls import reverse, resolve
from django.conf import settings
from django.contrib.auth.models import User

from django.apps import apps
from foodies.apps import FoodiesConfig

from django.db import models
from django.forms import fields as django_fields


FAIL_HEADER = f"{os.linesep}{os.linesep}{os.linesep}==============={os.linesep}Foodies: Test failure message{os.linesep}==============={os.linesep}"
FAIL_FOOTER = f"{os.linesep}"

#Helper Method for test_index_view_with_categories   
def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category

#Helper Method
def create_user_object():
    user = User.objects.get_or_create(username='111', first_name='111', last_name='111', email='111@test.com')[0]
    user.set_password('111')
    user.save()
    return user

#Helper Method: Creates admin account
def super_user_object_creation():
    return User.objects.create_superuser('admin', 'admin@test.com', 'adminpw')

#Helper Method: Gives back string representation of template file.
def obtain_template_file(path_for_template):
    f = open(path_for_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str


#Check apps.py #works
class AppFoodiesConfigTest(TestCase):

    def test_config_apps_py_file(self):
        self.assertEqual(FoodiesConfig.name, 'foodies', f"{FAIL_HEADER}App config for foodies is not named correctly. Check apps.py.{FAIL_FOOTER}")
        self.assertEqual(apps.get_app_config('foodies').name, 'foodies', f"{FAIL_HEADER}App config for foodies is not named correctly. Check apps.py{FAIL_FOOTER}")    


#Check: Appropriate slug for, for example, meal category creation. #works
class SlugLineTest(TestCase):

    def test_slug_line_creation(self):
        category = Category(name='Food Category Random')
        category.save()
        self.assertEquals(category.slug, 'food-category-random', f"{FAIL_HEADER}Slug line creation for meal categories failed. Check Slug.{FAIL_FOOTER}")


class IndexViewTests(TestCase):

    def test_index_page_with_no_categories(self):
        #If no meal categories exist in view, display an error message.
        response = self.client.get(reverse('foodies:index'))

        self.assertQuerysetEqual(response.context['categories'], [])
        self.assertContains(response, 'There are no meal categories present.')
        self.assertEqual(response.status_code, 200)

    def test_index_page_with_categories(self):
        #Checks correct display of present categories. #works
        add_category('Vegetarian Meal Category', 200, 200)
        add_category('Seafood Meal Category', 100, 100)
        add_category('Vegan Meal Category', 21,21)

        response = self.client.get(reverse('foodies:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vegetarian Meal Category")
        self.assertContains(response, "Seafood Meal Category")
        self.assertContains(response, "Vegan Meal Category")

        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)

    def test_index_page_with_no_meals(self):
        #If no meals exists in view, an error message should be displayed. #works
        response = self.client.get(reverse('foodies:index'))

        self.assertQuerysetEqual(response.context['meals'], [])
        self.assertContains(response, 'There are no meals present.')
        self.assertEqual(response.status_code, 200)


# Tests derived from source: https://github.com/maxwelld90/tango_with_django_2_code/blob/master/progress_tests/tests_chapter4.py        
class DatabaseConfigTests(TestCase):

    def test_variable_for_databases_exists(self):
        #Checks, default config & setting for DATABASES     #works
        self.assertTrue(settings.DATABASES, f"{FAIL_HEADER} Settings module of Foodies does not contain DATABASES variables.{FAIL_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAIL_HEADER}'Default' database configuration is not existent in Foodies' DATABASES configuration variable.{FAIL_FOOTER}")


#Tests for User Authentication derived from source: https://github.com/maxwelld90/tango_with_django_2_code/blob/master/progress_tests/tests_chapter9.py
class SetupTest(TestCase):

    def test_auth_system_in_django(self):
        #Authentication system 'django.contrib.auth' check: In settings.py under installed apps is specified. #works
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS, f"{FAIL_HEADER}django.contrib.auth is not installed! Install it in settings.py for INSTALLED_APPS{FAIL_FOOTER}")


class ModelTests(TestCase):
    
    def test_userprofile(self):
        #Creation check: For UserProfile model in foodies.model;attributes for picture & user; value assertion for fields required   #works
        self.assertTrue('UserProfile' in dir(foodies.models))

        user_profile = foodies.models.UserProfile()
        #Expectation for attributes and types for example: Picture ans User
        expected_types = {
            'user': models.fields.related.OneToOneField,
            'picture': models.fields.files.ImageField,
        }

        expected_attributes = {
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'user': create_user_object(),
        }
        
        #Expectation check
        check_expectation_counter = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expctd_attr_name in expected_attributes.keys():
                if expctd_attr_name == attr_name:
                    check_expectation_counter = check_expectation_counter+1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAIL_HEADER}Attribute type for '{attr_name}' was '{type(attr)}'. However, it should be '{expected_types[attr_name]}'.{FAIL_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        
        self.assertEqual(check_expectation_counter, len(expected_attributes.keys()), f"{FAIL_HEADER}In UserProfile model, {check_expectation_counter} attributes were found. However, it should be {len(expected_attributes.keys())}.{FAIL_FOOTER}")
        user_profile.save()
    

class RegisterFormClassTests(TestCase):
    #Checks creation of UserForm and UserProfileForm  #works

    def test_userform(self):
        self.assertTrue('UserForm' in dir(forms), f"{FAIL_HEADER}No UserForm class in Foodies's forms.py module.{FAIL_FOOTER}")
        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, f"{FAIL_HEADER}UserForm does not match User model. In UserForm, check Meta definition.{FAIL_FOOTER}")

        fields = user_form.fields
        
        fields_expected = {
            'email': django_fields.EmailField,            
            'password': django_fields.CharField,
            'username': django_fields.CharField,
        }
        
        for expected_field_name in fields_expected:
            expected_field = fields_expected[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAIL_HEADER}The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification, and try again.{FAIL_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAIL_HEADER}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAIL_FOOTER}")
    

    def test_user_profile_form(self):
        #Checks UserProfileForm: Correct place + Correct fields specified #works
        self.assertTrue('UserProfileForm' in dir(forms), f"{FAIL_HEADER}Can't find UserProfileForm class in Foodies's forms.py module.{FAIL_FOOTER}")
        
        user_profile_form = forms.UserProfileForm()
        self.assertEqual(type(user_profile_form.__dict__['instance']), foodies.models.UserProfile, f"{FAIL_HEADER}UserProfileForm does not match up to the UserProfile model. Check Meta definition of UserProfileForm.{FAIL_FOOTER}")

        fields = user_profile_form.fields

        #Checks if UserProfilForm includes the checkbox isCooker & isDinner
        fields_expected = {
            'isCooker': django_fields.BooleanField,
            'isDinner': django_fields.BooleanField
        }

        for expected_field_name in fields_expected:
            expected_field = fields_expected[expected_field_name]
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAIL_HEADER}The field {expected_field_name} in UserProfileForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAIL_FOOTER}")
            self.assertTrue(expected_field_name in fields.keys(), f"{FAIL_HEADER}The field {expected_field_name} was not found in the UserProfile form.{FAIL_FOOTER}")


class RegistrationTests(TestCase):
    #Tests: Examine the registration of a user.  #works

    def test_registration_page(self):
        #Checks: Registration view with correct naming
        url = ''
        
        try:
            url = reverse('foodies:register')
        except:
            pass

        self.assertEqual(url, '/register/', f"{FAIL_HEADER}No correct mapping for foodies:register URL. It should point to register() view, and have a '/register/' URL.{FAIL_FOOTER}")
    
    def test_base_path_for_registration_link(self):
        #Checks, if  registration link has been added to footer.html and header.html template.    #works
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'foodies')
        base_path = os.path.join(template_base_path, 'footer.html')
        template_str = obtain_template_file(base_path)

        self.assertTrue('>Sign Up<' in template_str)

    def test_registration_template(self):
        #Checks: If register.html template exists in the correct place, and if it uses template inheritance     #works
        #Check register.html in foodies template & therefore, template heritance
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'foodies')
        template_path = os.path.join(template_base_path, 'register.html')

        self.assertTrue(os.path.exists(template_path), f"{FAIL_HEADER}No 'register.html' template in 'templates/foodies/' directory.{FAIL_FOOTER}")

        template_str = obtain_template_file(template_path)
        check_block_title = r'{% block title_block %}(\s*|\n*)Register(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('foodies:register'))
        content = request.content.decode('utf-8')
        self.assertTrue(re.search(check_block_title, template_str), f"{FAIL_HEADER}<title> block in html-file is not be correct: register.html may not use template inheritance. {FAIL_FOOTER}")
     
class LoginTests(TestCase):
    #Login tests for Foodies. #works
    def test_login_url(self):
        #Checks, if new login view exists in correct place, with correct name.
        url = ''

        try:
            url = reverse('foodies:login')
        except:
            pass
        
        self.assertEqual(url, '/login/', f"{FAIL_HEADER}Mapping of foodies:login URL not correct. It should point to the new login() view, and have a URL of '/foodies/login/'.{FAIL_FOOTER}")


    def test_login_functionality(self):
        #Tests the login functionality. A user should be able to log in, and should be redirected to the Foodies homepage.     #works
        user_object = create_user_object()
        response = self.client.post(reverse('foodies:login'), {'username': '111', 'password': '111'})
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAIL_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}.{FAIL_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAIL_HEADER}Login attempt with login() view failed: User not logged in.{FAIL_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAIL_HEADER}Testing login functionality: logging in was successful. However, a redirect was expected; Instead, received a status code of {response.status_code}.{FAIL_FOOTER}")
        self.assertEqual(response.url, reverse('foodies:index'), f"{FAIL_HEADER} No redirection to Foodies homepage after logging in.{FAIL_FOOTER}")

    def test_login_template(self):
        #Checks existence of login.html template in correct place and uses template inheritance        #works
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'foodies')
        template_path = os.path.join(template_base_path, 'login.html')

        self.assertTrue(os.path.exists(template_path), f"{FAIL_HEADER}No 'login.html' template in 'templates/foodies/' directory.{FAIL_FOOTER}")

        template_str = obtain_template_file(template_path)
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Login(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('foodies:login'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAIL_HEADER}Login.html does not use template inheritance?{FAIL_FOOTER}")
    
    def test_login_template_content(self):
        #Simple checks for the login.html template.        #works
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'foodies')
        template_path = os.path.join(template_base_path, 'login.html')

        self.assertTrue(os.path.exists(template_path), f"{FAIL_HEADER}No 'login.html' template in the 'templates/foodies/' directory.{FAIL_FOOTER}")
        
        template_str = obtain_template_file(template_path)
        self.assertTrue('action="{% url \'foodies:login\' %}"' in template_str, f"{FAIL_HEADER}No URL lookup for 'foodies:login' in your login.html <form>.{FAIL_FOOTER}")
        self.assertTrue('<input type="submit" value="submit" class="btn btn-success py-2">' in template_str, f"{FAIL_HEADER} 'Submit'-button not in login.html template.{FAIL_FOOTER}")
    
    def test_label_homepage(self):
        #Checks to see if the homepage greeting changes when a user logs in.     #no welcome message
        content = self.client.get(reverse('foodies:index')).content.decode()
        self.assertTrue('Homepage' in content, f"{FAIL_HEADER}We didn't see the generic greeting for a user not logged in on the Foodies homepage.{FAIL_FOOTER}")

        #not applicable
        # create_user_object()
        # self.client.login(username='testuser', password='testabc123')
        # content = self.client.get(reverse('foodies:index')).content.decode()
        # self.assertTrue('howdy testuser!' in content, f"{FAIL_HEADER}After user login, we didn't see the expected message welcoming them on the homepage. Check your index.html template.{FAIL_FOOTER}")


class LogoutTests(TestCase):
    #Check: Logout functionality #works
    
    def test_nonvalid_request(self):
        #Log out user who is not logged in & redirect user to login page.
        response = self.client.get(reverse('foodies:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('foodies:login'))
    
    def test_valid_request(self):
        #Log out user who is logged in: Check login success, whether they are logged in, logout success, whether they are logged out.
        user_object = create_user_object()
        self.client.login(username='111', password='111')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAIL_HEADER}Attempt to log in user ID {user_object.id}. However, user with ID {self.client.session['_auth_user_id']} was logged. Please check login() view.{FAIL_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAIL_HEADER}Failure to login as user.{FAIL_FOOTER}")
        
        # User logout & redirection to index
        response = self.client.get(reverse('foodies:logout'))
        self.assertEqual(response.status_code, 302, f"{FAIL_HEADER}Failure to redirect logged out user. {FAIL_FOOTER}")
        self.assertEqual(response.url, reverse('foodies:index'), f"{FAIL_HEADER}Failure to redirect logged out user to index view (homepage).{FAIL_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAIL_HEADER}Failure of logout!{FAIL_FOOTER}")


class LinkTidyingTests(TestCase):
    #Check links that should be globally existent (independant from user state).    #works
    def test_global_links(self):
        content = self.client.get(reverse('foodies:index')).content.decode()
        self.assertTrue('href="/about/"' in content)
        self.assertTrue('href="/"' in content)

        user_object = create_user_object()
        self.client.login(username='111', password='111')

        #Update of links correct?
        content = self.client.get(reverse('foodies:index')).content.decode()
        self.assertTrue('href="/about/"' in content, f"{FAIL_HEADER}Check links in base.html have been updated correctly to change when users log in and out.{FAIL_FOOTER}")
        self.assertTrue('href="/"' in content, f"{FAIL_HEADER}Check links in base.html have been updated correctly to change when users log in and out.{FAIL_FOOTER}")


if __name__ == '__main__':
    unittest.main()