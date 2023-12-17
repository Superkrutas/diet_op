from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .models import BMIRecord, FoodIntake, Recipe
from .forms import BMIForm
from .views import bmi_tracker
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import FoodIntake
class BMITrackerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = RequestFactory()

    def test_bmi_tracker_view_get(self):
        # Test BMI tracker view with a GET request
        request = self.factory.get(reverse('bmi_tracker'))
        request.user = self.user
        response = bmi_tracker(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bmi_tracker.html')

    def test_bmi_tracker_view_post_valid_data(self):
        # Test BMI tracker view with a POST request and valid data
        data = {'weight': 70, 'height': 175, 'date': '2023-01-01'}
        request = self.factory.post(reverse('bmi_tracker'), data)
        request.user = self.user
        response = bmi_tracker(request)
        self.assertEqual(response.status_code, 302)  # Should redirect after a successful POST

        # Add more assertions to check if the BMIRecord was created and other expected outcomes

    def test_bmi_tracker_view_post_invalid_data(self):
        # Test BMI tracker view with a POST request and invalid data
        data = {'weight': -10, 'height': 175, 'date': '2023-01-01'}
        request = self.factory.post(reverse('bmi_tracker'), data)
        request.user = self.user
        response = bmi_tracker(request)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page for invalid data
        self.assertContains(response, 'Enter a valid number.')
class FoodIntakeTrackerViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_food_intake_tracker_view_for_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a POST request to the food_intake_tracker view
        response = self.client.post(reverse('food_intake_tracker'), {'calories': 200, 'protein': 10, 'carbohydrates': 20, 'fats': 5})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that a FoodIntake object has been created
        self.assertEqual(FoodIntake.objects.count(), 1)

    def test_food_intake_tracker_view_for_unauthenticated_user(self):
        # Log out any existing user
        self.client.logout()

        # Make a POST request to the food_intake_tracker view
        response = self.client.post(reverse('food_intake_tracker'), {'calories': 200, 'protein': 10, 'carbohydrates': 20, 'fats': 5})

        # Check that the response status code is 302 (redirect to login)
        self.assertEqual(response.status_code, 302)

        # Check that no FoodIntake object has been created
        self.assertEqual(FoodIntake.objects.count(), 0)
class HomeViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_home_view_for_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a POST request to the home view
        response = self.client.post(reverse('home'), {'username': 'testuser', 'password': 'testpassword'})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the 'user' key is in the context
        self.assertIn('user', response.context)

    def test_home_view_for_unauthenticated_user(self):
        # Log out any existing user
        self.client.logout()

        # Make a POST request to the home view
        response = self.client.post(reverse('home'), {'username': 'testuser', 'password': 'testpassword'})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the 'user' key is in the context
        self.assertIn('user', response.context)

class LogoutUserViewTests(TestCase):
    def test_logout_user_view(self):
        # Log in a test user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the logout_user view
        response = self.client.get(reverse('logout_user'))

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the user is logged out
        self.assertNotIn('_auth_user_id', self.client.session)

class RegisterUserViewTests(TestCase):
    def test_register_user_view_for_valid_data(self):
        # Make a POST request to the register_user view with valid data
        response = self.client.post(reverse('register_user'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that a new user is created
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_register_user_view_for_invalid_data(self):
        # Make a POST request to the register_user view with invalid data
        response = self.client.post(reverse('register_user'), {'username': '', 'password1': 'newpassword', 'password2': 'newpassword'})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that no new user is created
        self.assertEqual(User.objects.count(), 0)