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
from django.urls import include, path

from Reviewer.views import(
    home_view, 
    login_register_control_view, 
    logout_view, 
    member_del_view, 
    member_modify_view, 
    register_view, 
    setting_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("login", login_register_control_view, name="login"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('setting',setting_view,name="setting"),
    path('member_modify/', member_modify_view, name="member_modify"),
    path('member_del/', member_del_view, name="member_del"),
    path("category_list/", include("Reviewer.category_list.urls")),
]
