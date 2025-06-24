from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from .models import Profile, User


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

class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 != p2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data


class PasswordForgotForm(forms.Form):
    email = forms.EmailField(label="Введите актуальную почту, привязанную к аккаунту", required=True, widget=forms.TextInput(attrs={}))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class SetNewEmailForm(forms.Form):
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(attrs={}))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data