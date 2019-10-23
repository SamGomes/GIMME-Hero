from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from djangoTest.core.views import Views

urlpatterns = [
    re_path(r'^$', Views.home, name=""),
    re_path(r'^home/$', Views.home, name="home"),
    re_path(r'^login/$', Views.login, name="login"),
    re_path(r'^logout/$', Views.logout, name="logout"),

    re_path(r'^dash/$', Views.dash, name="dash"),

    re_path(r'^registerUser/$', Views.registerUser, name="registerUser"),
    re_path(r'^registerTask/', Views.registerTask, name="registerTask"),

    re_path(r'^saveUserRegistration/$', Views.saveUserRegistration, name="saveUserRegistration"),
    re_path(r'^saveTaskRegistration/$', Views.saveTaskRegistration, name="saveTaskRegistration"),

    re_path(r'^newAvailablePlayer/$', Views.newAvailablePlayer, name="newAvailablePlayer"),
    re_path(r'^loginCheck/$', Views.loginCheck, name="loginCheck"),
    re_path(r'^startAdaptation/', Views.startAdaptation, name="startAdaptation"),

    re_path(r'^displayTask/', Views.displayTask, name="displayTask"),
    re_path(r'^saveTaskResults/', Views.saveTaskResults, name="saveTaskResults"),
]