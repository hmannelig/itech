import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodies_project.settings')

import django

django.setup()
from foodies.models import Category, Meal, User, UserProfile
import random



def populate():

    profile_picture_path = "profile_images/"

    users = [
        {
            'username'      : 'elpi',
            'name'          : 'Elpida Vasiou',
            'address'       : 'Happy Steet 5',
            'city'          : 'Glasgow',
            'specialty'     : 'Greek',
            'phone'         : '76 77 12 34 99',
            'personalDescription' : 'I am the best cooker of Greek food you will ever found, based in Glasgow I trained to the point where my cooking skills have a mix of flavours with Inidian food and Italian.',
            'picture'       : profile_picture_path + 'elpi-profile-picture.jpg',
            'email'         : 'elpi@email.com',
            'password'      : 'user',
            'isCooker'      : True,
            'isDinner'      : True,
            'isBestCooker'  : True
        },
        {
            'username'      : 'pablo',
            'name'          : 'Pablo Berjon',
            'address'       : 'Studying Steet 7',
            'city'          : 'Madrid',
            'specialty'     : 'Spanish',
            'phone'         : '76 12 34 77 99',
            'personalDescription' : 'With 5 years of experience in Mediterranean and Spanish food, my style of cooking is unique since I know how to preserve the original flavours of all ingredients, what Paella? just let me know',
            'picture'       : profile_picture_path + 'pablo-profile-picture.jpg',
            'email': 'pablo@email.com',
            'password': 'user',
            'isCooker': False,
            'isDinner': True,
            'isBestCooker': False
        },
        {
            'username': 'efra',
            'name'          : 'Pablo Berjon',
            'address'       : 'LOL Steet 3',
            'city'          : 'Cancún',
            'specialty'     : 'Mexican',
            'phone'         : '99 12 34 77 91',
            'personalDescription' : 'When it comes to me the only think you need to know is tacos. Based on Cancun I have met the best cookers in the world and learned how to give a twist fo my tacos, combining mexican flavours with techniques from around the world',
            'picture'       : profile_picture_path + 'efra-profile-picture.jpg',
            'email'   : 'efra@email.com',
            'password': 'user',
            'isCooker': True,
            'isDinner': False,
            'isBestCooker': True
        },
        {
            'username'      : 'linh',
            'name'          : 'Linh Diem',
            'address'       : 'Safe Steet 1',
            'city'          : 'Frankfurt',
            'specialty'     : 'Vietnamese',
            'phone'         : '02 12 63 77 13',
            'personalDescription' : 'Want homemade food from Vietname? from China? Japan, Korea? I have mastered all of the Asian style of cooking, therefore I am the best Asian Cheff you will ever meet, specially because I focus in cooking that tastes like home.',
            'picture'       : profile_picture_path + 'linh-profile-picture.jpg',
            'email'   : 'linh@email.com',
            'password': 'user',
            'isCooker': False,
            'isDinner': True,
            'isBestCooker': False
        }
    ]

    users_instances = []

    african_meals = [
        {
            'title': 'Egusi Soup from Nigeria',
            'price': '12',
            'views': 10,
            'picture': 'dish-1.jpg'
        },
        {
            'title': 'Thieboudienne from Senegal',
            'price': '12',
            'views': 20,
            'picture': 'dish-2.jpg'
        },
        {   
            'title': 'Muamba de Galinha from Angola',
            'price': '12',
            'views': 22,
            'picture': 'dish-3.jpg'
        }
    ]

    american_meals = [
        {
            'title': 'Tacos by Jamie Oliver',
            'price': '12',
            'views': 250,
            'picture': 'dish-4.jpg'
        },
        {
            'title': 'Chicken Enchiladas',
            'price': '12',
            'views': 123,
            'picture': 'dish-5.jpg'
        }
    ]

    asian_meals = [
        {
            'title': 'Ramen from Japan',
            'price': '12',
            'views': 111,
            'picture': 'dish-6.jpg'
        },
        {   
            'title': 'Vietnamese Summer Rolls',
            'price': '12',
            'views': 332,
            'picture': 'dish-1.jpg'
        }
    ]

    european_meals = [
        {
            'title': 'Spaghetti Aglio e Olio from Italy',
            'price': '12',
            'views': 111,
            'picture': 'dish-2.jpg'
        },
        {
            'title': 'Sauerkraut from Germany',
            'price': '12',
            'views': 332,
            'picture': 'dish-3.jpg'
        }
    ]

    cats = {
        'African': {
            'meals': african_meals, 
            'views': 128, 
            'likes': 64
        },
        'American': {
            'meals': american_meals, 
            'views': 64, 
            'likes': 32
        },
        'Asian': {
            'meals': asian_meals, 
            'views': 32, 
            'likes': 16
        },
        'European': {
            'meals': european_meals, 
            'views': 24, 
            'likes': 22
        }
    }

    for user in users:
        user = add_users(user['username'], user['email'], user['password'], user['isCooker'], user['isDinner'], user['isBestCooker'], user['name'], user['address'], user['city'], user['specialty'], user['phone'], user['personalDescription'], user['picture'])
        if user.isCooker:
            users_instances.append(user)
        print(f'- user {user} created')

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['meals']:
            user_selected = random.choice(users_instances)
            add_meal(c, user_selected, p['title'], p['price'], views=p['views'], picture=p['picture'])

    for c in Category.objects.all():
        for p in Meal.objects.filter(category=c):
            print(f'- {c}: {p}')

# def add_user(user):
#     u = User.objects.get_or_create(username=user['username'], email=user['email'])[0]
#     u.save()
#     u.set_password(user['password'])
#     u.save()
#
#     uprof = UserProfile.objects.get_or_create(user=u, isCooker=user['isCooker'], isDinner=user['isDinner'])
#     uprof.save()

def add_meal(cat, user, title, price, views=0, picture=""):
    p = Meal.objects.get_or_create(category=cat, title=title, price=price, user=user)[0]
    p.price = price
    p.views = views
    p.picture = picture
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_users(username, email, password, isCooker, isDiner, isBestCooker, name, address, city, specialty, phone, personalDescription, picture):
    user = User.objects.get_or_create(username=username, email=email)[0]
    user.set_password(password)
    user.save()
    userProfile = UserProfile.objects.get_or_create(name=name, address=address, city=city, specialty=specialty, phone=phone, personalDescription=personalDescription, picture=picture, isCooker=isCooker, isDinner=isDiner, isBestCooker=isBestCooker, user=user)[0]
    userProfile.save()
    return userProfile

# Start execution here!
if __name__ == '__main__':
    print('Starting Foodies population script...')
    populate()