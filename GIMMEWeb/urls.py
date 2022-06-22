from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from GIMMEWeb.core.views import Views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', Views.home, name=''),
    re_path(r'^home/$', Views.home, name='home'),

    re_path(r'^initServer/$', Views.initServer, name='initServer'),
    re_path(r'^simulateReaction/$', Views.simulateReaction, name='simulateReaction'),

    re_path(r'^dash/$', Views.dash, name='dash'),

    re_path(r'^userRegistration/$', Views.userRegistration, name='userRegistration'),
    re_path(r'^userUpdate/$', Views.userUpdate, name='userUpdate'),
    re_path(r'^userDeletion/$', Views.userDeletion, name='userDeletion'),
    
    re_path(r'^taskRegistration/', Views.taskRegistration, name='taskRegistration'),
    re_path(r'^taskUpdate/', Views.taskUpdate, name='taskUpdate'),
    re_path(r'^taskDeletion/', Views.taskDeletion, name='taskDeletion'),

    re_path(r'^addAllUsersSelected/$', Views.addAllUsersSelected, name='addAllUsersSelected'),
    re_path(r'^removeAllUsersSelected/$', Views.removeAllUsersSelected, name='removeAllUsersSelected'),
    re_path(r'^addSelectedUser/$', Views.addSelectedUser, name='addSelectedUser'),
    re_path(r'^removeSelectedUser/$', Views.removeSelectedUser, name='removeSelectedUser'),
    
    re_path(r'^addAllTasksSelected/$', Views.addAllTasksSelected, name='addAllTasksSelected'),
    re_path(r'^removeAllTasksSelected/$', Views.removeAllTasksSelected, name='removeAllTasksSelected'),
    re_path(r'^addSelectedTask/$', Views.addSelectedTask, name='addSelectedTask'),
    re_path(r'^removeSelectedTask/$', Views.removeSelectedTask, name='removeSelectedTask'),

    re_path(r'^loginCheck/$', Views.loginCheck, name='loginCheck'),
    re_path(r'^logoutCheck/$', Views.logoutCheck, name='logoutCheck'),

    re_path(r'^startAdaptation/', Views.startAdaptation, name='startAdaptation'),
    re_path(r'^configAdaptation/', Views.configAdaptation, name='configAdaptation'),

    re_path(r'^startActivity/', Views.startActivity, name='startActivity'),
    re_path(r'^saveTaskResults/', Views.saveTaskResults, name='saveTaskResults'),

    
    re_path(r'^fetchServerState/', Views.fetchServerState, name='fetchServerState'),
    re_path(r'^fetchStudentStates/', Views.fetchStudentStates, name='fetchStudentStates'),
    re_path(r'^fetchStudentInfo/', Views.fetchStudentInfo, name='fetchStudentInfo'),

    re_path(r'^fetchTasksFromId/', Views.fetchTasksFromId, name='fetchTasksFromId'),
    re_path(r'^fetchGroupFromId/', Views.fetchGroupFromId, name='fetchGroupFromId'),

    re_path(r'^fetchUserState/', Views.fetchUserState, name='fetchUserState'),
    re_path(r'^uploadTaskResults/', Views.uploadTaskResults, name='uploadTaskResults'),
    
    re_path(r'^manuallyChangeStudentGroup/', Views.manuallyChangeStudentGroup, name='manuallyChangeStudentGroup'),
    re_path(r'^manuallyManageStudent/', Views.manuallyManageStudent, name='manuallyManageStudent'),
    
    
    re_path(r'^fetchSynergiesTable/', Views.fetchSynergiesTable, name='fetchSynergiesTable'),
    re_path(r'^saveSynergiesTable/', Views.saveSynergiesTable, name='saveSynergiesTable')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
