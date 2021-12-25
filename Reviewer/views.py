from django.shortcuts import render

from Reviewer.form import LoginForm

# Create your views here.


def login_view(requset):
	if requset.method == "POST":
		
	else:
		form = LoginForm()
	return render(requset, "login.html", {"form" : form})