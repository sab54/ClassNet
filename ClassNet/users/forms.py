from django import forms
from .models import CustomUser    
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    """
    Form for user registration, including fields for username, first name, last name, email,
    password, and confirming the password. This form handles the validation and saving of 
    user data to create a new CustomUser.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'profile_picture']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A custom form for changing passwords, extending the built-in PasswordChangeForm.
    This form adds custom functionality, such as allowing the user to update their password
    with additional validation and logic as needed.
    """
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

class UserSearchForm(forms.Form):
    """
    Form for searching users based on username, email, or user type (e.g., Student, Teacher).
    This form allows admins or users to filter users based on different search criteria.
    """
    query = forms.CharField(
        label='Search',
        max_length=100,
        min_length=3,  # Enforces a minimum length of 3 characters
        required=False,
        widget=forms.TextInput(attrs={'minlength': 3})  # Optional: HTML5 client-side validation
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']
