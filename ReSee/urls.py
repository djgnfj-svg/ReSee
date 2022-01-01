"""ReSee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Reviewer.views import category_change_view, category_view, category_create_view, home_view, login_register_control_view, logout_view, member_del_view, member_modify_view, register_view, study_change_view, study_create_view, study_list_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login", login_register_control_view, name="login"),
    path('register/', register_view, name="register"),
    path("", home_view, name="home"),
    path('logout/', logout_view, name="logout"),
    path('member_modify/', member_modify_view, name="member_modify"),
    path('member_del/', member_del_view, name="member_del"),
    path("category_list/",category_view,name="cate_list"),
    path("category_list/create/",category_create_view,name="cate_create"),
    path("category_list/<str:action>/<int:category_id>",category_change_view,name="cate_change"),
    path("category_list/<int:category_id>/study_list/",study_list_view,name="study_list"),
    path("category_list/<int:category_id>/study_list/create/",study_create_view,name="study_create"),
    path("category_list/<int:category_id>/study_list/<str:action>/<int:study_id>",
        study_change_view,name="study_change"),
]
