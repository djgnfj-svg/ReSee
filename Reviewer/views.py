from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from Reviewer.form import LoginForm, MemberDelForm, MemberModifiForm, RegisterForm
from Reviewer.models import Users
from django.contrib.auth.decorators import login_required

# Create your views here.

@csrf_exempt
def login_register_control_view(request):
    msg = None
    form_login = LoginForm()
    form_register = RegisterForm()
    if request.method == "POST":
        if "register" in request.POST:
            return register_view(request)
        elif "login" in request.POST:
            return login_view(request)
    else:
        return render(request, "login.html", {"form_login" : form_login, "msg" : msg, "form_register" : form_register})

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
                msg = "성공"
                login(request, user)
                return render(request,"home.html")
    else:
        msg = None
        form_login = LoginForm()
    return render(request, "login.html", {"form_login" : form_login, "msg" : msg, "form_register" : form_register})

def register_view(request):
    form_login = LoginForm()
    form_register = RegisterForm()
    msg = None
    if request.method == "POST":
        form_register = RegisterForm(request.POST)
        if form_register.is_valid():
            form_register.save()
            msg = "가입완료"
        return render(request, "login.html", {"form_login" : form_login, "msg" : msg, "form_register" : form_register})
    return render(request, "login.html", {"form_login" : form_login, "msg" : msg, "form_register" : form_register})

def logout_view(request):
    logout(request)
    return redirect("home")

@csrf_exempt
@login_required
def member_modify_view(request):
    form_modify = MemberModifiForm()
    if request.method == "POST":
        form_modify = MemberModifiForm(request.POST)
        if form_modify.is_valid():
            user = request.user
            user.email = request.POST["useremail"]
            user.save()
    else:
        msg = None
    return render(request, "member_modify.html", {"form_modify" : form_modify})
    
@login_required
def setting_view(request):
    return render(request,"setting.html")

@csrf_exempt
@login_required
def member_del_view(request):
    form_del = MemberDelForm()
    if request.method == "POST":
        form_del = MemberDelForm(request.POST)
        print(form_del.errors.as_json())
        if form_del.is_valid():
            user = request.user
            email = request.POST["useremail"]
            raw_password = request.POST["password1"]
            if user.check_password(raw_password):
                user.delete()
                return redirect("home")
    return render(request, "member_del.html", {"form_del" : form_del})
    

def home_view(request):
    return render(request, "home.html")