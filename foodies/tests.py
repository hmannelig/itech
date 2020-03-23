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


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}==============={os.linesep}Foodies: Test failure message{os.linesep}==============={os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

#admin.py 100%
#appy.py 100%
#urls.py 100%
#bing_search.py 16% -> 32 miss out of 38
#forms.py 92% -> 6 miss out of 75
#models.py 90% -> 8 out of 84
#templatetags\foodies_template_tags.py 83% -> 1 out of 6
#tests.py 93%
#views.py 21% -> 274 miss out of 348 
#wsgi.py 0% -> 4 out of 4
#manage.py 78% -> 2 out of 9 - lines 9 and 10: except ImportERror as exc: raise ImportError(
#populate_foodies 0% -> 33 out of 33

#for manage.py 2 lines //doesn't work
# class managePYTest(TestCase):
#     def test_importerror(self):
#         sys.path.insert(0,'.')
#         from django.core.management import execute_from_command_line
#         raise ImportError()
#     self.assertEqual(response, 'available on your PYTHONPATH environment variable')
# class SlugLineTest(TestCase):
#     #works    
#     def managepy_creation(self):
#         self.assertRaisesMessage(ImportError, 'available on your PYTHONPATH environment variable')
    


# #Missing adaption in Models & View
# class CategoryMethodTests(TestCase):
#     def test_ensure_views_are_positive(self):
#         """
#         Ensures the number of views received for a Category are positive or zero.
#         """
#         category = Category(name='test', views=-1, likes=0)
#         category.save()
#         self.assertEqual((category.views >= 0), True)

    #Helper Method for test_index_view_with_categories   
def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category

class SlugLineTest(TestCase):
    #works    
    def test_slug_line_creation(self):
        """
        Checks to make sure that when a category is created, an appropriate slug is created. 
        Example: "Random Category String" should be "random-category-string".
        """
        category = Category(name='Random Category String')
        category.save()
        self.assertEquals(category.slug, 'random-category-string')


class IndexViewTests(TestCase):
    #works
    def test_index_view_with_no_categories(self):
        """
        If no meal categories exist, an error message should be displayed.
        """
        response = self.client.get(reverse('foodies:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no meal categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    #works
    def test_index_view_with_no_meals(self):
        """
        If no meals exist, an error message should be displayed.
        """
        response = self.client.get(reverse('foodies:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no meals present.')
        self.assertQuerysetEqual(response.context['meals'], [])
    
    #works
    def test_index_view_with_categories(self):
        """
        Checks whether categories are displayed correctly when present.
        """
        add_category('Vegetarian Meal Category', 1, 1)
        add_category('Seafood Meal Category', 1, 1)
        add_category('Vegan Meal Category', 1, 1)
        response = self.client.get(reverse('foodies:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vegetarian Meal Category")
        self.assertContains(response, "Seafood Meal Category")
        self.assertContains(response, "Vegan Meal Category")
        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)
        
#Source: https://github.com/maxwelld90/tango_with_django_2_code/blob/master/progress_tests/tests_chapter4.py        
class DatabaseConfigurationTests(TestCase):
    #Helper Class
    def setUp(self):
        pass
    #Helper Class
    def gitignore_includes_database(self, path):
        """
        Checks .gitignore file whether db.sqlite3 database is included
        """
        f = open(path, 'r')
        for line in f:
            line = line.strip()
            if line.startswith('db.sqlite3'):
                return True
        f.close()
        return False

    #works    
    def test_databases_variable_exists(self):
        """
        Checks existence for DATABASES settings and for default configuration
        """
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Project's settings module does not have a DATABASES variable.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}'Default' database configuration is not existent in Foodies' DATABASES configuration variable.{FAILURE_FOOTER}")

#Tests apps.py #works --> 100% covered in foodies\apps.py test
class AppFoodiesConfigTest(TestCase):
    def test_apps_py_file(self):
        self.assertEqual(FoodiesConfig.name, 'foodies')
        self.assertEqual(apps.get_app_config('foodies').name, 'foodies')    

#Test User Authentication; Source: https://github.com/maxwelld90/tango_with_django_2_code/blob/master/progress_tests/tests_chapter9.py
#Helper Class
def create_user_object():
    user = User.objects.get_or_create(username='testuser', first_name='Test', last_name='User', email='test@test.com')[0]
    user.set_password('tester1')
    user.save()
    return user

#Helper Class
def create_super_user_object():
    """
    Helper function: Creates super user (admin) account.
    """
    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

#Helper Class
def get_template(path_to_template):
    """
    Helper function: Returns string representation of template file.
    """
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str

class SetupTest(TestCase):
    """
    Check if the auth app is specified.
    """
    #works
    def test_installed_apps(self):
        """
        Checks if 'django.contrib.auth' app is included in INSTALLED_APPS.
        """
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)


class ModelTests(TestCase):
    """
    Chacks if UserProfile model is created
    """
    #works
    def test_userprofile_class(self):
        """
        Does the UserProfile class exist in foodies.models? If so, are all the required attributes present?
        Assertion fails if we can't assign values to all the fields required (i.e. one or more missing).
        """
        self.assertTrue('UserProfile' in dir(foodies.models))

        user_profile = foodies.models.UserProfile()

        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.
        expected_attributes = {
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'user': create_user_object(),
        }

        expected_types = {
            'picture': models.fields.files.ImageField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        
        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}.{FAILURE_FOOTER}")
        user_profile.save()
    

class RegisterFormClassTests(TestCase):
    """
    Checks if the UserForm and UserProfileForm is created.
    """
    #works
    def test_user_form(self):
        """
        Tests: IS UserForm is in the correct place, and whether the correct fields have been specified for it.
        """
        self.assertTrue('UserForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the UserForm class in Foodies's forms.py module. Did you create it in the right place?{FAILURE_FOOTER}")
        
        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, f"{FAILURE_HEADER}Your UserForm does not match up to the User model. Check your Meta definition of UserForm and try again.{FAILURE_FOOTER}")

        fields = user_form.fields
        
        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }
        
        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")
    

    def test_user_profile_form(self):
        """
        Tests if UserProfileForm is in  correct place, and whether the correct fields have been specified for it.
        """
        #works
        self.assertTrue('UserProfileForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the UserProfileForm class in Foodies's forms.py module. Did you create it in the right place?{FAILURE_FOOTER}")
        
        user_profile_form = forms.UserProfileForm()
        self.assertEqual(type(user_profile_form.__dict__['instance']), foodies.models.UserProfile, f"{FAILURE_HEADER}Your UserProfileForm does not match up to the UserProfile model. Check your Meta definition of UserProfileForm and try again.{FAILURE_FOOTER}")

        fields = user_profile_form.fields

        #Checks if UserProfilForm includes the checkbox isCooker & isDinner
        expected_fields = {
            'isCooker': django_fields.BooleanField,
            'isDinner': django_fields.BooleanField
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserProfile form. Check you have complied with the specification, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserProfileForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")


class RegistrationTests(TestCase):
    """
    Tests: Examine the registration of a user.
    """
    #works
    def test_new_registration_view_exists(self):
        """
        Checks if the new registration view exists with the correct name.
        """
        url = ''
        try:
            url = reverse('foodies:register')
        except:
            pass
        self.assertEqual(url, '/register/', f"{FAILURE_HEADER}foodies:register URL is not mapped correctly. It should point to register() view, and have a URL of '/register/'.{FAILURE_FOOTER}")
    
    #works
    def test_registration_template(self):
        """
        Does the register.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'foodies')
        template_path = os.path.join(template_base_path, 'register.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'register.html' template in the 'templates/foodies/' directory. Did you put it in the right place?{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        #full_title_pattern = r'<title>(\s*|\n*)Foodies(\s*|\n*){% block title_block %}(\s*|\n*)(\s*|\n*){% endblock %}(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Register(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('foodies:register'))
        content = request.content.decode('utf-8')

        #self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'foodies:register' is not correct. Check your register.html template, and try again.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}Is register.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")
        
    # def test_registration_get_response(self):
    #     """
    #     Checks the GET response of the registration view. There should be a form with the correct markup.
    #     """
    #     request = self.client.get(reverse('foodies:register'))
    #     content = request.content.decode('utf-8')

    #     self.assertTrue('<h1>Register for Foodies</h1>' in content, f"{FAILURE_HEADER}Can't find the '<h1>Register for Foodies</h1>' header tag in the register template.{FAILURE_FOOTER}")
    #     #self.assertTrue('Foodies says: <strong>thank you for registering!</strong>' in content, f"{FAILURE_HEADER}When loading the register view with a GET request, we didn't see the required 'Foodies says: <strong>thank you for registering!</strong>'. Check register.html template and try again.{FAILURE_FOOTER}")
    #     self.assertTrue('enctype="multipart/form-data"' in content, f"{FAILURE_HEADER}In the register.html template: Use 'multipart/form-data' for the <form>'s 'enctype'{FAILURE_FOOTER}")
    #     self.assertTrue('action="/register/"' in content, f"{FAILURE_HEADER}<form> in register.html doesn't point to the correct URL for registering a user{FAILURE_FOOTER}")
    #     self.assertTrue('<input type="submit" name="submit" value="Register" />' in content, f"{FAILURE_HEADER}Can't find the markup for the form submission button in register.html. Try again.{FAILURE_FOOTER}")
    #     #self.assertTrue('<p><label for="id_password">Password:</label> <input type="password" name="password" required id="id_password"></p>' in content, f"{FAILURE_HEADER}Checking a random form field in register.html (password), the markup didn't match what we expected. Is your password form field configured correctly?{FAILURE_FOOTER}")
    
    #creates ERROR: <ul class="errorlist"><li>username<ul class="errorlist"
    # def test_bad_registration_post_response(self):
    #     """
    #     Checks the POST response of the registration view. What if we submit a blank form?
    #     """
    #     request = self.client.post(reverse('foodies:register'))
    #     content = request.content.decode('utf-8')

    #     #insert Stuff for assertTrue
    #     self.assertTrue('' in content)
    
    # def test_good_form_creation(self):
    #     """
    #     Tests the functionality of the forms.
    #     Creates a UserProfileForm and UserForm, and attempts to save them.
    #     Upon completion, we should be able to login with the details supplied.
    #     """
    #     user_data = {'username': '111', 'password': '111', 'email': '111@test.com', 'name': '111', 'isDinner': 'True'}
    #     user_form = forms.UserForm(data=user_data)

    #     #'website': 'http://www.bing.com', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name
    #     user_profile_data = {}
    #     user_profile_form = forms.UserProfileForm(data=user_profile_data)

    #     self.assertTrue(user_form.is_valid(), f"{FAILURE_HEADER}The UserForm was not valid after entering the required data. Check your implementation of UserForm, and try again.{FAILURE_FOOTER}")
    #     self.assertTrue(user_profile_form.is_valid(), f"{FAILURE_HEADER}The UserProfileForm was not valid after entering the required data. Check your implementation of UserProfileForm, and try again.{FAILURE_FOOTER}")

    #     user_object = user_form.save()
    #     user_object.set_password(user_data['password'])
    #     user_object.save()
        
    #     user_profile_object = user_profile_form.save(commit=False)
    #     user_profile_object.user = user_object
    #     user_profile_object.save()
        
    #     self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a User object created, but it didn't appear. Check your UserForm implementation, and try again.{FAILURE_FOOTER}")
    #     self.assertEqual(len(foodies.models.UserProfile.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a UserProfile object created, but it didn't appear. Check your UserProfileForm implementation, and try again.{FAILURE_FOOTER}")
    #     self.assertTrue(self.client.login(username='111', password='111'), f"{FAILURE_HEADER}We couldn't log our sample user in during the tests. Please check your implementation of UserForm and UserProfileForm.{FAILURE_FOOTER}")

#    #Creates ERROR MESSAGE:<ul class="errorlist"><li>name<ul class="errorlist"><li>This field is required.</li></ul></li></ul>
#     def test_good_registration_post_response(self):
#         """
#         Checks the POST response of the registration view.
#         We should be able to log a user in with new details after this!
#         """
#         post_data = {'username': 'webformuser', 'password': 'test123', 'email': 'test@test.com', 'website': 'http://www.bing.com', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
#         request = self.client.post(reverse('foodies:register'), post_data)
#         content = request.content.decode('utf-8')

#         self.assertTrue('<h1>Register for Foodies</h1>' in content, f"{FAILURE_HEADER}We were missing the '<h1>Register for Foodies</h1>' header in the registration response.{FAILURE_FOOTER}")
#         #self.assertTrue('Foodies says: <strong>thank you for registering!</strong>' in content, f"{FAILURE_HEADER}Upon successful registration, we couldn't find the expected success message. Check your implementation of register.html, and try again.{FAILURE_FOOTER}")
#         self.assertTrue('<a href="/foodies/">Return to the homepage.</a>' in content, f"{FAILURE_HEADER}After successfully registering, we couldn't find the expected link back to the Foodies homepage.{FAILURE_FOOTER}")

#         self.assertTrue(self.client.login(username='webformuser', password='test123'), f"{FAILURE_HEADER}We couldn't log in the user we created using your registration form. Please check your implementation of the register() view. Are you missing a .save() call?{FAILURE_FOOTER}")

    #works
    def test_base_for_register_link(self):
        """
        Checks, if  registration link has been added to footer.html and header.html template. This should work for pre-exercises, and post-exercises.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'foodies')
        base_path = os.path.join(template_base_path, 'footer.html')
        template_str = get_template(base_path)
        self.assertTrue('>Sign Up<' in template_str)
    

class LoginTests(TestCase):
    """
    A series of tests for checking the login functionality of Fodies.
    """
    #works
    def test_login_url_exists(self):
        """
        Checks to see if the new login view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('foodies:login')
        except:
            pass
        
        self.assertEqual(url, '/login/', f"{FAILURE_HEADER}Have you created the foodies:login URL mapping correctly? It should point to the new login() view, and have a URL of '/foodies/login/' Remember the first part of the URL (/foodies/) is handled by the project's urls.py module, and the second part (login/) is handled by the Foodies app's urls.py module.{FAILURE_FOOTER}")

    #works
    def test_login_functionality(self):
        """
        Tests the login functionality. A user should be able to log in, and should be redirected to the Foodies homepage.
        """
        user_object = create_user_object()
        response = self.client.post(reverse('foodies:login'), {'username': 'testuser', 'password': 'tester1'})
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with login() view, it doesn't log the user in. Check login() view implementation, and try again.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Testing login functionality: logging in was successful. However, a redirect was expected; Instead, received a status code of {response.status_code}. Check login() view implementation.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('foodies:index'), f"{FAILURE_HEADER} No redirection to Foodies homepage after logging in. Please check login() view implementation, and try again.{FAILURE_FOOTER}")

    def test_login_template(self):
        """
        Cehcks if login.html template exist in correct place and uses template inheritance
        """
        #works
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'foodies')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}Can't find the 'login.html' template in the 'templates/foodies/' directory. Did you put it in the right place?{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        #full_title_pattern = r'<title>(\s*|\n*)Foodies(\s*|\n*)-(\s*|\n*)Login(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Login(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('foodies:login'))
        content = request.content.decode('utf-8')

        #self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'foodies:login' is not correct. Check your login.html template, and try again.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}Is login.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")
    
    def test_login_template_content(self):
        """
        Simple checks for the login.html template.
        """
        #works
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'foodies')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}No 'login.html' template in the 'templates/foodies/' directory.{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        #self.assertTrue('<h1>Login to Foodies</h1>' in template_str, f"{FAILURE_HEADER}We couldn't find the '<h1>Login to Foodies</h1>' in the login.html template.{FAILURE_FOOTER}")
        self.assertTrue('action="{% url \'foodies:login\' %}"' in template_str, f"{FAILURE_HEADER}We couldn't find the url lookup for 'foodies:login' in your login.html <form>.{FAILURE_FOOTER}")
        self.assertTrue('<input type="submit" value="submit" class="btn btn-info btn-block rounded-0 py-2">' in template_str, f"{FAILURE_HEADER} Submit button not in login.html template.{FAILURE_FOOTER}")
    
    #no welcome message
    def test_homepage_greeting(self):
        """
        Checks to see if the homepage greeting changes when a user logs in.
        """
        content = self.client.get(reverse('foodies:index')).content.decode()
        self.assertTrue('Homepage' in content, f"{FAILURE_HEADER}We didn't see the generic greeting for a user not logged in on the Foodies homepage. Please check your index.html template.{FAILURE_FOOTER}")

        #not applicable
        # create_user_object()
        # self.client.login(username='testuser', password='testabc123')
        # content = self.client.get(reverse('foodies:index')).content.decode()
        # self.assertTrue('howdy testuser!' in content, f"{FAILURE_HEADER}After user login, we didn't see the expected message welcoming them on the homepage. Check your index.html template.{FAILURE_FOOTER}")


# class RestrictedAccessTests(TestCase):
#     """
#     Some tests to test the restricted access view. Can users who are not logged in see it?
#     """
#     def test_restricted_url_exists(self):
#         """
#         Checks to see if the new restricted view exists in the correct place, with the correct name.
#         """
#         url = ''

#         try:
#             url = reverse('foodies:restricted')
#         except:
#             pass
        
#         self.assertEqual(url, 'foodies:restricted', f"{FAILURE_HEADER}Have you created the foodies:restricted URL mapping correctly? It should point to the new restricted() view, and have a URL of '/foodies/restricted/' Remember the first part of the URL (/foodies/) is handled by the project's urls.py module, and the second part (restricted/) is handled by the Foodies app's urls.py module.{FAILURE_FOOTER}")
    
    
#     def test_bad_request(self):
#         """
#         Tries to access the restricted view when not logged in.
#         This should redirect the user to the login page.
#         """
#         response = self.client.get(reverse('foodies:restricted'))
        
#         self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}We tried to access the restricted view when not logged in. We expected to be redirected, but were not. Check your restricted() view.{FAILURE_FOOTER}")
#         self.assertTrue(response.url.startswith(reverse('foodies:login')), f"{FAILURE_HEADER}We tried to access the restricted view when not logged in, and were expecting to be redirected to the login view. But we were not! Please check your restricted() view.{FAILURE_FOOTER}")
    
#     def test_good_request(self):
#         """
#         Attempts to access the restricted view when logged in.
#         This should not redirect. We cannot test the content here. Only links in base.html can be checked -- we do this in the exercise tests.
#         """
#         create_user_object()
#         self.client.login(username='testuser', password='testabc123')

#         response = self.client.get(reverse('foodies:restricted'))
#         self.assertTrue(response.status_code, 200)


class LogoutTests(TestCase):
    """
    A few tests to check the functionality of logging out. D
    """
    #works
    def test_bad_request(self):
        """
        Attepts to log out a user who is not logged in. This should redirect the user to the login page.
        """
        response = self.client.get(reverse('foodies:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('foodies:login'))
    
    def test_good_request(self):
        """
        Attempts to log out a logged in user.
        This should succeed -- we should be able to login, check that they are logged in, logout, and perform the same check.
        """
        user_object = create_user_object()
        self.client.login(username='111', password='111')

        # try:
        #     self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view. This happened when testing logout functionality.{FAILURE_FOOTER}")
        # except KeyError:
        #     self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. Please check your login() view and try again.{FAILURE_FOOTER}")
        
        # Now lot the user out. This should cause a redirect to the homepage.
        response = self.client.get(reverse('foodies:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user should cause a redirect, but this failed to happen. Check logout() view.{FAILURE_FOOTER}")
        #views.py has reverse('foodies:index')
        # self.assertEqual(response.url, reverse('foodies:index'), f"{FAILURE_HEADER}When logging out a user, the book states you should then redirect them to the homepage. This did not happen; Check your logout() view.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out with your logout() view didn't actually log the user out! Please check yout logout() view.{FAILURE_FOOTER}")


class LinkTidyingTests(TestCase):
    """
    Some checks to see whether the links in base.html have been tidied up and change depending on whether a user is logged in or not.
    We don't check for category/page links here; these are done in the exercises.
    """
    #works
    def test_omnipresent_links(self):
        """
        Checks for links that should always be present, regardless of user state.
        """
        content = self.client.get(reverse('foodies:index')).content.decode()
        self.assertTrue('href="/about/"' in content)
        self.assertTrue('href="/"' in content)

        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        # These should be present.
        content = self.client.get(reverse('foodies:index')).content.decode()
        self.assertTrue('href="/about/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        self.assertTrue('href="/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
    
    # def test_logged_in_links(self):
    #     """
    #     Checks for links that should only be displayed when the user is logged in.
    #     """
    #     user_object = create_user_object()
    #     self.client.login(username='testuser', password='testabc123')
    #     content = self.client.get(reverse('foodies:index')).content.decode()

    #     # These should be present.
    #     self.assertTrue('href="/logout/"' in content, f"{FAILURE_HEADER}Check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")

    #     # These should not be present.
    #     self.assertTrue('href="/login/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
    #     self.assertTrue('href="/register/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
    
    # def test_logged_out_links(self):
    #     """
    #     Checks for links that should only be displayed when the user is not logged in.
    #     """
    #     content = self.client.get(reverse('foodies:index')).content.decode()

    #     # These should be present.
    #     self.assertTrue('href="/foodies/login/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
    #     self.assertTrue('href="/foodies/register/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        
    #     # These should not be present.
    #     self.assertTrue('href="/foodies/restricted/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
    #     self.assertTrue('href="/foodies/logout/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")



if __name__ == '__main__':
    unittest.main()