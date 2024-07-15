from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from GIMMEWeb.core.views import Views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', Views.home, name=''),
    re_path(r'^home/$', Views.home, name='home'),

    re_path(r'^initServer/$', Views.init_server, name='initServer'),
    re_path(r'^simulateReaction/$', Views.simulate_reaction, name='simulateReaction'),

    re_path(r'^dash/$', Views.dash, name='dash'),

    re_path(r'^userRegistration/$', Views.user_registration, name='userRegistration'),
    re_path(r'^userUpdate/$', Views.user_update, name='userUpdate'),
    re_path(r'^userDeletion/$', Views.user_deletion, name='userDeletion'),
    
    re_path(r'^taskRegistration/', Views.taskRegistration, name='taskRegistration'),
    re_path(r'^taskUpdate/', Views.taskUpdate, name='taskUpdate'),
    re_path(r'^taskDeletion/', Views.taskDeletion, name='taskDeletion'),

    re_path(r'^addAllUsersSelected/$', Views.add_all_users_selected, name='addAllUsersSelected'),
    re_path(r'^removeAllUsersSelected/$', Views.remove_all_users_selected, name='removeAllUsersSelected'),
    re_path(r'^addSelectedUser/$', Views.add_selected_user, name='addSelectedUser'),
    re_path(r'^removeSelectedUser/$', Views.remove_selected_user, name='removeSelectedUser'),
    
    re_path(r'^addAllTasksSelected/$', Views.add_all_tasks_selected, name='addAllTasksSelected'),
    re_path(r'^removeAllTasksSelected/$', Views.remove_all_tasks_selected, name='removeAllTasksSelected'),
    re_path(r'^addSelectedTask/$', Views.add_selected_task, name='addSelectedTask'),
    re_path(r'^removeSelectedTask/$', Views.removeSelectedTask, name='removeSelectedTask'),

    re_path(r'^loginCheck/$', Views.login_check, name='loginCheck'),
    re_path(r'^logoutCheck/$', Views.logout_check, name='logoutCheck'),

    re_path(r'^startAdaptation/', Views.startAdaptation, name='startAdaptation'),
    re_path(r'^configAdaptation/', Views.configAdaptation, name='configAdaptation'),

    re_path(r'^startActivity/', Views.startActivity, name='startActivity'),
    re_path(r'^saveTaskResults/', Views.saveTaskResults, name='saveTaskResults'),

    #re_path(r'^questionnaire/', Views.questionnaire, name='questionnaire'),
    re_path(r'^addPersonality/', Views.add_personality, name='addPersonality'),
    re_path(r'^questionnaire/(?P<questionnaire_title>[\w-]+)/$', Views.questionnaire, name='questionnaire'),
    #re_path('questionnaire/<int:questionnaire_id>/$', Views.questionnaire, name='questionnaire'),
    
    re_path(r'^createNewTag/', Views.create_new_tag, name='createNewTag'),
    re_path(r'^deleteTag/', Views.delete_tag, name='deleteTag'),
    re_path(r'^assignTag/', Views.assign_tag, name='assignTag'),
    re_path(r'^selectTag/', Views.select_tag, name='selectTag'),
    re_path(r'^removeAssignedTag/', Views.remove_assigned_tag, name='removeAssignedTag'),
    re_path(r'^randomizeGroupTags/', Views.randomize_group_tags, name='randomizeGroupTags'),

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
    re_path(r'^saveSynergiesTable/', Views.saveSynergiesTable, name='saveSynergiesTable'),

    re_path(r'^resetSimWeek/', Views.resetSimWeek, name='resetSimWeek'),
    re_path(r'^advanceSimWeek/', Views.advanceSimWeek, name='advanceSimWeek'),
    re_path(r'^shareLinkSim/', Views.shareLinkSim, name='shareLinkSim'),
    re_path(r'^taskRegistrationSim/', Views.taskRegistrationSim, name='taskRegistrationSim'),
    re_path(r'^evaluateSim/', Views.evaluateSim, name='evaluateSim'),


    path('admin/', admin.site.urls)



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
