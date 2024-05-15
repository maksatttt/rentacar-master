from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import RentU, Cars


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False, help_text='По желанию')
    last_name = forms.CharField(max_length=30, required=False, help_text='По желанию')
    username = forms.CharField(max_length=30, required=True, help_text='По желанию')

    class Meta:
        model = RentU
        fields = ["email", "password1", "password2", 'first_name', 'last_name', 'username']



