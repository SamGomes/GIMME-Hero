from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from GIMMEWeb.core.views import Views

urlpatterns = [
    re_path(r'^$', Views.home, name=""),
    re_path(r'^home/$', Views.home, name="home"),
    re_path(r'^logout/$', Views.logout, name="logout"),

    re_path(r'^dash/$', Views.dash, name="dash"),

    re_path(r'^playerRegistration/$', Views.playerRegistration, name="playerRegistration"),
    re_path(r'^taskRegistration/', Views.taskRegistration, name="taskRegistration"),

    re_path(r'^saveUserRegistration/$', Views.saveUserRegistration, name="saveUserRegistration"),
    re_path(r'^saveTaskRegistration/$', Views.saveTaskRegistration, name="saveTaskRegistration"),

    re_path(r'^addAllPlayersWaiting/$', Views.addAllPlayersWaiting, name="addAllPlayersWaiting"),
    re_path(r'^removeAllPlayersWaiting/$', Views.removeAllPlayersWaiting, name="removeAllPlayersWaiting"),
    re_path(r'^addWaitingPlayer/$', Views.addWaitingPlayer, name="addWaitingPlayer"),
    re_path(r'^removeWaitingPlayer/$', Views.removeWaitingPlayer, name="removeWaitingPlayer"),
    
    re_path(r'^loginCheck/$', Views.loginCheck, name="loginCheck"),
    re_path(r'^startAdaptation/', Views.startAdaptation, name="startAdaptation"),
    re_path(r'^configAdaptation/', Views.configAdaptation, name="configAdaptation"),

    re_path(r'^startActivity/', Views.startActivity, name="startActivity"),
    re_path(r'^saveTaskResults/', Views.saveTaskResults, name="saveTaskResults"),

    
    re_path(r'^fetchServerState/', Views.fetchServerState, name="fetchServerState"),
    re_path(r'^fetchPlayerState/', Views.fetchPlayerState, name="fetchPlayerState"),
]