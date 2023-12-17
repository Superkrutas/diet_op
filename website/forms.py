from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import BMIRecord
from .models import FoodIntake
from .models import Recipe
from .models import Profile

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'height', 'age', 'activity_level']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Gender'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height (in cm)'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'activity_level': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Activity Level'}),
        }
        
class BMIForm(forms.ModelForm):
    class Meta:
        model = BMIRecord
        fields = ['date', 'weight', 'height']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select Date'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Weight (in kg)'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Height (in cm)'}),
        }
class FoodIntakeForm(forms.ModelForm):
    class Meta:
        model = FoodIntake
        fields = ['date', 'food_name', 'calories', 'protein', 'carbohydrates', 'fats']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select Date'}),
            'food_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Food Name'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Calories'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Protein'}),
            'carbohydrates': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Carbohydrates'}),
            'fats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Fats'}),
        }
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'calories', 'protein', 'carbohydrates', 'fat', 'meal_type']