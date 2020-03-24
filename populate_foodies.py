import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodies_project.settings')

import django

django.setup()
from foodies.models import Category, Meal, User, UserProfile, Allergy, Review
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
            'isBestCooker'  : True,
            'allergies'       : [
                {
                    'name': 'Explosions',
                    'name': 'Bad food',
                    'name': 'Rotten tomatoes'
                }
            ],
            'reviews'       : [
                {
                    'title'     : 'Best cooker in the world',
                    'date'      : '2020-02-01',
                    'rating'    : '5',
                    'content'   : 'I hired her for a bussines dinner and it was the best thing I could have ever done, everything was delicious.'
                }, 
                {
                    'title'     :'I kinda liked it',
                    'date'      :'2019-11-12',
                    'rating'    :'3',
                    'content'   :'I have to say I am not a big fan of Greek food, it was... nice'
                }
            ]
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
            'isBestCooker': False,
            'allergies'       : [
                {
                    'name': 'People',
                    'name': 'Bullets'
                }
            ],
            'reviews'       : [
                {
                    'title'     : 'Totally recommended as a diner',
                    'date'      : '2019-07-23',
                    'rating'    : '5',
                    'content'   : 'He hired me for his weekly meals. He is an honest and good client'
                }
            ]
        },
        {
            'username'      : 'efra',
            'name'          : 'Efraín Villanueva',
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
            'isBestCooker': True,
            'allergies'       : [],
            'reviews'       : [
                {
                    'title'     : 'Never hire this guy',
                    'date'      : '2019-07-23',
                    'rating'    : '1',
                    'content'   : 'His mix of tacos with lots of things is really disgusting, NEVER HIRE THIS GUYS PLEASE'
                },
                {
                    'title'     : 'Poisonous food',
                    'date'      : '2019-07-29',
                    'rating'    : '2',
                    'content'   : 'I am giving him 2 stars ONLY because I didn\'t die'
                }
            ]
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
            'isBestCooker': False,
            'allergies'       : [
                {
                    'name': 'Jump from buildings',
                    'name': 'Swim with sharks',
                    'name': 'Drink Gasoline'
                }
            ],
            'reviews'       : [
                {
                    'title'     : 'Did you read her description? IS TRUE',
                    'date'      : '2020-03-01',
                    'rating'    : '5',
                    'content'   : 'OMG she is amazing! if you haven\'t tried her style PLEASE DO!!! I WILL BUY IT FOR YOU!'
                }
            ]
        }
    ]

    users_instances = []
    
    african_meals = [
        {
            'title': 'Egusi Soup from Nigeria',
            'price': '12',
            'views': 10,
            'picture': 'dish-1.jpg',
            'ingredients': 'onions, fresh chilies, egusi melon seeds, palm oil, Une Iru, locust beans, Ground crayfish, Cooked Meat & fish, pumpkin leaves, waterleaf cut, bitter leaf washed',
            'recipe': 'EGUSI PASTE: \n Prepare the egusi paste: \n Blend egusi seeds and onion mixture. Set aside.\nMAKE THE SOUP: \n In a large pot, heat the palm oil on medium for a minute and then add the Une. \n Slowly add the stock and set on low heat to simmer. \n Scoop teaspoon size balls of the egusi paste mixture into the stock. Be sure to keep ball shape. \n Leave to simmer for 20 – 30 minutes so the balls cook through. \n Add the meat and fish and other bits which you’d like to use. \n Add cut-up pumpkin leaves. \n Add the waterleaf. \n Stir and put a lid on the pot and allow cook for 7–10 minutes, till the leaves wilt. \n Add the bitter leaf.  Leave the lid off while the cooking finishes for another 5-10 minutes. \n Stir, check seasoning and adjust accordingly.'
        },
        {
            'title': 'Thieboudienne from Senegal',
            'price': '12',
            'views': 20,
            'picture': 'dish-2.jpg',
            'ingredients': 'Whole fish, grouper, sea bream, bass, pike, hake, tilapia or snapper, bunch parsley, shallots, garlic, hot peppers, piece nététou, dried fish (guedj), vegetable oil, onion, tomato paste, tomatoes, bay leaves, carrots',
            'recipe': 'Prepare fish stuffing. Mix parsley, 2 garlic cloves, shallots, 2 hot peppers, stock cube and salt with a mortar and pestle. Set aside. \n Clean the fish if necessary. Rinse and dry with paper towels. Make 2 to 3 deep diagonal cuts in each fish. Stuff each fish cut with the mixture. \n Heat the vegetable oil in a deep skillet. Fry fish for 6 to 7 minutes on each side and set aside. \n Reduce heat and add the remaining 2 garlic cloves and onion. Add the remaining 2 peppers and mix for 5 minutes. \n Meanwhile, grind the remaining stock cube, dried fish and nététou using a food processor. \n Pour the powder, tomato paste and peeled tomatoes in the pan. Add salt and pepper. Simmer for 5 minutes. Add the bay leaves and 1 cup of water. Simmer for 15 minutes over low heat. \n Add the vegetables to the pot and simmer for 30 minutes. Remove the vegetables as they are cooked through but still firm and reserve. \n Add the rice, previously rinsed and add enough water to cover the rice, about 4 cups. \n Cook 20 to 30 minutes uncovered. Stir occasionally while cooking. \n Add the vegetables and fish back to the pan and cook for an additional 5 minutes. \n Place rice and vegetables and fish pieces on each plate. Serve hot with lemon slices.'
        },
        {   
            'title': 'Muamba de Galinha from Angola',
            'price': '12',
            'views': 22,
            'picture': 'dish-3.jpg',
            'ingredients': 'Chicken, lemon juice optional, white pepper, garlic, dried thyme, smoked paprika, chicken bouillon powder, canola oil, palm oil, onions, tomatoes diced, white pepper, smoked paprika, hot pepper pierced chili, Scotch bonnet, butternut, Okra, chicken broth',
            'recipe': 'Place chicken in a large bowl or saucepan, rub with lemon juice, \n Then add salt, garlic, white pepper and chicken bouillon. \n Mix chicken with a spoon or with hands until they are well coated, set aside. \n \n When ready to cook, heat up large saucepan with palm and canola oil, then add chicken, brown both sides for about 4-5 minutes. \n \n Add garlic, chili pepper and smoked paprika, stir for about a minute then add onions and tomatoes, sauté 2-3 minutes until onions is translucent. \n Add chicken stock if necessary to prevent any burns \n \n Next add chicken stock or water (about 2 cups or enough to cover chicken. Add chicken bouillon, and squash. Bring to a boil and let it simmer until sauce thickens, it might take about 20 or more depending on the type of chicken used. Throw in okra, continue cooking until desired texture is reached about 5 minutes or more \n Adjust for salt, pepper and stew consistency. \n Serve warm with Cornmeal mash or rice.'
        }
    ]

    american_meals = [
        {
            'title': 'Tacos by Jamie Oliver',
            'price': '12',
            'views': 250,
            'picture': 'dish-4.jpg',
            'ingredients': 'onion, red pepper, green pepper, olive oil, garlic, paprika, cumin, beef, beef stock, corn taco shells \n\n SALSA \n ripe tomatoes, spring onion, sprigs of fresh coriander, lime \n \n GUACAMOLE \n avocados, lime, crème fraîche',
            'recipe': 'Peel and dice the onion, then deseed and dice the peppers. Soften in 1 tablespoon of oil in a large pan over a low heat. \n Peel, finely slice and add the garlic, along with the paprika and cumin, and cook for 1 to 2 minutes. Add the beef and stir until it has browned. \n Pour in the stock, cover, and cook for 45 minutes, or until reduced and delicious. \n Preheat the oven to 180ºC/350ºF/gas 4. \n For the salsa, roughly chop the tomatoes, trim and finely slice the spring onion, then pick and roughly chop the coriander leaves. Combine with the lime juice, then season carefully to taste. \n For the guacamole, halve and destone the avocados, then mash the flesh with a fork. Squeeze in the lime juice, add the crème fraîche, season, and gently mix it all up. \n Spread the taco shells out on a baking tray and place in the oven for 3 to 4 minutes until crisp. \n Fill the shells with the meat, salsa and guacamole or lay everything out and let everyone help themselves.'
        },
        {
            'title': 'Chicken Enchiladas',
            'price': '12',
            'views': 123,
            'picture': 'dish-5.jpg',
            'ingredients': 'Chicken \n Onion and diced green chiles \n Beans \n Tortillas \n Cheese \n Toppings',
            'recipe': 'Prepare your sauce.  Get your homemade enchilada sauce simmering in a separate saucepan while you prepare the rest of the enchiladas. \n Prepare your filling.  Sauté the onion, followed by the diced chicken and green chiles.  Season with salt and pepper.  Then (recipe update!) go ahead and stir in the black beans to complete your filling. \n Assemble your enchiladas.  Lay a single tortilla on a flat surface.  Spread a generous spoonful of enchilada sauce over the surface of the tortilla.  Then spoon your filling mixture in a line down the middle of the tortilla, roll it up, and… \n Arrange the enchiladas in a baking dish. You can either place the chicken enchiladas seam-side-up or seam-side-down.  Then pour any remaining sauce on top of the enchiladas and sprinkle on some extra cheese. \n Bake the enchiladas. Bake uncovered until the enchiladas are cooked through and the edges of the tortillas get slightly crispy.  Remove from the oven, sprinkle with your favorite toppings, and... \n Serve warm.  And enjoy!'
        }
    ]

    asian_meals = [
        {
            'title': 'Ramen from Japan',
            'price': '12',
            'views': 111,
            'picture': 'dish-6.jpg',
            'ingredients': 'Chicken, garlic, soy sauce, Worcestershire sauce, Chinese five spice pinch of chilli powder, white sugar, ramen noodles, pork or chicken breast, sesame oil For the garnish, baby spinach, sweetcorn, boiled eggs, dried nori, green spring onions or shallots sprinkle of sesame seeds',
            'recipe': 'Mix 700ml chicken stock, 3 halved garlic cloves, 4 tbsp soy sauce, 1 tsp Worcestershire sauce, a sliced thumb-sized piece of ginger, ½ tsp Chinese five spice, pinch of chilli powder and 300ml water in a stockpot or large saucepan, bring to the boil, then reduce the heat and simmer for 5 mins. \n\n Taste the stock – add 1 tsp white sugar or a little more soy sauce to make it sweeter or saltier to your liking.\n\n Cook 375g ramen noodles following the pack instructions, then drain and set aside. \n\n Slice 400g cooked pork or chicken, fry in 2 tsp sesame oil until just starting to brown, then set aside. \n\n Divide the noodles between four bowls. Top each with a quarter of the meat, 25g spinach, 1 tbsp sweetcorn and two boiled egg halves each. \n\n Strain the stock into a clean pan, then bring to the boil once again. \n\n Divide the stock between the bowls, then sprinkle over 1 shredded nori sheet, sliced spring onions or shallots and a sprinkle of sesame seeds. Allow the spinach to wilt slightly before serving.',
        },
        {   
            'title': 'Vietnamese Summer Rolls',
            'price': '12',
            'views': 332,
            'picture': 'dish-1.jpg',
            'ingredients': 'dipping sauce, lime juice, fish sauce, sugar, red Thai chiles or 1 red jalapeño or Fresno chile, thinly sliced \n\n summer rolls\n bean thread noodles, rice paper roundst, shrimp, basil leavest, cilantro leaves, mint leaves, daikon sprouts, English hothouse cucumber, carrot, green or red leaves',
            'recipe': 'Put noodles in a large bowl. Pour enough hot water over to cover; let stand until softened, about 10 minutes. Drain. Transfer to a large bowl of ice water to cool; drain and set aside. \n\n Fill a pie plate with warm water. Working with 1 rice paper round at a time, soak rice paper in water, turning occasionally, until just pliable but not limp, about 30 seconds. Transfer to a work surface. Arrange 3 shrimp halves across center of round. Top with some leaves of each herb, then daikon sprouts (if using), cucumber, and carrot. Arrange a small handful of noodles over. Place 1 lettuce leaf over, torn or folded to fit. Fold bottom of rice paper over filling, then fold in ends and roll like a burrito into a tight cylinder. Transfer roll, seam side down, to a platter. Repeat to make 11 more rolls. DO AHEAD Can be made 1 hour ahead. Cover with a damp kitchen towel and refrigerate.'
        }
    ]

    european_meals = [
        {
            'title': 'Spaghetti Aglio e Olio from Italy',
            'price': '12',
            'views': 111,
            'picture': 'dish-2.jpg',
            'ingredients':'Spaghetti, garlic, olive oil, red pepper flakes, fresh Italian parsley, Parmigiano-Reggiano cheese',
            'recipe':'Bring a large pot of lightly salted water to a boil. Cook spaghetti in the boiling water, stirring occasionally until cooked through but firm to the bite, about 12 minutes. Drain and transfer to a pasta bowl. \n\n Combine garlic and olive oil in a cold skillet. Cook over medium heat to slowly toast garlic, about 10 minutes. Reduce heat to medium-low when olive oil begins to bubble. Cook and stir until garlic is golden brown, about another 5 minutes. Remove from heat. \n\n Stir red pepper flakes, black pepper, and salt into the pasta. Pour in olive oil and garlic, and sprinkle on Italian parsley and half of the Parmigiano-Reggiano cheese; stir until combined. \n\n Serve pasta topped with the remaining Parmigiano-Reggiano cheese.'
        },
        {
            'title': 'Sauerkraut from Germany',
            'price': '12',
            'views': 332,
            'picture': 'dish-3.jpg',
            'ingredients':'Cabbage, juniper berries, caraway seeds, yellow mustard seeds, un-iodized salt',
            'recipe':'º. Gather the ingredients \n 2. In a clean, non-metallic bowl, mix together cabbage, juniper berries, caraway seeds, mustard seeds, and pickling salt. \n 3. Stir the cabbage to release its juices. \n 4. Let it rest 10 minutes and then mix again. You might let this rest longer, as much as 1 to 2 hours, if needed. \n 5. Sterilize a 1-quart wide-mouthed Mason jar and lid by boiling for several minutes in water and draining on a clean dishcloth. \n 6. Pack the cabbage and seasonings into the sterilized jar, pushing down with a wooden (not metal) spoon. \n 7. Pack the cabbage and seasonings into the sterilized jar, pushing down with a wooden (not metal) spoon.'
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
        instanced_user = add_users(user['username'], user['email'], user['password'], user['isCooker'], user['isDinner'], user['isBestCooker'], user['name'], user['address'], user['city'], user['specialty'], user['phone'], user['personalDescription'], user['picture'])
        if user['isCooker']:
            users_instances.append(instanced_user)

        for allergy in user['allergies']:
            add_allergy(instanced_user, allergy['name'])
        
        for review in user['reviews']:
            add_review(instanced_user, review['title'], review['date'], review['rating'], review['content'])
        
        print(f'- user {user} created')

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['meals']:
            user_selected = random.choice(users_instances)
            add_meal(c, user_selected, p['title'], p['price'], p['ingredients'], p['recipe'], p['views'], p['picture'])

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

def add_meal(cat, user, title, price, ingredients, recipe, views=0, picture=""):
    p = Meal.objects.get_or_create(category=cat, title=title, price=price, user=user, ingredients=ingredients, recipe=recipe)[0]
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

def add_review(user, title, date, rating, content):
    r = Review.objects.get_or_create(user=user, title=title, date=date, rating=rating, content=content)[0]
    return r

def add_allergy(user, name):
    a = Allergy.objects.get_or_create(name=name)[0]
    a.users.add(user)
    return a

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