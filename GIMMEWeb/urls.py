from django.contrib import admin
from django.urls import path, re_path
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

    re_path(r'^taskRegistration/', Views.task_registration, name='taskRegistration'),
    re_path(r'^taskUpdate/', Views.task_update, name='taskUpdate'),
    re_path(r'^taskDeletion/', Views.task_deletion, name='taskDeletion'),

    re_path(r'^addAllUsersSelected/$', Views.add_all_users_selected, name='addAllUsersSelected'),
    re_path(r'^removeAllUsersSelected/$', Views.remove_all_users_selected, name='removeAllUsersSelected'),
    re_path(r'^addSelectedUser/$', Views.add_selected_user, name='addSelectedUser'),
    re_path(r'^removeSelectedUser/$', Views.remove_selected_user, name='removeSelectedUser'),

    re_path(r'^addAllTasksSelected/$', Views.add_all_tasks_selected, name='addAllTasksSelected'),
    re_path(r'^removeAllTasksSelected/$', Views.remove_all_tasks_selected, name='removeAllTasksSelected'),
    re_path(r'^addSelectedTask/$', Views.add_selected_task, name='addSelectedTask'),
    re_path(r'^removeSelectedTask/$', Views.remove_selected_task, name='removeSelectedTask'),

    re_path(r'^loginCheck/$', Views.login_check, name='loginCheck'),
    re_path(r'^logoutCheck/$', Views.logout_check, name='logoutCheck'),

    re_path(r'^startAdaptation/', Views.start_adaptation, name='startAdaptation'),
    re_path(r'^configAdaptation/', Views.config_adaptation, name='configAdaptation'),

    re_path(r'^startActivity/', Views.start_activity, name='startActivity'),
    re_path(r'^saveTaskResults/', Views.save_task_results, name='saveTaskResults'),

    # re_path(r'^questionnaire/', Views.questionnaire, name='questionnaire'),
    re_path(r'^addPersonality/', Views.add_personality, name='addPersonality'),
    re_path(r'^questionnaire/(?P<questionnaire_title>[\w-]+)/$', Views.questionnaire, name='questionnaire'),
    # re_path('questionnaire/<int:questionnaire_id>/$', Views.questionnaire, name='questionnaire'),

    re_path(r'^createNewTag/', Views.create_new_tag, name='createNewTag'),
    re_path(r'^deleteTag/', Views.delete_tag, name='deleteTag'),
    re_path(r'^assignTag/', Views.assign_tag, name='assignTag'),
    re_path(r'^selectTag/', Views.select_tag, name='selectTag'),
    re_path(r'^removeAssignedTag/', Views.remove_assigned_tag, name='removeAssignedTag'),
    re_path(r'^randomizeGroupTags/', Views.randomize_group_tags, name='randomizeGroupTags'),

    re_path(r'^fetchServerState/', Views.fetch_server_state, name='fetchServerState'),
    re_path(r'^fetchStudentStates/', Views.fetch_student_states, name='fetchStudentStates'),
    re_path(r'^fetchStudentInfo/', Views.fetch_student_info, name='fetchStudentInfo'),

    re_path(r'^fetchTasksFromId/', Views.fetch_tasks_from_id, name='fetchTasksFromId'),
    re_path(r'^fetchGroupFromId/', Views.fetch_group_from_id, name='fetchGroupFromId'),

    re_path(r'^fetchUserState/', Views.fetch_user_state, name='fetchUserState'),
    re_path(r'^uploadTaskResults/', Views.upload_task_results, name='uploadTaskResults'),

    re_path(r'^manuallyChangeStudentGroup/', Views.manually_change_student_group, name='manuallyChangeStudentGroup'),
    re_path(r'^manuallyManageStudent/', Views.manually_manage_student, name='manuallyManageStudent'),

    re_path(r'^fetchSynergiesTable/', Views.fetch_synergies_table, name='fetchSynergiesTable'),
    re_path(r'^saveSynergiesTable/', Views.save_synergies_table, name='saveSynergiesTable'),

    re_path(r'^resetSimWeek/', Views.reset_sim_week, name='resetSimWeek'),
    re_path(r'^advanceSimWeek/', Views.advance_sim_week, name='advanceSimWeek'),
    re_path(r'^shareLinkSim/', Views.share_link_sim, name='shareLinkSim'),
    re_path(r'^taskRegistrationSim/', Views.task_registration_sim, name='taskRegistrationSim'),
    re_path(r'^evaluateSim/', Views.evaluate_sim, name='evaluateSim'),

    path('admin/', admin.site.urls)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
