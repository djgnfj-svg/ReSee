from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models.base import Model
from django.utils.translation import gettext_lazy as _
from Reviewer.models import Categories, StudyList, Users


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일"})
    )
    password = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
    )


class MemberModifiForm(forms.Form):
    class Meta:
        model = Users
        fields = (
            "useremail"
        )
    useremail = forms.EmailField(
        max_length=30, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일수정"})
    )

class MemberDelForm(forms.Form):
    class Meta:
        model = Users
        fields = (
            "useremail",
            "password",
        )
    useremail = forms.EmailField(
        max_length=30, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일수정"})
    )
    password1 = forms.CharField(
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
        "useremail",
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
    useremail = forms.EmailField(
        max_length=30, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일"})
    )
    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(RegisterForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        user.email = self.cleaned_data["useremail"]
        if commit:
            user.save()
        return user

class CateCreateForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ["category_name"]
        labels = {
            "category_name" : _("과목이름"),
        }
        widgets ={
            "category_name":forms.TextInput(attrs={"class" : "form-control", "placeholder" : "과목이름을 입력하세욥!"}),
        }
        
    def save(self, request, commit=True):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.created_by_id = request.user.id
        instance.category_name = instance.category_name.strip()
        if commit:
            print("Teststsets")
            instance.save()
        return instance

    def update_form(self, request, list_id):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.category_name = instance.category_name.strip()
        Categories.objects.filter(pk=list_id, created_by_id=request.user.id).update(category_name=instance.category_name)

class StudyCreateForm(forms.ModelForm):
    class Meta:
        model = StudyList
        fields = [
            "study_topic",
            "study_contect",
        ]
        widgets ={
            "study_topic":forms.TextInput(attrs={"class" : "form-control", "placeholder" : "학습 주제를 입력하세요! ex.. 접두사"}),
            "study_contect":forms.TextInput(attrs={"class" : "form-control", "placeholder" : "학습 내용을 입력하세요"}),
        }
    def save(self, request, temp, commit=True):
        instance = super(StudyCreateForm, self).save(commit=False)
        instance.created_by_id = request.user.id
        instance.category_id_id = temp
        instance.nick_name = instance.nick_name.strip()
        instance.study_topic = instance.study_topic.strip()
        instance.study_contect = instance.study_contect.strip()
        if commit:
            instance.save()
        return instance

    def update_form(self, request, list_id):
        instance = super(StudyCreateForm, self).save(commit=False)
        instance.nick_name = instance.nick_name.strip()
        instance.study_topic = instance.study_topic.strip()
        instance.study_contect = instance.study_contect.strip()
        StudyList.objects.filter(pk=list_id, created_by_id=request.user.id).update(category_name=instance.category_name)
