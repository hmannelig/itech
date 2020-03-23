from django.contrib import admin
from foodies.models import Category, Meal, UserProfile, Ingredient, Allergy

class MealAdmin(admin.ModelAdmin):
    list_display = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(UserProfile)
admin.site.register(Ingredient)
admin.site.register(Allergy)