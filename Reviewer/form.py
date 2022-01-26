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
        fields = ["name"]
        labels = {
            "name" : _("과목이름"),
        }
        widgets ={
            "name":forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "케테고리 입력하세욥!",
                }),
        }
        
    def save(self, request, commit=True):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.creator_id = request.user.id
        instance.name = instance.name.strip()
        if commit:
            print("Teststsets")
            instance.save()
        return instance

    def update_form(self, request, list_id):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.category_name = instance.category_name.strip()
        Categories.objects.filter(pk=list_id, creator_id=request.user.id).update(category_name=instance.category_name)

class StudyCreateForm(forms.ModelForm):
    class Meta:
        model = StudyList
        fields = [
            "study_topic",
            "study_contect",
        ]
        widgets ={
            "study_topic":forms.Textarea(attrs={
                "class" : "form-control",
                 "placeholder" : "학습 주제를 입력하세요! ex.. 접두사",
                 "style" : "height : 30px"
                 }),
            "study_contect":forms.Textarea(attrs={
                "class": "new-class-name two",
                 "placeholder" : "학습 내용을 입력하세요",
                 "style" : "height : 500px; width : 90.75rem; outline:none; border:none; overflow: auto;"
                 }),
        }
    def save(self, request, category_id, commit=True):
        instance = super(StudyCreateForm, self).save(commit=False)
        instance.creator_id = request.user.id
        instance.category_id = category_id
        instance.study_topic = instance.study_topic.strip()
        instance.study_contect = instance.study_contect.strip()
        instance.review_count = 0
        if commit:
            instance.save()
        return instance

    def update_form(self, request, list_id):
        instance = super(StudyCreateForm, self).save(commit=False)
        instance.study_topic = instance.study_topic.strip()
        instance.study_contect = instance.study_contect.strip()
        StudyList.objects.filter(pk=list_id, creator_id=request.user.id).update(
            study_topic=instance.study_topic, study_contect=instance.study_contect)

class StudyReviewForm(forms.ModelForm):
    class Meta:
        model = StudyList
        fields = [
            "study_topic",
            "study_contect",
        ]
        widgets ={
            "study_topic":forms.TextInput(attrs={"class" : "form-control",
             "disabled" : True,
             "style" : "width : 150px;"

             }),
            "study_contect":forms.Textarea(attrs={"class" : "form-control",
             "disabled" : True,
            "style" : "height : 570px; width : 1440px; overflow : auto;",
             }),
        }