from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    height = models.FloatField()
    age = models.IntegerField()
    activity_level = models.FloatField(choices=[(1.2, 'Sedentary'), (1.375, 'Lightly active'), (1.55, 'Moderately active'), (1.725, 'Very active'), (1.9, 'Extremely active')])

    def __str__(self):
        return f'{self.user.username} Profile'
    
class BMIRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)

    def calculate_bmi(self):
            height_in_meters = float(self.height) / 100  # Convert height to float before division

            # Check if height_in_meters is zero to avoid division by zero
            if height_in_meters == 0:
                return 0

            return float(self.weight) / (height_in_meters ** 2)
    def __str__(self):
        return f'{self.user.username} - {self.date}'
    
class FoodIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    food_name = models.CharField(max_length=255)
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    protein = models.DecimalField(max_digits=6, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=2)
    fats = models.DecimalField(max_digits=6, decimal_places=2)

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    calories = models.PositiveIntegerField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    fat = models.FloatField()
    
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    ]
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)

    def __str__(self):
        return self.title
    
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - Meal Plan created on {self.created_at}'