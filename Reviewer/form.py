from django import forms
from django.contrib.auth.forms import UserCreationForm

from Reviewer.models import Users


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일"})
    )
    password = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields=(
        "username",
        "password1",
        "password2",
        "email",
        )
        
    username = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(attrs={"class" : "input-field", "placeholder": "유저이름"})
        )
    password1 = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
    )
    password2 = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드 확인"})
    )
    email = forms.EmailField(
        max_length=30, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일"})
    )
    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(RegisterForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
