from django import forms
from django.forms.widgets import PasswordInput



class LoginForm(forms.Form):
	email = forms.CharField(
		max_length=100, required=True, widget=forms.TextInput(attrs={"class" : "input-field", "placeholder": "이메일"})
	)
	password = forms.CharField(
		max_length=30, required=True, 
		widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
	)
