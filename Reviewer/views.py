from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render

from Reviewer.form import LoginForm, RegisterForm
from Reviewer.models import Users
# Create your views here.

@csrf_exempt
def login_view(request):
    form_register = RegisterForm()
    if request.method == "POST":
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            email = form_login.cleaned_data.get("email")
            raw_password = form_login.cleaned_data.get("password")
            msg = "가입되있지 않거나 키보드를 사야할지도 모릅니다."
        try :
            user = Users.objects.get(email=email)	
        except Users.DoesNotExist:
            pass
        else :
            if user.check_password(raw_password):
                msg = None
                login(request, user)
    else:
        msg = None
        form_login = LoginForm()
    
    return render(request, "login.html", {"form_login" : form_login, "msg" : msg, "form_register" : form_register})

def register_view(request):
    if request.method == "POST":
        form_register = RegisterForm(request.POST)
        msg = "잘쳐라 씹라야"
        if form_register.is_valid():
            form_register.save()
            username = form_register.cleaned_data.get("username")
            raw_password = form_register.cleaned_data.get("password1")
            useremail = form_register.cleaned_data.get("useremail")
            user = authenticate(username=username, password=raw_password, useremail=useremail)
            login(request, user)
            msg = "가입완료"
        return render(request, "login.html", {"form_register": form_register, "msg": msg})
    return redirect("login")

def logout_view(request):
    logout(request)
    return redirect("")

def home_view(request):
    return render(request, "home.html")