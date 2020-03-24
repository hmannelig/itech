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


def index(request):
    user_list=UserProfile.objects.order_by('-id')[:6]
    category_list = Category.objects.order_by('-likes')[:6]
    meal_list = Meal.objects.order_by('-views')[:6]
    context_dict = {        
        'categories': category_list,
        'meals': meal_list,  
        'user_info':user_list 
    }
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

            return redirect('foodies/index')
        else:
            print(form.errors)

    return render(request, 'foodies/add_category.html', {'form': form})


@login_required
def add_meal(request):
    profile_title = "Add a Meal"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    userProfile = UserProfile.objects.filter(user=user).first()
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    if user_info.get('isCooker') is False:
        return HttpResponseRedirect(reverse('foodies:user_profile'))

    if request.method == 'POST':
        meal_form = MealForm(request.POST, request.FILES)

        if meal_form.is_valid():

            meal = meal_form.save(commit=False)
            user_profile = UserProfile.objects.filter(user=request.user).first()
            meal.user = user_profile

            if 'picture' in request.FILES:
                meal.picture = request.FILES['picture']

            meal.save()

            return redirect('foodies:user_meals')
        else:
            messages.error(request, meal_form.errors)
            return HttpResponseRedirect(reverse('foodies:add_meal'))
    else:
        meal_form = MealForm()

    return render(request, 'foodies/add_meal.html',
                  {'meal_form': meal_form, 'profile_title': profile_title, 'user_info': user_info})


@login_required
def edit_meal(request, meal_id):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    userProfile = UserProfile.objects.filter(user=user).first()
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    if user_info.get('isCooker') is False:
        return HttpResponseRedirect(reverse('foodies:user_profile'))

    try:
        meal = Meal.objects.get(id=meal_id)
    except User.DoesNotExist:
        messages.error(request, 'The meal does not exists')
        return HttpResponseRedirect(reverse('foodies:edit_meal', kwargs={'meal_id': meal_id}))

    meal_form = MealForm(request.POST or None, instance=meal)

    if request.method == 'POST':
        if meal_form.is_valid():

            meal_form.save()
            meal = meal_form.save(commit=False)

            if 'picture' in request.FILES:
                meal.picture = request.FILES['picture']

            meal.save()
            return HttpResponseRedirect(reverse('foodies:user_meals'))

        else:
            print(meal_form.errors)
            messages.error(request, meal_form.errors)
            return HttpResponseRedirect(reverse('foodies:edit_meal', kwargs={'meal_id': meal_id}))

    return render(request, 'foodies/edit_meal.html',
                  {'meal_form': meal_form, 'meal_id': meal_id, 'user_info': user_info})


def delete_meal(request, meal_id):
    try:
        meal = Meal.objects.get(id=meal_id)
    except Request.DoesNotExist:
        return redirect('foodies:user_meals')

    meal.delete()
    return redirect('foodies:user_meals')


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
                return HttpResponseRedirect('/register')

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
            return redirect('foodies:index')
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

    userProfile = UserProfile.objects.filter(user=user).first()
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

    user_requests = Request(cooker=userProfile.id)

    return render(request, 'foodies/user_profile.html', context={'profile_title': profile_title,
                                                                 'user_info': user_info,
                                                                 'user_requests': user_requests, })


@login_required
def user_profile_update(request):
    profile_title = "Update User Profile"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    userProfile = UserProfile.objects.filter(user=user).first()
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

    user_form = UserUpdateForm(request.POST or None, instance=user)
    user_profile_form = UserProfileUpdateForm(request.POST or None, instance=userProfile)

    if user_form.is_valid() and user_profile_form.is_valid():

        if User.objects.filter(email=request.POST.get('email')).exists() and request.user.email != request.POST.get(
                'email'):
            messages.error(request, 'The email is taken by another user')
            return HttpResponseRedirect('/user-profile/update/')

        user_form.save()
        profile = user_profile_form.save(commit=False)

        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']

        profile.save()
        return redirect('/user-profile')

    else:
        print(user_form.errors, user_profile_form.errors)

    return render(request, 'foodies/user_profile_update.html',
                  context={
                      'user_info': user_info,
                      'profile_title': profile_title,
                      'user_form': user_form,
                      'user_profile_form': user_profile_form
                  })


@login_required
def user_meals(request):
    profile_title = "User Meals"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    userProfile = UserProfile.objects.filter(user=user).first()
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    if user_info.get('isCooker') is False:
        return HttpResponseRedirect(reverse('foodies:user_profile'))

    user_profile = UserProfile.objects.filter(user=user)[0]
    user_meals = Meal.objects.filter(user=user_profile)

    return render(request, 'foodies/user_meals.html', context={'user_info': user_info,
                                                               'profile_title': profile_title,
                                                               'meals_info': user_meals})


@login_required
def user_requests(request):
    profile_title = "User Requests"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    user_profile = UserProfile.objects.filter(user=user).first()

    requests_as_cooker = Request.objects.filter(cooker=user_profile.id)
    requests_as_diner = Request.objects.filter(dinner=user_profile.id)

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


@login_required
def show_allergies(request):
    profile_title = "User Allergies"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    user_profile = UserProfile.objects.filter(user=user).first()
    user_requests = Request.objects.filter(cooker=user_profile.id)
    user_info = {
        'id': user_profile.id,
        'email': user.email,
        'isCooker': user_profile.isCooker,
        'isDinner': user_profile.isDinner
    }

    allergies = Allergy.objects.filter(users=user_profile.id)

    return render(request, 'foodies/user_allergies.html', context={ 'allergies': allergies,
                                                                    'profile_title': profile_title,
                                                                    'user_info': user_info})

@login_required
def add_allergy(request):
    profile_title = "Add Allergy"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    user_profile = UserProfile.objects.filter(user=user).first()
    user_requests = Request.objects.filter(cooker=user_profile.id)
    user_info = {
        'id': user_profile.id,
        'email': user.email,
        'isCooker': user_profile.isCooker,
        'isDinner': user_profile.isDinner
    }

    allergies_form = AllergiesForm(request.POST)

    if request.method == 'POST':
        if allergies_form.is_valid():

            allergy = allergies_form.save()
            allergy.save()

            try:
                userProfile = UserProfile.objects.get(user=user)
            except User.DoesNotExist:
                return None
                
            allergy.users.add(userProfile)

            return redirect(reverse('foodies:show_allergies'))
        else:
            messages.error(request, allergies_form.errors)
            HttpResponseRedirect(reverse('foodies:add_allergy'))

    return render(request, 'foodies/add_allergy.html', context={'allergies_form': allergies_form,
                                                                    'profile_title': profile_title,
                                                                    'user_info': user_info})

@login_required
def edit_allergy(request, allergy_id):
    profile_title = "Edit Allergy"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    user_profile = UserProfile.objects.filter(user=user).first()
    user_requests = Request.objects.filter(cooker=user_profile.id)
    user_info = {
        'id': user_profile.id,
        'email': user.email,
        'isCooker': user_profile.isCooker,
        'isDinner': user_profile.isDinner
    }

    try:
        allergy = Allergy.objects.get(id=allergy_id)
    except Allergy.DoesNotExist:
        return None

    allergies_form = AllergiesForm(request.POST or None, instance=allergy)

    if request.method == 'POST':
        if allergies_form.is_valid():

            allergy = allergies_form.save()
            allergy.save()

            try:
                userProfile = UserProfile.objects.get(user=user)
            except User.DoesNotExist:
                return None
                
            allergy.users.add(userProfile)

            return redirect(reverse('foodies:show_allergies'))
        else:
            messages.error(request, allergies_form.errors)
            HttpResponseRedirect(reverse('foodies:add_allergy'))

    return render(request, 'foodies/edit_allergy.html', context={   'allergy_id':allergy_id,
                                                                    'allergies_form': allergies_form,
                                                                    'profile_title': profile_title,
                                                                    'user_info': user_info})

@login_required
def delete_allergy(request, allergy_id):
    try:
        allergy = Allergy.objects.get(id=allergy_id)
    except Allergy.DoesNotExist:
        return redirect('foodies:show_allergies')
    
    allergy.delete()
    return redirect('foodies:show_allergies')

@login_required
def delete_request(request, request_id):
    try:
        select_request = Request.objects.get(id=request_id)
    except Request.DoesNotExist:
        return redirect('foodies:user_requests')

    select_request.delete()
    return redirect('foodies:user_requests')


def add_review_to_diner(request, request_id):

    profile_title = "Add a Review to Diner"
    action_url = "foodies:add_review_to_diner"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    userProfile = UserProfile.objects.filter(user=user).first()
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    if request.method == 'POST':
        request_info = Request.objects.filter(id=request_id).first()

        try:
            user_to_save = UserProfile.objects.get(id=request_info.dinner)
        except UserProfile.DoesNotExist:
            return None

        review_form = ReviewsForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = user_to_save
            form.date = datetime.now()
            review_form.save()
            return redirect(reverse('foodies:user_requests'))
        else:
            messages.error(request, review.errors)
            return HttpResponseRedirect('foodies:user_requests')
    else:
        review_form = ReviewsForm()

    return render(request, 'foodies/add_review.html',
                                                        context={'action_url':action_url,
                                                                'request_id': request_id,
                                                                'profile_title': profile_title,
                                                                'user_info': user_info,
                                                                'review_form': review_form})

def add_review_to_cooker(request, request_id):

    profile_title = "Add a Review to Cooker"
    action_url = "foodies:add_review_to_cooker"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None

    userProfile = UserProfile.objects.filter(user=user).first()
    user_info = {
        'id': userProfile.id,
        'email': user.email,
        'isCooker': userProfile.isCooker,
        'isDinner': userProfile.isDinner
    }

    if request.method == 'POST':
        request_info = Request.objects.filter(id=request_id).first()

        try:
            user_to_save = UserProfile.objects.get(id=request_info.cooker)
        except UserProfile.DoesNotExist:
            return None

        review_form = ReviewsForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = user_to_save
            form.date = datetime.now()
            review_form.save()
            return redirect(reverse('foodies:user_requests'))
        else:
            messages.error(request, review.errors)
            return HttpResponseRedirect(reverse('foodies:user_requests'))
    else:
        review_form = ReviewsForm()

    return render(request, 'foodies/add_review.html',
                                                        context={'action_url':action_url,
                                                                'request_id': request_id,
                                                                'profile_title': profile_title,
                                                                'user_info': user_info,
                                                                'review_form': review_form})


def register_diners(request):
    return render(request, 'foodies/register_diners.html')

def user_reviews(request):
    profile_title = "User Reviews"

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return None
    
    try:
        userProfile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        return None

    user_reviews = Review.objects.filter(user=userProfile)

    return render(request, 'foodies/user_reviews.html', {'all_reviews':user_reviews})


def register_cookers(request):
    return render(request, 'foodies/register_cookers.html')


def search_cookers(request):
    return HttpResponse("This is search cooker")


def contact_us(request):
    return render(request, 'foodies/contact_us.html')

@login_required
def request_meal(request, meal_id):

    meal = Meal.objects.filter(id=meal_id).first()

    if request.method == 'POST':

        request_form = RequestAMealForm(request.POST)
        if request_form.is_valid():
            form = request_form.save(commit=False)
            form.cooker = meal.user.id
            form.dinner = request.user.id
            form.date = datetime.now()
            form.email = request.user.email
            request_form.save()
            return HttpResponseRedirect(reverse('foodies:meal_details', kwargs={'meal_id':meal_id}))
        else:
            messages.error(request, request_form.errors)
            return HttpResponseRedirect(reverse('foodies:request_meal', kwargs={'meal_id':meal_id}))
    else:
        meal_form = RequestAMealForm()

    return render(request, 'foodies/request.html', context={
                                                              'meal': meal, 
                                                              'meal_form': meal_form })


def show_meal_details(request, meal_id):
    
    meal_details = Meal.objects.filter(id=meal_id).first()
    return render(request, 'foodies/meal_details.html',  {'meal_id':meal_id,'meal_details':meal_details})

def search(request):
    results = {}
    querystring = ""
    context = {}

    if 'query' in request.GET:
        querystring = request.GET.get('query')
        if querystring is not None:
            results_meals = Meal.objects.filter(Q(title__icontains=querystring)).order_by('pk')
            results_cats = Category.objects.filter(Q(name__icontains=querystring)).order_by('pk')
            results_cookers = UserProfile.objects.filter(
                    Q(city__icontains=querystring) |
                    Q(specialty__icontains=querystring) &
                    Q(isCooker=1)
                ).order_by('pk')
            context = {
                'query': querystring,
                'results_meals': results_meals,
                'results_cats': results_cats,
                'results_cookers': results_cookers
            }

    return render(request, "foodies/search.html", context)

def contact_reply(request):
    return render(request, 'foodies/contact_reply.html')

def public_user_profile(request,id):

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return None

    profile_title = "User Profile"

    userProfile = UserProfile.objects.filter(user=user).first()
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

    user_meals = Meal.objects.filter(user=userProfile)
    user_reviews = Review.objects.filter(user=userProfile)

    return render(request, 'foodies/user_profile_public.html', context={'id': id,
                                                                 'profile_title': profile_title,
                                                                 'user_info': user_info,
                                                                 'user_reviews': user_reviews,
                                                                 'user_meals': user_meals})


def is_user_login(request):
    if request.user.id: 
        loggedin = True
    else:
        loggedin = False

    return JsonResponse({
        'is_loggedin': loggedin
    })

