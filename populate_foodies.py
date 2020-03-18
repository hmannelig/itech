import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodies_project.settings')

import django

django.setup()
from foodies.models import Category, Meal



def populate():

    african_meals = [
        {'title': 'Egusi Soup from Nigeria',
         'price': '12',
         'url': 'http://www.africanbites.com/egusi-soup/',
         'views': 10},
        {'title': 'Thieboudienne from Senegal',
         'price': '12',
         'url': 'http://www.internationalcuisine.com/thieboudienne/',
         'views': 20},
        {'title': 'Muamba de Galinha from Angola',
         'price': '12',
         'url': 'http://www.africanbites.com/muamba-chickenmuamba-de-galinha/',
         'views': 22}]

    american_meals = [
        {'title': 'Tacos by Jamie Oliver',
         'price': '12',
         'url': 'http://www.jamieoliver.com/recipes/beef-recipes/beef-tacos/',
         'views': 250},
        {'title': 'Chicken Enchiladas',
         'price': '12',
         'url': 'http://www.delish.com/cooking/recipe-ideas/a49105/cheesy-chicken-enchiladas-recipe/',
         'views': 123}]

    asian_meals = [
        {'title': 'Ramen from Japan',
         'price': '12',
         'url': 'http://www.justonecookbook.com/homemade-chashu-miso-ramen/',
         'views': 111},
        {'title': 'Vietnamese Summer Rolls',
         'price': '12',
         'url': 'https://www.bonappetit.com/recipe/vietnamese-summer-rollscxs',
         'views': 332}]

    european_meals = [
        {'title': 'Spaghetti Aglio e Olio from Italy',
         'price': '12',
         'url': 'https://www.allrecipes.com/recipe/222000/spaghetti-aglio-e-olio/',
         'views': 111},
        {'title': 'Sauerkraut from Germany',
         'price': '12',
         'url': 'https://www.allrecipes.com/recipe/228631/bavarian-sauerkraut/',
         'views': 332}]

    cats = {
            'African': 
                {
                    'meals': african_meals, 'views': 128, 'likes': 64
                },
            'American': 
                {
                    'meals': american_meals, 'views': 64, 'likes': 32
                },
            'Asian': 
                {
                    'meals': asian_meals, 'views': 32, 'likes': 16
                },
            'European': 
                {
                    'meals': european_meals, 'views': 24, 'likes': 22
                }
            }

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['meals']:
            add_meal(c, p['title'], p['url'], p['price'], views=p['views'])

    for c in Category.objects.all():
        for p in Meal.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_meal(cat, title, url, price, views=0):
    p = Meal.objects.get_or_create(category=cat, title=title, price=price)[0]
    p.url = url
    p.price = price
    p.views = views
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print('Starting Foodies population script...')
    populate()