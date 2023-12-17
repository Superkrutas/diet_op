from django.contrib import admin
from .models import FoodIntake
from .models import Recipe
from .models import Profile

class FoodIntakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'food_name', 'calories', 'protein', 'carbohydrates', 'fats')
    list_filter = ('user', 'date')

admin.site.register(FoodIntake, FoodIntakeAdmin)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    list_filter = ('created_by', 'created_at')
    search_fields = ('title', 'description', 'ingredients', 'instructions', 'protein', 'carbohydrates', 'fat', 'meal_type')

admin.site.register(Recipe, RecipeAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'height', 'age', 'activity_level')

admin.site.register(Profile, ProfileAdmin)