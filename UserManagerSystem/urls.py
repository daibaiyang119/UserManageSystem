"""UserManagerSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login.html', views.login),
    url(r'^logout.html', views.logout),
    url(r'^index.html', views.index),
    url(r'^classes.html', views.handle_classes),
    url(r'^add_classes.html', views.handle_add_classes),
    url(r'^edit_classes.html', views.handle_edit_classes),
    url(r'^up_classes.html', views.handle_up_classes),
    url(r'^del_classes.html', views.handle_del_classes),
    url(r'^students.html', views.handle_students),
    url(r'^add_students.html', views.handle_add_students),
    url(r'^edit_students.html', views.handle_edit_students),
    url(r'^del_students.html', views.handle_del_students),
    url(r'^teachers.html', views.handle_teachers),
    url(r'^add_teachers.html', views.handle_add_teachers),
    url(r'^edit_teachers.html', views.handle_edit_teachers),
    url(r'^del_teachers.html', views.handle_del_teachers),
]
