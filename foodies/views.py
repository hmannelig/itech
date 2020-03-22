from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from foodies.models import Category, Meal, User, UserProfile, Request
from foodies.forms import CategoryForm, MealForm, UserForm, UserProfileForm, mealIngredientMultiForm, UserUpdateForm, UserProfileUpdateForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib import messages
from foodies.bing_search import run_query


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    meal_list = Meal.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['meals'] = meal_list
    visitor_cookie_handler(request)
    return render(request, 'foodies/index.html', context=context_dict)


def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'foodies/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        meals = Meal.objects.filter(category=category)

        context_dict['meals'] = meals

        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['meals'] = None

    return render(request, 'foodies/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return redirect('/foodies/')
        else:
            print(form.errors)

    return render(request, 'foodies/add_category.html', {'form': form})


@login_required
def add_meal(request):
    form = mealIngredientMultiForm

    if request.method == 'POST':
        ingredientsMeal = mealIngredientMultiForm(request.POST)

        if ingredientsMeal.is_valid():

            ingredient = ingredientsMeal['ingredients'].save(commit=False)
            meal = ingredientsMeal['meal'].save(commit=False)

            ingredient.save()
            meal.save()

            cleaned_data = ingredientsMeal['meal'].cleaned_data
            cleaned_data = cleaned_data['category'].name.lower()
            category = '/foodies/category/' + cleaned_data + '/'

            return HttpResponseRedirect(category)
        else:
            return redirect('/foodies/')
    else:
        print(form.errors)

    return render(request, 'foodies/add_meal.html', {'form': form})


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            data = request.POST.copy()
            if data.get('isCooker') == None and data.get('isDinner') == None:
                messages.error(request, 'Invalid: Check at least 1 checkbox for Cooker or Dinner or both.')
                return HttpResponseRedirect('/foodies/register')

            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.name = data.get('name')

            if data.get('isCooker') is not None:
                profile.isCooker = True

            if data.get('isDiner') is not None:
                profile.isDinner = True

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
            login(request, user)
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'foodies/register.html',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('foodies:index'))
            else:
                return HttpResponse("Your Foodies account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            messages.error(request, 'Invalid login details.')
            return redirect(reverse('foodies:login'))

    else:
        return render(request, 'foodies/login.html')


@login_required
def restricted(request):
    return render(request, 'foodies/restricted.html')


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('foodies:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


@login_required
def user_profile(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    profile_title = "User Profile"

    userProfile = UserProfile.objects.filter(user=user)[0]
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'picture': userProfile.picture,
        'name': userProfile.name,
        'address': userProfile.address,
        'personalDescription': userProfile.personalDescription,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner,
        'isBestCooker': userProfile.isBestCooker,
    }

    user_requests = Request(cooker=userProfile.id)

    return render(request, 'foodies/user_profile.html', context={'profile_title': profile_title,
                                                                 'user_info': user_info,
                                                                 'user_meals': user_meals,
                                                                 'user_requests': user_requests, })

@login_required
def user_profile_update(request):

    profile_title = "Update User Profile"

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST)
        profile_form = UserProfileUpdateForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            data = request.POST.copy()
            if data.get('isCooker') == None and data.get('isDinner') == None:
                messages.error(request, 'Invalid: Check at least 1 checkbox for Cooker or Dinner or both.')
                return HttpResponseRedirect('/foodies/register')

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.name = data.get('name')

            if data.get('isCooker') is not None:
                profile.isCooker = True

            if data.get('isDiner') is not None:
                profile.isDinner = True

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            login(request, user)
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserUpdateForm()
        profile_form = UserUpdateForm()

    return render(request, 'foodies/user_profile_update.html',
                            context={
                                        'user_info': request.user,
                                        'profile_title': profile_title,
                                        'user_form': user_form, 
                                        'profile_form': profile_form
                                    })
    

@login_required
def user_meals(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    user_profile = UserProfile.objects.filter(user=user)[0]
    user_meals = Meal.objects.filter(user=user_profile)

    meals_array=[]

    for e in user_meals:
        meals_array[e] = meals_info = {
                    'title': e.title,
                    'url': e.url,
                    'price': e.price,
                    'views': e.views,
                    'category': e.category,
                }

    profile_title = "User Meals"

    return render(request, 'foodies/user_meals.html', context={'profile_title': profile_title,
                                                               'meals_info': meals_array})


@login_required
def user_requests(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    user_profile = UserProfile.objects.filter(user=user)[0]
    user_requests = Request.objects.filter(id=user_profile.id)

    requests_array = []

    for e in user_requests:
        requests_array[e] = request_info = {
            'title': e.title,
            'date': e.url,
            'name': e.price,
            'email': e.views,
            'content': e.category,
            'message': e.category,
            'dinner': e.category,
            'cooker': e.category,
        }

    profile_title = "User Requests"

    return render(request, 'foodies/user_requests.html', context={'profile_title': profile_title, 'requests_array': requests_array})

def reviews(request):
    return render(request, 'foodies/reviews.html')


def register_diners(request):
    return render(request, 'foodies/register_diners.html')


def register_cookers(request):
    return render(request, 'foodies/register_cookers.html')


def search(request):
    return HttpResponse("This is search")


def search_cookers(request):
    return HttpResponse("This is search cooker")


def contact_us(request):
    return render(request, 'foodies/contact_us.html')


def request(request):
    return render(request, 'foodies/request.html')

def search(request):
    result_list = []
    query = ''

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)
    
    return render(request, 'foodies/search.html', {'result_list': result_list, 'query': query})

