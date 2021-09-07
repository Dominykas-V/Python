"""KaleduKorteles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import django
from django.contrib import admin
from django.urls import path, include
from main import views as mv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('', mv.LogIn, name="LogIn"),
    path('login/', mv.LogIn, name="LogIn"),
    path('rinkimas/', mv.Rinkimas, name="Rinkimas"),

    path('adminlogin/', mv.AdminLogIn, name="AdminLogIn"),
    path('adminpanel/', mv.AdminPanel, name="AdminPanel"),

    path('acc/', include("django.contrib.auth.urls")),

    
    path('testhtml/', mv.testhtml, name="testhtml"),
]
