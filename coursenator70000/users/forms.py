from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Пароли не совпадают.")


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': "login-class",
        'placeholder': 'Введите логин',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "login-class",
        'placeholder': 'Введите пароль',
    }))

    error_messages = {
        'invalid_login': "Неверное имя пользователя или пароль.",
        'inactive': "Этот аккаунт неактивен.",
    }

    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
    'accept': 'image/jpg, image/jpeg, image/png',
    'style': 'display: none;',
    'onchange': 'this.form.submit();'
    }))
    class Meta:
        model = Profile
        fields = ['avatar']