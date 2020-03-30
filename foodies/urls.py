from django.urls import path
from foodies import views

app_name = 'foodies'

urlpatterns = [
    # home view
    path('', views.index, name='index'),
    # about view
    path('about/', views.about, name='about'),
    # speficid category view
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'), 
    # create a cayegory form
    path('add-category/', views.add_category, name='add_category'),
    # New mapping!
    path('register/', views.register, name='register'),  
    # login form
    path('login/', views.user_login, name='login'), 
    # logout url
    path('logout/', views.user_logout, name='logout'),
    # user profile view
    path('user-profile/', views.user_profile, name = 'user_profile'), 
    # user profile update form
    path('user-profile/update/', views.user_profile_update, name = 'user_profile_update'), 
    # add meal form
    path('user-profile/meals/add/', views.add_meal, name='add_meal'),  
    # update meal form
    path('user-profile/meals/<int:meal_id>/edit/', views.edit_meal, name='edit_meal'),  
    # delete meal url
    path('user-profile/meals/<int:meal_id>/delete/', views.delete_meal, name='delete_meal'),
    # user profile meals
    path('user-profile/meals/', views.user_meals, name='user_meals'),  
    # user requests delete url
    path('user-profile/requests/<int:request_id>/delete/', views.delete_request, name='delete_request'), 
    # user requests view
    path('user-profile/requests/', views.user_requests, name='user_requests'),  
    # user reviews view
    path('user-profile/reviews/', views.user_reviews, name='user_reviews'),  
    # diner user allergies view
    path('user-profile/allergies/', views.show_allergies, name='show_allergies'),  
    # diner user register allergies form
    path('user-profile/allergies/add', views.add_allergy, name='add_allergy'),  
    # diner user update allergies form
    path('user-profile/allergies/<int:allergy_id>/edit', views.edit_allergy, name='edit_allergy'),  
    # diner user delete allergy url
    path('user-profile/allergies/<int:allergy_id>/delete', views.delete_allergy, name='delete_allergy'),  
    # search view
    path('search/', views.search, name='search'),  
    # contact us view
    path('contact-us/', views.contact_us, name = 'contact_us'), 
    # contact form reply view
    path('contact-reply/', views.contact_reply, name='contact_reply'),
    # specific meal view
    path('meal/<int:meal_id>/', views.show_meal_details, name='meal_details'),
    # request a meal form
    path('meal/<int:meal_id>/request/', views.request_meal, name='request_meal'),  
    # public user profile view
    path('public-user-profile/<int:id>/', views.public_user_profile, name='public_user_profile'),  
    # user login validator url
    path('is_user_login/', views.is_user_login, name='is_user_login'),
    # add review to diner form
    path('user-profile/add-review-diner/<int:request_id>', views.add_review_to_diner, name='add_review_to_diner'),  
    # add review to cooker form
    path('user-profile/add-review-cooker/<int:request_id>', views.add_review_to_cooker, name='add_review_to_cooker'),  
]
