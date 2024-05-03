from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# https://stackoverflow.com/questions/5827590/css-styling-in-django-forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username-password-form'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'username-password-form'}))

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username',help_text='', error_messages={'required': ''})
    email = forms.EmailField(help_text='', error_messages={'required': ''})
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='', error_messages={'required': ''})
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, help_text='', error_messages={'required': ''})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email