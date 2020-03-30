from django.contrib import admin
from foodies.models import Category, Meal, UserProfile, Ingredient, Allergy

# Adjustment for the Meal model in the admin, so it display the title of the Meal
class MealAdmin(admin.ModelAdmin):
    list_display = ('title',)

# Adjustment for the Catygeory model in the admin, so it display the slug field of the Categories
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Registering the models in the admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(UserProfile)
admin.site.register(Ingredient)
admin.site.register(Allergy)