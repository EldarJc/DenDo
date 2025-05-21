import re

from django import forms
from django.contrib.auth.hashers import check_password
from django.core.validators import MinLengthValidator

from .models import CustomUser
from .utils import UserHelper

class SignUpForm(forms.Form):

    """
    Form for creating a new user.

    Fields:
        - username
        - Email
        - password
        - confirm_password
    """

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[MinLengthValidator(limit_value=8, message='Password must be at least 8 characters long')]
    )

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-z]{2,}$', username.strip()):
            raise forms.ValidationError("Username cannot be an email address.")

        user = UserHelper.get_user(username)
        if user:
            raise forms.ValidationError('That username is already taken')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = UserHelper.get_user(email)
        if user:
            raise forms.ValidationError('Email is already registered. Try logging in instead.')
        
        return email


    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match.')
            
        return cleaned_data

class UserEditForm(forms.ModelForm):

    """
    Form for editing a user's profile.

    Fields:
        - avatar
        - banner
        - username
        - bio
    
    Requires:
        - 'user' instance to be passed during initialization.
    """
    class Meta:
        model = CustomUser
        fields = ['banner', 'avatar', 'username', 'bio']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if self.user is None:
            raise ValueError('User is required for this form.')
        super().__init__(*args, **kwargs)
        self.fields['banner'].required = False
        self.fields['avatar'].required = False
        self.fields['username'].required = False
        self.fields['bio'].required = False


    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username:

            if re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', username.strip()):
                raise forms.ValidationError("Username cannot be an email address.")

            elif username == self.user.username:
                raise forms.ValidationError('This is already your current username.')
            
            elif UserHelper.get_user(username):
                raise forms.ValidationError('Username is already taken. Please choose another one.')

        return username
        
    def save(self, commit = True):
        user_profile = self.user
        if user_profile is None:
            raise ValueError("User instance must be provided to save the form.")
        data_changed = 0

        for field in self.fields:
            field_value = self.cleaned_data.get(field)
            
            if field_value in [None, '']:
                continue

            elif field in ['avatar', 'banner'] and field in self.files:
                current_image = getattr(user_profile, field)
                if current_image:
                    current_image.delete(save=False)

            setattr(user_profile, field, field_value)
            data_changed += 1

        if commit and data_changed > 0:
            user_profile.save()
        
        return user_profile

class PasswordUpdateForm(forms.Form):
    """
        Form for updating a user's password.

        Fields:
            - old_password
            - new_password
        
        Internal parameters (passed to form):
            - current_password_hash
    """

    def __init__(self, *args, **kwargs):
        self.password_hash = kwargs.pop('current_password_hash', None)
        if self.password_hash is None:
            raise ValueError('User password is required for this form.')
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        validators=[MinLengthValidator(limit_value=8, message='Password must be at least 8 characters long')])

    def clean_old_password(self):
        old_password_input = self.cleaned_data.get('old_password')

        if old_password_input:
            if not check_password(old_password_input, self.password_hash):
                raise forms.ValidationError('Old password is incorrect.')
        return old_password_input
            
    def clean_new_password(self):
        new_password_input = self.cleaned_data.get('new_password')

        if new_password_input :
            if check_password(new_password_input , self.password_hash):
                raise forms.ValidationError('New password cannot be the same as old password.')
        return new_password_input

class LogInForm(forms.Form):
    """
        Form for authenticating a user.

        Fields:
            - username_or_email
            - password
    """
    username_or_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email or username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if username_or_email and password:
            user = UserHelper.get_user(username_or_email)

            if user:
                if not user.check_password(password):
                    raise forms.ValidationError('Login failed. Make sure your email/username and password are correct.')
            else:
                raise forms.ValidationError('Login failed. Make sure your email/username and password are correct.')
        return cleaned_data