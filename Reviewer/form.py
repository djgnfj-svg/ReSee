from django import forms
from django.contrib.auth.forms import UserCreationForm

from Reviewer.models import Users


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100, required=True, widget=forms.TextInput(attrs={"class" : "input-field", "placeholder": "이메일"})
    )
    password = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class" : "input-field", "placeholder": "유저이름"}))
    password = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
    )
    email = forms.EmailField(
        max_length=100, required=True, widget=forms.TextInput(attrs={"class" : "input-field", "placeholder": "이메일"})
    )

    class Meta:
        model = Users
        fields=(
        "username",
        "email",
        "password1",
        "password2",
        )
