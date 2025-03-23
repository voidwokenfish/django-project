from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': "login-class",
        'placeholder': 'Введите почту',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "login-class",
        'placeholder': 'Введите пароль',
    }))

    class Meta:
        model = User
        fields = ('email', 'password')
