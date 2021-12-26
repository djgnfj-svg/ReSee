from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from Reviewer.form import LoginForm, RegisterForm
from Reviewer.models import Users
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        form_register = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
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
        form = LoginForm()
    print(request.id)
    return render(request, "login.html", {"form" : form, "msg" : msg})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "잘쳐라 씹라야"
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "가입완료"
        return render(request, "login.html", {"form_register": form, "msg": msg})
    else:
        form = RegisterForm()
    return render(request, "login.html", {"form_register": form})

def logout_view(request):
    logout(request)
    return redirect("")