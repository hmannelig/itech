from django.urls import path
from foodies import views

app_name = 'foodies'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/add_meal/', views.add_meal,
         name='add_meal'),
    path('category/<slug:category_name_slug>/', views.show_category,
         name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('register/', views.register, name='register'),  # New mapping!
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]
