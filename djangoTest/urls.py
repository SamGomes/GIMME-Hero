from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from djangoTest.core.views import Views

urlpatterns = [
    re_path(r'^$', Views.home, name=""),
    re_path(r'^home/$', Views.home, name="home"),
    re_path(r'^login/$', Views.login, name="login"),
    re_path(r'^dash/$', Views.dash, name="dash"),
    re_path(r'^registration/$', Views.registration, name="registration"),
    re_path(r'^saveRegistration/$', Views.saveRegistration, name="saveRegistration"),
    re_path(r'^newTask/$', Views.newTask, name="newTask"),
]