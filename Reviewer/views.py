from django.contrib.auth import SESSION_KEY, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from Reviewer.form import CateCreateForm, LoginForm, MemberDelForm, MemberModifiForm, RegisterForm, StudyCreateForm, StudyReviewForm
from Reviewer.models import Categories, StudyList, Users
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Reviewer.utils import dateCalculation
# Create your views here.

@csrf_exempt
def login_register_control_view(request):
    msg = None
    form_login = LoginForm()
    form_register = RegisterForm()
    # form_register = None
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

def category_view(request):
    msg = "asdf"
    get_list = Categories.objects.order_by("created_at").filter(created_by_id=request.user.id)
    return render(request, "cate_list.html", {"list" : get_list, "msg":msg})

@login_required
def category_create_view(request):
    msg = None
    if request.method == "POST":
        form = CateCreateForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('category_name')} 생성완료!"
            messages.add_message(request, messages.INFO, msg)
            form.save(request)
            return redirect("cate_list")
        else:
            form =CateCreateForm()
    else:
        form =CateCreateForm()
    return render(request, "cate_create.html", {"form":form})

@login_required
def category_change_view(request, action, category_id):
    if request.method == "POST":
        list_data = Categories.objects.filter(id=category_id)
        if list_data.exists():
            if list_data.first().created_by_id != request.user.id:
                msg = "자신이 소유하지 않은 list 입니다리~~"
            else:
                if action == "delete":
                    msg = f"{list_data.first().category_name} 삭제 완료"
                    list_data.delete()
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = f"{list_data.first().category_name} 수정 완료"
                    form = CateCreateForm(request.POST)
                    form.update_form(request, category_id)
                    messages.add_message(request, messages.INFO, msg)
    elif request.method == "GET" and action == "update":
        list_data = Categories.objects.filter(pk=category_id).first()
        form = CateCreateForm(instance=list_data)
        return render(request, "cate_create.html", {"form" : form, "is_update":True})
    elif request.method == "GET" and action == "study_list":
        return study_list_view(request, category_id)
    return redirect("cate_list")

def study_list_view(request, category_id):
    form = StudyList.objects.order_by("created_at").filter(created_by_id = request.user.id, category_id_id = category_id)
    return render(request, "study_list.html", {"form" : form, "category_id":category_id})

@login_required
def study_create_view(request, category_id):
    msg = None
    if request.method == "POST":
        form = StudyCreateForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('category_name')} 생성완료!"
            messages.add_message(request, messages.INFO, msg)
            temp = Categories.objects.filter(id=category_id).first()
            form.save(request, temp.id)
            return redirect("study_list", category_id)
        else:
            form =StudyCreateForm()
    else:
        form =StudyCreateForm()
    return render(request, "study_create.html", {"form":form})

@login_required
def study_change_view(request, category_id, action, study_id):
    if request.method == "POST":
        list_data = StudyList.objects.filter(id=study_id)
        if list_data.exists():
            if list_data.first().created_by_id != request.user.id:
                msg = "자신이 소유하지 않은 list 입니다리~~"
            else:
                if action == "delete":
                    msg = f"{list_data.first().study_topic} 삭제 완료"
                    list_data.delete()
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = f"{list_data.first().study_topic} 수정 완료"
                    form = StudyCreateForm(request.POST)
                    if form.is_valid():
                        # 복습을 했을경우 이건 업데이트이기때문에 주석함
                        # temp = list_data.get(id=study_id)
                        # temp.review_count_up()
                        form.update_form(request, study_id)
                    else :
                        msg = f"에메함 "
                    print(form.errors.as_json())
                    messages.add_message(request, messages.INFO, msg)
    elif request.method == "GET" and action == "update":
        list_data = StudyList.objects.filter(pk=study_id).first()
        form = StudyCreateForm(instance=list_data)
        return render(request, "study_create.html", {"form" : form, "is_update":True})
    return redirect("study_list", category_id)

# def study_review_check_view(request, category_id):


def study_review_view(request, category_id, study_id):
    base_time = StudyList.objects.filter(pk=category_id).order_by("-created_at").first().created_at
    review_list = dateCalculation(base_time, StudyList)
    try:
        form = StudyReviewForm(instance=review_list[study_id])
    except IndexError:
        messages.add_message(request, messages.INFO, "복습할 껀덕지가 없다 이말이야")
        return redirect("cate_list")
    else:
        return render(request, "study_review.html", {"form" : form, "study_id" : study_id})