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

    class Meta:
        model = Users
        fields=(
        "username",
        "email",
        "password1",
        )
        
    username = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(attrs={"class" : "input-field", "placeholder": "유저이름"})
        )
    password = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
    )
    email = forms.EmailField(
        max_length=30, required=True, widget=forms.TextInput(attrs={"class" : "input-field", "placeholder": "이메일"})
    )
    def save(self, commit=True):  # save메소드 오버라이
        user = super(RegisterForm, self).save(commit=False) # 기존의 id와 pw를 저장. commit이 Flase인 이유는 2번 저장하는것 방지.
        user.email = self.cleaned_data["email"]               # user 객체에 email 값 추가.
        if commit:
            user.save()              # 객체에 대한 모든 정보를 DB에 저장.
        return user