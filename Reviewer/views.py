from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from Reviewer.form import LoginForm
from Reviewer.models import Users
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
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
    print(msg)
    return render(request, "login.html", {"form" : form, "msg" : msg})

def logout_view(request):
    logout(request)
    return redirect("")