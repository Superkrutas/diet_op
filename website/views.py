from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from .forms import SignUpForm, BMIForm, FoodIntakeForm, ProfileForm
from .models import BMIRecord, FoodIntake, Recipe
from decimal import Decimal
import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def home(request):
    # Renders the home page and handles user authentication.

    # If the request method is POST, attempts to authenticate the user with the provided
    # username and password. If successful, logs in the user; otherwise, displays an error message.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in!")
        else:
            messages.success(request, "Error, try again!")

    user = request.user

    context = {
            'user': user,
        }    
    return render(request, 'home.html', context)
@csrf_exempt
def logout_user(request):
    # Logs out the authenticated user, displays a success message, and redirects to the home page.
    # Calls the Django `logout` function to log out the user associated with the given request.
    logout(request)
    # Displays a success message to inform the user that they have been logged out.
    messages.success(request, "You are logged out!")
    # Redirects the user to the home page after successful logout.
    return redirect('home')
@csrf_exempt
def register_user(request):
    # Handles user registration, processes registration form submissions, and logs in new users.

    # Checks if the HTTP request method is POST, indicating a form submission.
    if request.method == 'POST':
        # Instantiates SignUpForm and ProfileForm objects with the data from the POST request.
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

        # Validates both user and profile forms.
        if user_form.is_valid() and profile_form.is_valid():
            # Saves the user object and returns a User instance.
            user = user_form.save()

            # Saves the profile object with the user association.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Logs in the newly registered user.
            login(request, user)

            # Displays a success message and redirects the user to the home page.
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')

    # If the request method is not POST, creates empty user and profile forms.
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()

    # Renders the registration form page with the user and profile forms.
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})
@csrf_exempt
@login_required
def bmi_tracker(request):
    # View for handling BMI tracking, displaying recommendations, and providing meal plans.
    context = {}
    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            bmi_record = form.save(commit=False)
            bmi_record.user = request.user
            bmi_record.save()
            return redirect('bmi_tracker')
    else:
        form = BMIForm()
    
    bmi_records = BMIRecord.objects.filter(user=request.user).order_by('date')
    
    # Use the most recent BMI record for calculations
    latest_bmi_record = bmi_records.last()
    
    if latest_bmi_record:
            average_bmi = latest_bmi_record.calculate_bmi()
            bmi_category = calculate_bmi_category(average_bmi)
    else:
        average_bmi = 0  # Set a default value if there's no latest_bmi_record
        bmi_category = calculate_bmi_category(average_bmi)

    if average_bmi < 18.5:
        overall_recommendation = "Your latest BMI suggests that you should consider increasing your daily calorie intake for healthy weight gain."
        meal_plan_recommendation = "Consider a meal plan that includes a balanced mix of protein, carbohydrates, and healthy fats. Include nutrient-dense foods like lean meats, whole grains, and fruits."
    elif 18.5 <= average_bmi < 24.9:
        overall_recommendation = "Your latest BMI suggests that you should aim to maintain your current daily calorie intake for weight maintenance."
        meal_plan_recommendation = "Maintain a balanced diet with a mix of protein, carbohydrates, and healthy fats. Include a variety of fruits, vegetables, and whole grains in your meals."
    else:
        overall_recommendation = "Your latest BMI suggests that you should consider reducing your daily calorie intake for weight management."
        meal_plan_recommendation = "Focus on a calorie-controlled diet with an emphasis on nutrient-dense foods. Include plenty of fruits, vegetables, lean proteins, and whole grains."

    dates = [record.date.strftime('%Y-%m-%d') for record in bmi_records]
    bmi_values = [record.calculate_bmi() for record in bmi_records]

    if bmi_records.exists():
        average_bmi = float(BMIRecord.objects.filter(user=request.user).aggregate(Avg('weight'))['weight__avg'] or 0)
        activity_level = float(request.user.profile.activity_level)
        # Calculate daily calorie intake using the Harris-Benedict equation
        # The formula varies for men and women
        if request.user.profile.gender == 'M':
            bmr = 88.362 + (13.397 * average_bmi) + (4.799 * float(request.user.profile.height)) - (5.677 * float(request.user.profile.age))
        else:
            bmr = 447.593 + (9.247 * average_bmi) + (3.098 * float(request.user.profile.height)) - (4.330 * float(request.user.profile.age))

        # Apply activity level multiplier (assuming a sedentary level for demonstration)
        daily_calories_needed = bmr * activity_level

        # Calculate daily calories from food intake records
        food_intake_data = FoodIntake.objects.filter(user=request.user, date__gte=min(dates), date__lte=max(dates))
        daily_calories_consumed = float(food_intake_data.aggregate(Sum('calories'))['calories__sum'] or 0)

        # Calculate the remaining daily calories
        if daily_calories_consumed is not None:
            remaining_calories = daily_calories_needed - daily_calories_consumed
        else:
            remaining_calories = daily_calories_needed
        if bmi_category == 'Underweight':
            # Fetch recipes for underweight individuals
            breakfast_recommendation = Recipe.objects.filter(meal_type='Breakfast').first()
            lunch_recommendation = Recipe.objects.filter(meal_type='Lunch').first()
            dinner_recommendation = Recipe.objects.filter(meal_type='Dinner').first()
        elif bmi_category == 'Normal weight':
            # Fetch recipes for normal-weight individuals
            breakfast_recommendation = Recipe.objects.filter(meal_type='Breakfast').first()
            lunch_recommendation = Recipe.objects.filter(meal_type='Lunch').first()
            dinner_recommendation = Recipe.objects.filter(meal_type='Dinner').first()
        elif bmi_category == 'Overweight':
            # Fetch recipes for overweight individuals
            breakfast_recommendation = Recipe.objects.filter(meal_type='Breakfast').first()
            lunch_recommendation = Recipe.objects.filter(meal_type='Lunch').first()
            dinner_recommendation = Recipe.objects.filter(meal_type='Dinner').first()
        else:
            # Fetch recipes for obese individuals
            breakfast_recommendation = Recipe.objects.filter(meal_type='Breakfast').first()
            lunch_recommendation = Recipe.objects.filter(meal_type='Lunch').first()
            dinner_recommendation = Recipe.objects.filter(meal_type='Dinner').first()
        
        context = {
            'form': form,
            'bmi_records': bmi_records,
            'bmi_category': bmi_category,
            'overall_recommendation': overall_recommendation,
            'meal_plan_recommendation': meal_plan_recommendation,
            'dates_json': json.dumps(dates),
            'bmi_values_json': json.dumps(bmi_values),
            'daily_calories_needed': daily_calories_needed,
            'daily_calories_consumed': daily_calories_consumed,
            'remaining_calories': remaining_calories,
            'breakfast_recommendation': breakfast_recommendation,
            'lunch_recommendation': lunch_recommendation,
            'dinner_recommendation': dinner_recommendation,

        }
    else:
        # Handle the case when there are no BMI records
        context = {
            'form': form,
            'bmi_records': [],
            'bmi_category': [],
            'overall_recommendation': "No BMI records available. Please input your BMI data to get recommendations.",
            'meal_plan_recommendation': "",
            'dates_json': json.dumps([]),
            'bmi_values_json': json.dumps([]),
            'daily_calories_needed': 0,
            'daily_calories_consumed': 0,
            'remaining_calories': 0,
        }

    return render(request,'bmi_tracker.html', context)

def calculate_bmi_category(bmi_value):# Categorize BMI into different weight status categories: 'Underweight', 'Normal weight', 'Overweight', or 'Obese'.
    if bmi_value < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi_value < 24.9:
        return 'Normal weight'
    elif 25 <= bmi_value < 29.9:
        return 'Overweight'
    else:
        return 'Obese'
    

# View function for tracking food intake.
# Allows authenticated users to input their daily food intake, providing a form to submit the data.
# Displays a summary of daily totals for calories, protein, carbohydrates, and fats.
# Uses charts to visualize the data over time.
@csrf_exempt
@login_required
def food_intake_tracker(request):
    if request.method == 'POST':
        form = FoodIntakeForm(request.POST)
        if form.is_valid():
            food_intake = form.save(commit=False)
            food_intake.user = request.user
            food_intake.save()

    form = FoodIntakeForm()
    food_intake_data = FoodIntake.objects.filter(user=request.user).order_by('date')
    daily_totals = food_intake_data.values('date').annotate(
            total_calories=Sum('calories'),
            total_protein=Sum('protein'),
            total_carbohydrates=Sum('carbohydrates'),
            total_fats=Sum('fats')
        )

    dates = [entry['date'].strftime('%Y-%m-%d') for entry in daily_totals]
    daily_calories = [float(entry['total_calories']) for entry in daily_totals]
    daily_protein = [float(entry['total_protein']) for entry in daily_totals]
    daily_carbohydrates = [float(entry['total_carbohydrates']) for entry in daily_totals]
    daily_fats = [float(entry['total_fats']) for entry in daily_totals]

    context = {
            'form': form,
            'food_intake_data': food_intake_data,
            'dates_json': json.dumps(dates),
            'daily_calories_json': json.dumps(daily_calories),
            'daily_protein_json': json.dumps(daily_protein),
            'daily_carbohydrates_json': json.dumps(daily_carbohydrates),
            'daily_fats_json': json.dumps(daily_fats),
    }    
    return render(request, 'food_intake_tracker.html', context)
# View function for displaying a list of all recipes.
# Retrieves all Recipe objects from the database and passes them to the template for rendering.
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})
# View function for displaying the details of a specific recipe.
# Retrieves a Recipe object with the given ID from the database and passes it to the template for rendering.
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

# Function for generating meal recommendations based on BMI category and daily calorie needs.
# It takes the BMI category and daily calories needed as parameters and returns a dictionary
# with recommendations for breakfast, lunch, and dinner.
def get_meal_recommendations(bmi_category, daily_calories_needed):
    if bmi_category == 'Underweight':
        # Fetch recipes for underweight individuals
        breakfast_recommendation = Recipe.objects.filter(meal_type='Breakfast').first()
        lunch_recommendation = Recipe.objects.filter(meal_type='Lunch').first()
        dinner_recommendation = Recipe.objects.filter(meal_type='Dinner').first()
    elif bmi_category == 'Normal weight':
        # Fetch recipes for normal-weight individuals
        breakfast_recommendation = Recipe.objects.filter(meal_type='Breakfast').first()
        lunch_recommendation = Recipe.objects.filter(meal_type='Lunch').first()
        dinner_recommendation = Recipe.objects.filter(meal_type='Dinner').first()
    elif bmi_category == 'Overweight':
        # Fetch recipes for overweight individuals
        breakfast_recommendation = Recipe.objects.filter(meal_type='Breakfast', calories__lte=daily_calories_needed * 0.2).first()
        lunch_recommendation = Recipe.objects.filter(meal_type='Lunch', calories__lte=daily_calories_needed * 0.3).first()
        dinner_recommendation = Recipe.objects.filter(meal_type='Dinner', calories__lte=daily_calories_needed * 0.4).first()
    else:
        # Fetch recipes for obese individuals
        breakfast_recommendation = Recipe.objects.filter(meal_type='Breakfast', calories__lte=daily_calories_needed * 0.1).first()
        lunch_recommendation = Recipe.objects.filter(meal_type='Lunch', calories__lte=daily_calories_needed * 0.2).first()
        dinner_recommendation = Recipe.objects.filter(meal_type='Dinner', calories__lte=daily_calories_needed * 0.3).first()

    return {
        'Breakfast': breakfast_recommendation,
        'Lunch': lunch_recommendation,
        'Dinner': dinner_recommendation,
    }