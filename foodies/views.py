from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from foodies.models import Category, Meal, User, UserProfile, Request, Ingredient, Allergy, Review
from django.urls import reverse
from foodies.forms import CategoryForm, MealForm, UserForm, UserProfileForm, IngredientsForm, UserUpdateForm, UserProfileUpdateForm, RequestAMealForm, AllergiesForm, ReviewsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib import messages
from foodies.bing_search import run_query
from django.db.models import Q

# function to show the index view
def index(request):

    # requiresting the 6 first user profiles 
    user_list=UserProfile.objects.order_by('-id')[:6]
    # requiresting the 6 most liked categories
    category_list = Category.objects.order_by('-likes')[:6]
    # requiresting the 3 most liked categories
    categories_for_meals = Category.objects.order_by('-likes')[:3]
    
    # requesting the first thre categories and the 6 first meals store for each
    meal_by_category = [
        {
            'name' : categories_for_meals[0].name,
            'meals'    : Meal.objects.filter(category=categories_for_meals[0])[:6]
        },
        {
            'name' : categories_for_meals[1].name,
            'meals'    : Meal.objects.filter(category=categories_for_meals[1])[:6]
        },
        {
            'name' : categories_for_meals[2].name,
            'meals'    : Meal.objects.filter(category=categories_for_meals[2])[:6]
        },
    ]

    # requesting the 6 most viewd meals
    meal_list = Meal.objects.order_by('-views')[:6]

    # passing all the parameters to the context
    context_dict = {        
        'categories'        : category_list,
        'meals'             : meal_list,  
        'user_info'         : user_list,
        'meal_by_category'  : meal_by_category
    }
    return render(request, 'foodies/index.html', context=context_dict)


# about page
def about(request):
    context_dict = {}
    return render(request, 'foodies/about.html', context=context_dict)

# Category page
def show_category(request, category_name_slug):
    context_dict = {}

    # try to get the meals for the selected category
    try:
        category = Category.objects.get(slug=category_name_slug)
        category.views = int(category.views) + 1
        category.save()

        meals = Meal.objects.filter(category=category)

        context_dict['meals'] = meals

        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['meals'] = None

    return render(request, 'foodies/category.html', context=context_dict)

# add category form
@login_required
def add_category(request):
    # Obtaining the form to reigster a category
    form = CategoryForm()

    # Detecting if POST request
    if request.method == 'POST':
        # Obtaining the form and saving the info
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return redirect('foodies/index')
        else:
            print(form.errors)

    return render(request, 'foodies/add_category.html', {'form': form})

# add meal form
@login_required
def add_meal(request):
    # page title
    profile_title = "Add a Meal"

    # Trying to obtain the user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Trying to obtain the user profile info
    userProfile = UserProfile.objects.filter(user=user).first()
    
    # Storing the info of the user
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    # Checking if the user is a diner to prevent him to see the page
    if user_info.get('isCooker') is False:
        return HttpResponseRedirect(reverse('foodies:user_profile'))

    # Detectint if POST request to save the form info
    if request.method == 'POST':

        # Obtaining the form meal info
        meal_form = MealForm(request.POST, request.FILES)

        # check if the form is valid
        if meal_form.is_valid():

            # Preventing the form from save
            meal = meal_form.save(commit=False)
            # Adding the user profile to the form
            user_profile = UserProfile.objects.filter(user=request.user).first()
            meal.user = user_profile

            # Adding the picture of the user to the form
            if 'picture' in request.FILES:
                meal.picture = request.FILES['picture']

            # saving the form
            meal.save()

            return redirect('foodies:user_meals')
        else:
            # Returning errores if the form is not valid
            messages.error(request, meal_form.errors)
            return HttpResponseRedirect(reverse('foodies:add_meal'))
    else:
        # Obtaining the form is not POST request
        meal_form = MealForm()

    return render(request, 'foodies/add_meal.html',
                  {'meal_form': meal_form, 'profile_title': profile_title, 'user_info': user_info})

# form edit meal view
@login_required
def edit_meal(request, meal_id):

    # title of the view
    profile_title = "Update Meal"

    # Obtaining the user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Obtaining the user profile info
    userProfile = UserProfile.objects.filter(user=user).first()
    # Storing the info of the user
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    # Checking if the user is a diner to prevent him to see the page
    if user_info.get('isCooker') is False:
        return HttpResponseRedirect(reverse('foodies:user_profile'))

    # obtainig the info of the meals that is going to be updated
    try:
        meal = Meal.objects.get(id=meal_id)
    except User.DoesNotExist:
        messages.error(request, 'The meal does not exists')
        return HttpResponseRedirect(reverse('foodies:edit_meal', kwargs={'meal_id': meal_id}))

    # Obtaining the meal form and passing the instance of the meal so it will be filled
    meal_form = MealForm(request.POST or None, instance=meal)

    # checking if POST request
    if request.method == 'POST':
        # Checking of the form is valid
        if meal_form.is_valid():

            # Saving the info of the meal along with the picture info
            meal_form.save()
            meal = meal_form.save(commit=False)

            if 'picture' in request.FILES:
                meal.picture = request.FILES['picture']

            meal.save()
            return HttpResponseRedirect(reverse('foodies:user_meals'))

        else:
            # return error emssages is the form is not valid
            messages.error(request, meal_form.errors)
            return HttpResponseRedirect(reverse('foodies:edit_meal', kwargs={'meal_id': meal_id}))

    return render(request, 'foodies/edit_meal.html',
                  {'meal_form': meal_form, 'meal_id': meal_id, 'user_info': user_info})

# delete meal function
@login_required
def delete_meal(request, meal_id):
    # obtain the instance of the meal
    try:
        meal = Meal.objects.get(id=meal_id)
    except Request.DoesNotExist:
        return redirect('foodies:user_meals')

    # Deleating
    meal.delete()
    return redirect('foodies:user_meals')

# user register form
def register(request):
    
    registered = False

    # Detecting POST request
    if request.method == 'POST':
        # Storing the info of user and user profile forms
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # validating both forms
        if user_form.is_valid() and profile_form.is_valid():
            
            # obtaining the info of the forms
            data = request.POST.copy()

            # Checking if one of these fields are checked, it not return error
            if data.get('isCooker') == None and data.get('isDinner') == None:
                messages.error(request, 'Invalid: Check at least 1 checkbox for Cooker or Dinner or both.')
                return HttpResponseRedirect('/register')

            # saving the form
            user = user_form.save()

            # setting and hashing the password
            user.set_password(user.password)
            user.save()

            # preventing the saving of the user profile so we can add other fields
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.name = data.get('name')

            # adding if the user is cooker, diner and the picture
            if data.get('isCooker') is not None:
                profile.isCooker = True

            if data.get('isDiner') is not None:
                profile.isDinner = True

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # saving the form info
            profile.save()

            # once the info is saved, loggin the user and return to home
            registered = True
            login(request, user)
            return redirect('foodies:index')
        else:
            # is forms are not valid return errors
            print(user_form.errors, profile_form.errors)
    else:
        # obtaining the forms to the shown in the view
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'foodies/register.html',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# User login form
def user_login(request):

    # Detecting if POST request
    if request.method == 'POST':

        # Obtaining the user and the password of the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Checking user credencials
        user = authenticate(username=username, password=password)

        # checking is the user is valid
        if user:
            if user.is_active:
                # login the user
                login(request, user)
                return redirect(reverse('foodies:index'))
            else:
                return HttpResponse("Your Foodies account is disabled.")
        else:
            # if there is a problem with the user account return errors
            print(f"Invalid login details: {username}, {password}")
            messages.error(request, 'Invalid login details.')
            return redirect(reverse('foodies:login'))

    else:
        return render(request, 'foodies/login.html')


# User logout function
@login_required
def user_logout(request):
    # logout
    logout(request)
    return redirect(reverse('foodies:index'))

# Obtainig cookies from the server
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# visitor cookie handler to manage user visit to pages
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

# user profile view 
@login_required
def user_profile(request):

    # obtaining the user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # profile title
    profile_title = "User Profile"

    # obtaining the user profile model info
    userProfile = UserProfile.objects.filter(user=user).first()
    
    # Setting the user info to be passed to the view
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'picture': userProfile.picture,
        'name': userProfile.name,
        'address': userProfile.address,
        'phone': userProfile.phone,
        'personalDescription': userProfile.personalDescription,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner,
        'isBestCooker': userProfile.isBestCooker,
    }

    # Obtainig user requests
    user_requests = Request(cooker=userProfile.id)

    return render(request, 'foodies/user_profile.html', context={'profile_title': profile_title,
                                                                 'user_info': user_info,
                                                                 'user_requests': user_requests, })

# User profile update form
@login_required
def user_profile_update(request):

    # page title
    profile_title = "Update User Profile"

    # Try to get the user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Try to get the user profile info
    userProfile = UserProfile.objects.filter(user=user).first()
    
    # Storing the user info
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        messages.error(request, 'The user does not exists')
        return HttpResponseRedirect('/user-profile')

    try:
        userProfile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        messages.error(request, 'The user does not exists')
        return HttpResponseRedirect('/user-profile')

    # passing the instance of the user to the form so the fields can be filled
    user_form = UserUpdateForm(request.POST or None, instance=user)
    
    # passing the instance of the user profile to the form so the fields can be filled
    user_profile_form = UserProfileUpdateForm(request.POST or None, instance=userProfile)

    # Validating the forms
    if user_form.is_valid() and user_profile_form.is_valid():

        # checking if the updated email wasnot taken b another user
        if User.objects.filter(email=request.POST.get('email')).exists() and request.user.email != request.POST.get(
                'email'):
            messages.error(request, 'The email is taken by another user')
            return HttpResponseRedirect('/user-profile/update/')

        # storing the form info and adding a new picture if this is passed
        user_form.save()
        profile = user_profile_form.save(commit=False)

        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']

        # saving the user profile info
        profile.save()
        return redirect('/user-profile')

    else:
        # printing errors if the form is not valid
        print(user_form.errors, user_profile_form.errors)

    return render(request, 'foodies/user_profile_update.html',
                  context={
                      'user_info': user_info,
                      'profile_title': profile_title,
                      'user_form': user_form,
                      'user_profile_form': user_profile_form
                  })

# User meals view, this only can be seen by cookers
@login_required
def user_meals(request):

    # page title
    profile_title = "User Meals"

    # Obtainig user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Obtainig user profile info
    userProfile = UserProfile.objects.filter(user=user).first()
    
    # Storing the info of the user
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    # checking is the user is a cooker, if not return to profile
    if user_info.get('isCooker') is False:
        return HttpResponseRedirect(reverse('foodies:user_profile'))

    # Obtaining the user profile info and the user meals
    user_profile = UserProfile.objects.filter(user=user)[0]
    user_meals = Meal.objects.filter(user=user_profile)

    return render(request, 'foodies/user_meals.html', context={'user_info': user_info,
                                                               'profile_title': profile_title,
                                                               'meals_info': user_meals})

# User meal requests view
@login_required
def user_requests(request):

    # page title
    profile_title = "User Requests"

    # Obtainig user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Obtainig user profile info
    user_profile = UserProfile.objects.filter(user=user).first()

    # Obtaining requests as cooker and as diner
    # in the HTML we have the validation to show he requests depending on the type of user
    requests_as_cooker = Request.objects.filter(cooker=user_profile.id)
    requests_as_diner = Request.objects.filter(dinner=user_profile.id)

    # Storing the user info
    user_info = {
        'id': user_profile.id,
        'email': user.email,
        'isCooker': user_profile.isCooker,
        'isDinner': user_profile.isDinner
    }

    return render(request, 'foodies/user_requests.html', context={
        'profile_title': profile_title,
        'requests_as_cooker': requests_as_cooker,
        'requests_as_diner': requests_as_diner,
        'user_info': user_info})

# User allergies view
@login_required
def show_allergies(request):

    # page title
    profile_title = "User Allergies"

    # Obtainig user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Obtainig user profile info
    user_profile = UserProfile.objects.filter(user=user).first()

    # Storing the user info
    user_info = {
        'id': user_profile.id,
        'email': user.email,
        'isCooker': user_profile.isCooker,
        'isDinner': user_profile.isDinner
    }

    # Obtaining stored allergies
    allergies = Allergy.objects.filter(users=user_profile.id)

    return render(request, 'foodies/user_allergies.html', context={ 'allergies': allergies,
                                                                    'profile_title': profile_title,
                                                                    'user_info': user_info})

# Add allergy form
@login_required
def add_allergy(request):
    
    # Page title
    profile_title = "Add Allergy"

    # Obtainig user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Obtainig user profile info
    user_profile = UserProfile.objects.filter(user=user).first()
    
    # Storing the user info
    user_info = {
        'id': user_profile.id,
        'email': user.email,
        'isCooker': user_profile.isCooker,
        'isDinner': user_profile.isDinner
    }

    # Obtaining allergies form
    allergies_form = AllergiesForm(request.POST)

    # Detecting if POST request
    if request.method == 'POST':
        
        # Check if form is valid
        if allergies_form.is_valid():

            # saving the info of the form
            allergy = allergies_form.save()
            allergy.save()

            # Obtainig the instance of the user profile so it can be saved in the allergy
            # As this is a many to many relation, we first have to create the allergy
            # then pass to the model the instance of the user so the relation can be created
            try:
                userProfile = UserProfile.objects.get(user=user)
            except User.DoesNotExist:
                return None

            # relation the new allergy with the authenticated user    
            allergy.users.add(userProfile)

            return redirect(reverse('foodies:show_allergies'))
        else:
            # if form is not valid return error
            messages.error(request, allergies_form.errors)
            HttpResponseRedirect(reverse('foodies:add_allergy'))

    return render(request, 'foodies/add_allergy.html', context={'allergies_form': allergies_form,
                                                                    'profile_title': profile_title,
                                                                    'user_info': user_info})

# update allergy form
@login_required
def edit_allergy(request, allergy_id):

    # page title
    profile_title = "Edit Allergy"

    # Obtainig user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Obtainig user profile info
    user_profile = UserProfile.objects.filter(user=user).first()
    
    # Storing the user info
    user_info = {
        'id': user_profile.id,
        'email': user.email,
        'isCooker': user_profile.isCooker,
        'isDinner': user_profile.isDinner
    }

    # Obtaining the info of the selected allergy 
    try:
        allergy = Allergy.objects.get(id=allergy_id)
    except Allergy.DoesNotExist:
        return None

    # Obtaining allergies form and passing the instance of selected allergy
    allergies_form = AllergiesForm(request.POST or None, instance=allergy)

    # Detecting if POST request
    if request.method == 'POST':
        # Checking is the form is valid
        if allergies_form.is_valid():

            # saving the form info
            allergy = allergies_form.save()
            allergy.save()

            # Obtainig authenticated user to relate the allergy
            try:
                userProfile = UserProfile.objects.get(user=user)
            except User.DoesNotExist:
                return None
                
            # relating allergy with user
            allergy.users.add(userProfile)

            return redirect(reverse('foodies:show_allergies'))
        else:
            # return error is form is not valid
            messages.error(request, allergies_form.errors)
            HttpResponseRedirect(reverse('foodies:add_allergy'))

    return render(request, 'foodies/edit_allergy.html', context={   'allergy_id':allergy_id,
                                                                    'allergies_form': allergies_form,
                                                                    'profile_title': profile_title,
                                                                    'user_info': user_info})

# Delete allergy function
@login_required
def delete_allergy(request, allergy_id):
    # try to obtain the selected allergy
    try:
        allergy = Allergy.objects.get(id=allergy_id)
    except Allergy.DoesNotExist:
        return redirect('foodies:show_allergies')
    
    # Once obtained, delete
    allergy.delete()
    return redirect('foodies:show_allergies')

# Delete request function
@login_required
def delete_request(request, request_id):
    # try to obtain the selected request
    try:
        select_request = Request.objects.get(id=request_id)
    except Request.DoesNotExist:
        return redirect('foodies:user_requests')

    # Once obtained, delete
    select_request.delete()
    return redirect('foodies:user_requests')

# form to add a review to a diner
@login_required
def add_review_to_diner(request, request_id):

    # page title
    profile_title = "Add a Review to Diner"

    # form url
    action_url = "foodies:add_review_to_diner"

    # Obtainig user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Obtainig user profile info
    userProfile = UserProfile.objects.filter(user=user).first()
    
    # Storing the user info
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    # detecting is POST request
    if request.method == 'POST':
        
        # Obtaining request to be reviewd
        request_info = Request.objects.filter(id=request_id).first()

        # Obtain the user who is going to be reviewd
        try:
            user_to_save = UserProfile.objects.get(id=request_info.dinner)
        except UserProfile.DoesNotExist:
            return None

        # obtainig the form
        review_form = ReviewsForm(request.POST)
        
        # validating the form
        if review_form.is_valid():
            # Saving the info of the form
            form = review_form.save(commit=False)
            form.user = user_to_save
            form.date = datetime.now()
            review_form.save()
            return redirect(reverse('foodies:user_requests'))
        else:
            # return errors if form not valid
            messages.error(request, review.errors)
            return HttpResponseRedirect('foodies:user_requests')
    else:
        # Obtaining review form
        review_form = ReviewsForm()

    return render(request, 'foodies/add_review.html',
                                                        context={'action_url':action_url,
                                                                'request_id': request_id,
                                                                'profile_title': profile_title,
                                                                'user_info': user_info,
                                                                'review_form': review_form})

# form to add a review to a cooker
@login_required
def add_review_to_cooker(request, request_id):

    # page title
    profile_title = "Add a Review to Cooker"
    
    # form url
    action_url = "foodies:add_review_to_cooker"

    # Obtainig user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    # Obtainig user profile info
    userProfile = UserProfile.objects.filter(user=user).first()
    
    # Storing user info
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    # detecting if POST request
    if request.method == 'POST':
        
        # Obtaining request to be reviewd
        request_info = Request.objects.filter(id=request_id).first()

        # Obtain the user who is going to be reviewd
        try:
            user_to_save = UserProfile.objects.get(id=request_info.cooker)
        except UserProfile.DoesNotExist:
            return None

        # Obtaining form
        review_form = ReviewsForm(request.POST)
        if review_form.is_valid():
            # Saving the info of the form
            form = review_form.save(commit=False)
            form.user = user_to_save
            form.date = datetime.now()
            review_form.save()
            return redirect(reverse('foodies:user_requests'))
        else:
            # If form is not valid return errors
            messages.error(request, review.errors)
            return HttpResponseRedirect(reverse('foodies:user_requests'))
    else:
        # Obtaining reviews form
        review_form = ReviewsForm()

    return render(request, 'foodies/add_review.html',
                                                        context={'action_url':action_url,
                                                                'request_id': request_id,
                                                                'profile_title': profile_title,
                                                                'user_info': user_info,
                                                                'review_form': review_form})

# User profile reviews view
@login_required
def user_reviews(request):

    # page title
    profile_title = "User Reviews"

    # Obtaining user model info
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None
    
    # Obtaining user profile info
    try:
        userProfile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        return None

    # Obtaining user reviews
    user_reviews = Review.objects.filter(user=userProfile)

    return render(request, 'foodies/user_reviews.html', {'all_reviews':user_reviews})

# Contact us page
def contact_us(request):
    return render(request, 'foodies/contact_us.html')

# Request a meal form
@login_required
def request_meal(request, meal_id):

    # Obtainig the info of the meal that is going to be requested
    meal = Meal.objects.filter(id=meal_id).first()

    # Detecting if POST request
    if request.method == 'POST':

        # Obtaining request meal form
        request_form = RequestAMealForm(request.POST)
        
        # Checking if form is valid
        if request_form.is_valid():
            # Preventing save of the form
            form = request_form.save(commit=False)
            
            # Passing all values that need to be saved
            form.cooker = meal.user.id
            form.dinner = request.user.id
            form.date = datetime.now()
            form.email = request.user.email

            # saving form
            request_form.save()
            return HttpResponseRedirect(reverse('foodies:meal_details', kwargs={'meal_id':meal_id}))
        else:
            # If form is not valid returning errors
            messages.error(request, request_form.errors)
            return HttpResponseRedirect(reverse('foodies:request_meal', kwargs={'meal_id':meal_id}))
    else:
        # Obtainig the meal form
        meal_form = RequestAMealForm()

    return render(request, 'foodies/request.html', context={
                                                              'meal': meal, 
                                                              'meal_form': meal_form })

# Meal details page
def show_meal_details(request, meal_id):
    
    # Obtain the info of selected meal
    meal_details = Meal.objects.filter(id=meal_id).first()
    
    # Adding one to the view
    meal_details.views = int(meal_details.views) + 1
    meal_details.save()
    return render(request, 'foodies/meal_details.html',  {'meal_id':meal_id,'meal_details':meal_details})

# Search page
def search(request):

    results = {}
    querystring = ""
    context = {}

    # Detecting if the parameter query exists in the GET request
    if 'query' in request.GET:
        # Obtaining the query from the field query
        querystring = request.GET.get('query')

        # Checking if the field has something
        if querystring is not None:

            # running a query to find meals that matches
            results_meals = Meal.objects.filter(Q(title__icontains=querystring)).order_by('pk')
            
            # running a query to find categories that matches
            results_cats = Category.objects.filter(Q(name__icontains=querystring)).order_by('pk')
            
            # running a query to find cookers that matches
            results_cookers = UserProfile.objects.filter(
                    Q(city__icontains=querystring) |
                    Q(specialty__icontains=querystring) &
                    Q(isCooker=1)
                ).order_by('pk')
            
            # storing all queries in variable to be passed to the view
            context = {
                'query': querystring,
                'results_meals': results_meals,
                'results_cats': results_cats,
                'results_cookers': results_cookers
            }

    return render(request, "foodies/search.html", context)

# Contact form reply view
def contact_reply(request):
    return render(request, 'foodies/contact_reply.html')

# public user profile page
def public_user_profile(request,id):

    # Obtaining the info of the authenticated user
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return None

    # page title
    profile_title = "User Profile"

    # Obtaining the info of the authenticated user profile
    userProfile = UserProfile.objects.filter(user=user).first()
    
    # Storing the user info
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'picture': userProfile.picture,
        'name': userProfile.name,
        'phone': userProfile.phone,
        'address': userProfile.address,
        'personalDescription': userProfile.personalDescription,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner,
        'isBestCooker': userProfile.isBestCooker,
    }

    # Obtaining the user meals
    user_meals = Meal.objects.filter(user=userProfile)
    
    # Obtaining the user reviews
    user_reviews = Review.objects.filter(user=userProfile)

    return render(request, 'foodies/user_profile_public.html', context={'id': id,
                                                                 'profile_title': profile_title,
                                                                 'user_info': user_info,
                                                                 'user_reviews': user_reviews,
                                                                 'user_meals': user_meals})

# function to check if the user is authenticated
def is_user_login(request):
    # If tru set loggedin variable to true, if not the opposite
    if request.user.id: 
        loggedin = True
    else:
        loggedin = False

    # return the response as a JSON response since we call this function with AJAX
    return JsonResponse({
        'is_loggedin': loggedin
    })

