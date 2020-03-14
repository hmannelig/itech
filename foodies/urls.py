from django.urls import path
from foodies import views

app_name = 'foodies'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/add_meal/', views.add_meal, name='add_meal'), #/categories
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'), #/categories/african
    path('add_category/', views.add_category, name='add_category'),
    path('register/', views.register, name='register'),  # New mapping!
    path('login/', views.user_login, name='login'), # /login
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('user-profile/', views.user_profile, name = 'user_profile'), #/user-profile
    path('user-profile/reviews', views.reviews, name='reviews'),  #/user-profile/reviews
    path('register-diners/', views.register_diners, name = 'register_diners'), #/register-diners
    path('register-cookers/', views.register_cookers, name = 'register_cookers'), #/register-cookers
    path('search/', views.search, name='search'),  #/search
    path('search-cookers/', views.search_cookers, name='search_cookers'),  #/search
    path('contact-us/', views.contact_us, name = 'contact_us'), #/contact-us
]
