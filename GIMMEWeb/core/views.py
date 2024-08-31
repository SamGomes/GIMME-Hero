import os
import json

import string

from datetime import date, time, timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages

from GIMMEWeb.core.models import UserProfile
from GIMMEWeb.core.models import Task
from GIMMEWeb.core.models import Tag
from GIMMEWeb.core.models import Questionnaire, LikertResponse, Submission, QuestionnaireType
from GIMMEWeb.core.models import ServerState
from GIMMEWeb.core.forms import CreateUserForm, CreateUserProfileForm, CreateTaskForm, UpdateUserForm, \
    UpdateUserProfileForm, UpdateTaskForm, UpdateUserPersonalityForm, LikertForm, CreateTagForm
from GIMMEWeb.core import OEJTS_questionnaire

from GIMMECore import *


class ServerStateModelBridge:

    def get_curr_adaptation_state(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_adaptation_state = json.loads(server_state.curr_adaptation_state)
        return curr_adaptation_state

    def is_ready_for_new_activity(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        ready_for_new_activity = json.loads(server_state.ready_for_new_activity)
        return ready_for_new_activity

    def get_curr_selected_users(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_selected_users = json.loads(server_state.curr_selected_users)
        return curr_selected_users

    def get_curr_free_users(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_free_users = json.loads(server_state.curr_free_users)
        return curr_free_users

    def get_curr_selected_tasks(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_selected_tasks = json.loads(server_state.curr_selected_tasks)
        return curr_selected_tasks

    def get_curr_free_tasks(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_free_tasks = json.loads(server_state.curr_free_tasks)
        return curr_free_tasks

    def get_simulation_week(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.simulation_week

    def get_sim_simulate_reaction(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.sim_simulate_reaction

    def get_sim_week_one_users_evaluated(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.sim_week_one_users_evaluated

    def get_sim_student_x(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.sim_student_x

    def get_sim_student_y(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.sim_student_y

    def get_sim_student_w(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.sim_student_w

    def get_sim_student_z(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.sim_student_z

    def get_sim_flags(self):
        server_state = ServerState.objects.first()
        server_state_sim_data = {
            "simIsLinkShared": server_state.sim_is_link_shared,
            "simIsTaskCreated": server_state.sim_is_task_created,
            "simWeekOneUsersEvaluated": server_state.sim_week_one_users_evaluated,
            "simSimulateReaction": server_state.sim_simulate_reaction,
            "simWeekFourDoneOnce": server_state.sim_week_four_done_once,
            "simWeek": server_state.simulation_week,
            "simStudentToEvaluate": server_state.sim_student_to_evaluate,
            "simUnavailableStudent": server_state.sim_unavailable_student,
            "simStudentX": server_state.sim_student_x,
            "simStudentY": server_state.sim_student_y,
            "simStudentW": server_state.sim_student_w,
            "simStudentZ": server_state.sim_student_z,
        }
        return server_state_sim_data

    def set_curr_adaptation_state(self, curr_adaptation_state):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_adaptation_state = json.dumps(curr_adaptation_state, default=lambda o: o.__dict__, sort_keys=True)
            server_state.curr_adaptation_state = curr_adaptation_state
        server_state.save()

    def set_ready_for_new_activity(self, ready_for_new_activity):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            ready_for_new_activity = json.dumps(ready_for_new_activity, default=lambda o: o.__dict__, sort_keys=True)
            server_state.ready_for_new_activity = ready_for_new_activity
        server_state.save()

    def set_curr_selected_users(self, curr_selected_users):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_selected_users = json.dumps(curr_selected_users, default=lambda o: o.__dict__, sort_keys=True)
            server_state.curr_selected_users = curr_selected_users
        server_state.save()

    def set_curr_free_users(self, curr_free_users):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_free_users = json.dumps(curr_free_users, default=lambda o: o.__dict__, sort_keys=True)
            server_state.curr_free_users = curr_free_users
        server_state.save()

    def set_curr_selected_tasks(self, curr_selected_tasks):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_selected_tasks = json.dumps(curr_selected_tasks, default=lambda o: o.__dict__, sort_keys=True)
            server_state.curr_selected_tasks = curr_selected_tasks
        server_state.save()

    def set_curr_free_tasks(self, curr_free_tasks):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_free_tasks = json.dumps(curr_free_tasks, default=lambda o: o.__dict__, sort_keys=True)
            server_state.curr_free_tasks = curr_free_tasks
        server_state.save()

    def set_sim_is_link_shared(self, sim_is_link_shared):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_is_link_shared = sim_is_link_shared
        server_state.save()

    def set_sim_is_task_created(self, sim_is_task_created):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_is_task_created = sim_is_task_created
        server_state.save()

    def set_sim_week_one_users_evaluated(self, sim_week_one_users_evaluated):
        server_state = ServerState.objects.first()
        if server_state == None:
            server_state = ServerState()
        else:
            server_state.sim_week_one_users_evaluated = sim_week_one_users_evaluated
        server_state.save()

    def set_sim_simulate_reaction(self, sim_simulate_reaction):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_simulate_reaction = sim_simulate_reaction
        server_state.save()

    def set_sim_week_four_done_once(self, sim_week_four_done_once):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_week_four_done_once = sim_week_four_done_once
        server_state.save()

    def set_simulation_week(self, simulation_week):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simulation_week = simulation_week
        server_state.save()

    def set_sim_student_to_evaluate(self, sim_student_to_evaluate):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_student_to_evaluate = sim_student_to_evaluate
        server_state.save()

    def set_sim_unavailable_student(self, sim_unavailable_student):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_unavailable_student = sim_unavailable_student
        server_state.save()

    def set_sim_student_x(self, sim_student_x):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_student_x = sim_student_x
        server_state.save()

    def set_sim_student_y(self, sim_student_y):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_student_y = sim_student_y
        server_state.save()

    def set_sim_student_z(self, sim_student_z):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_student_z = sim_student_z
        server_state.save()

    def set_sim_student_w(self, sim_student_w):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.sim_student_w = sim_student_w
        server_state.save()

    def get_tags(self, target):
        tags = list(Tag.objects.filter(target=target))
        return tags


server_state_model_bridge = ServerStateModelBridge()


class CustomTaskModelBridge(TaskModelBridge):

    def save_task(self, task):
        task.save()

    def get_task(self, task_id):
        return Task.objects.get(task_id=task_id)

    def remove_task(self, task_id):
        task = Task.objects.get(task_id=task_id)
        task.delete()

    def get_all_task_ids(self):  # all tasks for adaptation
        return server_state_model_bridge.get_curr_selected_tasks()

    def get_all_stored_task_ids(self):
        all_tasks = Task.objects.all()
        all_tasks_ids = []
        for task in all_tasks:
            all_tasks_ids.append(str(task.task_id))
        return all_tasks_ids

    def get_task_interactions_profile(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return InteractionsProfile(dimensions=json.loads(task.profile)['dimensions'])

    def get_min_task_required_ability(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return float(task.min_req_ability)

    def get_min_task_duration(self, task_id):
        pass

    def get_task_difficulty_weight(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return float(task.difficulty_weight)

    def get_task_profile_weight(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return float(task.profile_weight)

    def get_task_diversity_weight(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return float(task.diversity)

    def get_task_init_date(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return task.init_date

    def get_task_final_date(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return task.final_date

    def get_task_file_paths(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return task.filePaths

    def get_task_tags(self, task_id):
        tags = list(Task.objects.get(task_id=task_id).tags.all())
        return tags

    def add_task_tag(self, task_id, tag_name):
        try:
            task = Task.objects.get(task_id=task_id)
            tag = Tag.objects.get(name=tag_name, target='task')
            task.tags.add(tag)
            task.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def remove_task_tag(self, task_id, tag_name):
        try:
            task = Task.objects.get(task_id=task_id)
            tag = Tag.objects.get(name=tag_name, target='task')
            task.tags.remove(tag)
            task.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None


task_bridge = CustomTaskModelBridge()


class CustomPlayerModelBridge(PlayerModelBridge):

    def get_player(self, username):
        return User.objects.get(username=username).userprofile

    def set_and_save_player_state_to_data_frame(self, username, new_state):
        # print(json.dumps(newState,default=lambda o: o.__dict__, sort_keys=True))
        self.set_player_characteristics(username, new_state.characteristics)
        self.set_player_profile(username, new_state.profile)

        player_states_data_frame = self.get_player_states_data_frame(username)
        player_states_data_frame.push_to_data_frame(new_state)

        player_info = User.objects.get(username=username).userprofile
        player_info.past_model_increases_data_frame = json.dumps(player_states_data_frame, default=lambda o: o.__dict__)
        player_info.save()

    def reset_player(self, username):
        return 0

    def get_all_player_ids(self):  # all players for adaptation
        return server_state_model_bridge.get_curr_selected_users()

    def get_all_stored_student_usernames(self):
        all_users = UserProfile.objects.all()
        all_user_ids = []
        for userprofile in all_users:
            if 'Student' in userprofile.role:
                all_user_ids.append(userprofile.user.username)
        return all_user_ids

    def get_player_name(self, username):
        try:
            player = User.objects.get(username=username)
            return player.username
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_email(self, username):
        try:
            player = User.objects.get(username=username)
            return player.email
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_curr_profile(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            # print(json.dumps(player, default= lambda o: o.__dict__, sort_keys=True))
            profile = json.loads(player_info.curr_state)['profile']
            profile = InteractionsProfile(dimensions=profile['dimensions'])
            return profile
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_personality(self, username) -> PlayerPersonality:
        try:
            profile = User.objects.get(username=username).userprofile
            personality = json.loads(profile.personality)

            # TODO add personality model verification
            # if personalityModel == 'MBTI':
            # 	if len(personalityType) != 4:
            # 		return None  # exception if the personality type is not 4 characters long
            if personality and type(personality) is dict:
                return PersonalityMBTI(personality['letter1'], personality['letter2'], personality['letter3'],
                                       personality['letter4'])

        except UserProfile.DoesNotExist:
            # Handle the case when the UserProfile doesn't exist or "personality" is missing
            personality = {}
        except json.JSONDecodeError:
            # Handle the case when the JSON decoding fails (invalid JSON format)
            personality = None

        return None

    def get_player_curr_group(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            group = json.loads(player_info.curr_state)['group']
            return group
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_curr_tasks(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            tasks = json.loads(player_info.curr_state)['tasks']
            return tasks
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_states_data_frame(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            past_data_frame = json.loads(player_info.past_data_frame)

            states = []
            for state in past_data_frame['states']:
                characteristics = state['characteristics']
                characteristics = PlayerCharacteristics(
                    ability=float(characteristics['ability']),
                    engagement=float(characteristics['engagement']))

                profile = state['profile']
                profile = InteractionsProfile(dimensions=profile['dimensions'])

                player_state = PlayerState(profile=profile,
                                           characteristics=characteristics,
                                           dist=state['dist'],
                                           quality=state['quality'])

                player_state.creationTime = -1
                states.append(player_state)

            trim_alg = json.loads(json.dumps(past_data_frame['trim_alg']))
            sdf = PlayerStatesDataFrame(
                states=states,
                interactions_profile_template=int_prof_template.generate_copy().reset(),
                trim_alg=ProximitySortPlayerDataTrimAlg(
                    max_num_model_elements=int(trim_alg['_max_num_model_elements']),
                    epsilon=float(trim_alg['_ProximitySortPlayerDataTrimAlg__epsilon'])
                )
            )
            return sdf
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_curr_characteristics(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            characteristics = json.loads(player_info.curr_state)['characteristics']
            return PlayerCharacteristics(ability=float(characteristics['ability']),
                                         engagement=float(characteristics['engagement']))
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_grade(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            return player_info.grade
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_preferences_est(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            preferences = json.loads(player_info.preferences)
            preferences = InteractionsProfile(dimensions=preferences['dimensions'])
            return preferences
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_curr_state(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            curr_state = json.loads(player_info.curr_state)
            return PlayerState(profile=self.get_player_curr_profile(username),
                               characteristics=self.get_player_curr_characteristics(username),
                               dist=curr_state['dist'],
                               quality=curr_state['quality'],
                               group=curr_state['group'],
                               tasks=curr_state['tasks'])
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_full_name(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            return player_info.fullname
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def reset_player_curr_state(self, username):
        try:
            player_info = User.objects.get(username=username).userprofile
            new_state = PlayerState()
            player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def reset_player_past_model_increases(self, username):
        try:
            player_states_data_frame = self.get_player_states_data_frame(username)

            self.set_player_characteristics(username, PlayerCharacteristics())
            self.set_player_profile(username, int_prof_template.generate_copy())

            player_states_data_frame.reset()

            player_info = User.objects.get(username=username).userprofile
            player_info.past_model_increases_data_frame = json.dumps(player_states_data_frame,
                                                                     default=lambda o: o.__dict__)
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def set_player_preferences_est(self, username, preferences):
        try:
            player_info = User.objects.get(username=username).userprofile
            player_info.preferences = json.dumps(preferences, default=lambda o: o.__dict__)
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def set_player_characteristics(self, username, characteristics):
        try:
            player_info = User.objects.get(username=username).userprofile
            new_state = self.get_player_curr_state(username)
            new_state.characteristics = characteristics
            player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def set_player_personality(self, username, personality):
        try:
            player_info = User.objects.get(username=username).userprofile
            personality_dict = {"letter1": personality[0],
                                "letter2": personality[1],
                                "letter3": personality[2],
                                "letter4": personality[3], }

            player_info.personality = json.dumps(personality_dict, default=lambda o: o.__dict__)

            try:
                player_info.tags.add(Tag.objects.get(name=personality[0]))
                player_info.tags.add(Tag.objects.get(name=personality[1]))
                player_info.tags.add(Tag.objects.get(name=personality[2]))
                player_info.tags.add(Tag.objects.get(name=personality[3]))
            except Tag.DoesNotExist:
                print("Couldn't add default personality tags")
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def set_player_grade(self, username, grade):
        try:
            player_info = User.objects.get(username=username).userprofile
            player_info.grade = grade
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def set_player_profile(self, username, profile):
        try:
            player_info = User.objects.get(username=username).userprofile
            new_state = self.get_player_curr_state(username)
            new_state.profile = profile
            player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def set_player_group(self, username, group):
        try:
            player_info = User.objects.get(username=username).userprofile
            new_state = self.get_player_curr_state(username)
            new_state.group = group
            player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def set_player_tasks(self, username, tasks):
        try:
            player_info = User.objects.get(username=username).userprofile
            new_state = self.get_player_curr_state(username)
            new_state.tasks = tasks
            player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
            player_info.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def add_player_tag(self, username, tag_name):
        try:
            userprofile = User.objects.get(username=username).userprofile
            tag = Tag.objects.get(name=tag_name, target='student')
            userprofile.tags.add(tag)
            userprofile.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def remove_player_tag(self, username, tag_name):
        try:
            userprofile = User.objects.get(username=username).userprofile
            tag = Tag.objects.get(name=tag_name, target='student')
            userprofile.tags.remove(tag)
            userprofile.save()
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None

    def get_player_tags(self, username):
        try:
            userprofile = User.objects.get(username=username).userprofile
            tags = list(userprofile.tags.all())
            return tags
        except UserProfile.DoesNotExist:
            pass
        except json.JSONDecodeError:
            pass
        return None


player_bridge = CustomPlayerModelBridge()
curr_config_params = {}

int_prof_template = InteractionsProfile({'Challenge': 0, 'Focus': 0})
trim_alg_template = ProximitySortPlayerDataTrimAlg(
    max_num_model_elements=10,
    epsilon=0.05
)

defaultConfigsAlg = RandomConfigsGenAlg(
    player_model_bridge=player_bridge,
    interactions_profile_template=int_prof_template.generate_copy(),
    preferred_num_players_per_group=4)

# cannot call any model bridge so that if models are reset the migrations are not compromised
adaptation = Adaptation(name='GIMME',
                        configs_gen_alg=defaultConfigsAlg)

# sim stuff

# {'csrfmiddlewaretoken': ['3GuQuFgTG1tPLHK0bvD4kO5H0c4F2keftFkiQRIcpyDbrxlEEWmjazhfmCEx0p80'], 'username': ['s17'], 
# 'role': ['Student'], 'email': ['s17@s17.com'], 'password1': ['VW8fiAUkGs7QLwn'], 'password2': ['VW8fiAUkGs7QLwn'], 
# 'fullName': ['s17'], 'age': ['20'], 'gender': ['Male'], 'description': ['.'], 'Create User': ['Register']}
role = 'Student'
password = 'VW8fiAUkGs7QLwn'
age = '20'
description = '.'
createUser = 'Register'

names = ['Abbott', 'Acevedo', 'Acosta', 'Adams', 'Adkins', 'Aguilar', 'Aguirre', 'Albert', 'Alexander', 'Alford',
         'Allen', 'Allison', 'Alston', 'Alvarado', 'Alvarez', 'Anderson', 'Andrews', 'Anthony', 'Armstrong', 'Arnold',
         'Ashley', 'Atkins', 'Atkinson', 'Austin', 'Avery', 'Avila', 'Ayala', 'Ayers', 'Bailey', 'Baird', 'Baker',
         'Baldwin', 'Ball', 'Ballard', 'Banks', 'Barber', 'Barker', 'Barlow', 'Barnes', 'Barnett', 'Barr', 'Barrera',
         'Barrett', 'Barron', 'Barry', 'Bartlett', 'Barton', 'Bass', 'Bates', 'Battle', 'Bauer', 'Baxter', 'Beach',
         'Bean', 'Beard', 'Beasley', 'Beck', 'Becker', 'Bell', 'Bender', 'Benjamin', 'Bennett', 'Benson', 'Bentley',
         'Benton', 'Berg', 'Berger', 'Bernard', 'Berry', 'Best', 'Bird', 'Bishop', 'Black', 'Blackburn', 'Blackwell',
         'Blair', 'Blake', 'Blanchard', 'Blankenship', 'Blevins', 'Bolton', 'Bond', 'Bonner', 'Booker', 'Boone',
         'Booth', 'Bowen', 'Bowers', 'Bowman', 'Boyd', 'Boyer', 'Boyle', 'Bradford', 'Bradley', 'Bradshaw', 'Brady',
         'Branch', 'Bray', 'Brennan', 'Brewer', 'Bridges', 'Briggs', 'Bright', 'Britt', 'Brock', 'Brooks', 'Brown',
         'Browning', 'Bruce', 'Bryan', 'Bryant', 'Buchanan', 'Buck', 'Buckley', 'Buckner', 'Bullock', 'Burch',
         'Burgess', 'Burke', 'Burks', 'Burnett', 'Burns', 'Burris', 'Burt', 'Burton', 'Bush', 'Butler', 'Byers', 'Byrd',
         'Cabrera', 'Cain', 'Calderon', 'Caldwell', 'Calhoun', 'Callahan', 'Camacho', 'Cameron', 'Campbell', 'Campos',
         'Cannon', 'Cantrell', 'Cantu', 'Cardenas', 'Carey', 'Carlson', 'Carney', 'Carpenter', 'Carr', 'Carrillo',
         'Carroll', 'Carson', 'Carter', 'Carver', 'Case', 'Casey', 'Cash', 'Castaneda', 'Castillo', 'Castro',
         'Cervantes', 'Chambers', 'Chan', 'Chandler', 'Chaney', 'Chang', 'Chapman', 'Charles', 'Chase', 'Chavez',
         'Chen', 'Cherry', 'Christensen', 'Christian', 'Church', 'Clark', 'Clarke', 'Clay', 'Clayton', 'Clements',
         'Clemons', 'Cleveland', 'Cline', 'Cobb', 'Cochran', 'Coffey', 'Cohen', 'Cole', 'Coleman', 'Collier', 'Collins',
         'Colon', 'Combs', 'Compton', 'Conley', 'Conner', 'Conrad', 'Contreras', 'Conway', 'Cook', 'Cooke', 'Cooley',
         'Cooper', 'Copeland', 'Cortez', 'Cote', 'Cotton', 'Cox', 'Craft', 'Craig', 'Crane', 'Crawford', 'Crosby',
         'Cross', 'Cruz', 'Cummings', 'Cunningham', 'Curry', 'Curtis', 'Dale', 'Dalton', 'Daniel', 'Daniels',
         'Daugherty', 'Davenport', 'David', 'Davidson', 'Davis', 'Dawson', 'Day', 'Dean', 'Decker', 'Dejesus',
         'Delacruz', 'Delaney', 'Deleon', 'Delgado', 'Dennis', 'Diaz', 'Dickerson', 'Dickson', 'Dillard', 'Dillon',
         'Dixon', 'Dodson', 'Dominguez', 'Donaldson', 'Donovan', 'Dorsey', 'Dotson', 'Douglas', 'Downs', 'Doyle',
         'Drake', 'Dudley', 'Duffy', 'Duke', 'Duncan', 'Dunlap', 'Dunn', 'Duran', 'Durham', 'Dyer', 'Eaton', 'Edwards',
         'Elliott', 'Ellis', 'Ellison', 'Emerson', 'England', 'English', 'Erickson', 'Espinoza', 'Estes', 'Estrada',
         'Evans', 'Everett', 'Ewing', 'Farley', 'Farmer', 'Farrell', 'Faulkner', 'Ferguson', 'Fernandez', 'Ferrell',
         'Fields', 'Figueroa', 'Finch', 'Finley', 'Fischer', 'Fisher', 'Fitzgerald', 'Fitzpatrick', 'Fleming',
         'Fletcher', 'Flores', 'Flowers', 'Floyd', 'Flynn', 'Foley', 'Forbes', 'Ford', 'Foreman', 'Foster', 'Fowler',
         'Fox', 'Francis', 'Franco', 'Frank', 'Franklin', 'Franks', 'Frazier', 'Frederick', 'Freeman', 'French',
         'Frost', 'Fry', 'Frye', 'Fuentes', 'Fuller', 'Fulton', 'Gaines', 'Gallagher', 'Gallegos', 'Galloway', 'Gamble',
         'Garcia', 'Gardner', 'Garner', 'Garrett', 'Garrison', 'Garza', 'Gates', 'Gay', 'Gentry', 'George', 'Gibbs',
         'Gibson', 'Gilbert', 'Giles', 'Gill', 'Gillespie', 'Gilliam', 'Gilmore', 'Glass', 'Glenn', 'Glover', 'Goff',
         'Golden', 'Gomez', 'Gonzales', 'Gonzalez', 'Good', 'Goodman', 'Goodwin', 'Gordon', 'Gould', 'Graham', 'Grant',
         'Graves', 'Gray', 'Green', 'Greene', 'Greer', 'Gregory', 'Griffin', 'Griffith', 'Grimes', 'Gross', 'Guerra',
         'Guerrero', 'Guthrie', 'Gutierrez', 'Guy', 'Guzman', 'Hahn', 'Hale', 'Haley', 'Hall', 'Hamilton', 'Hammond',
         'Hampton', 'Hancock', 'Haney', 'Hansen', 'Hanson', 'Hardin', 'Harding', 'Hardy', 'Harmon', 'Harper', 'Harrell',
         'Harrington', 'Harris', 'Harrison', 'Hart', 'Hartman', 'Harvey', 'Hatfield', 'Hawkins', 'Hayden', 'Hayes',
         'Haynes', 'Hays', 'Head', 'Heath', 'Hebert', 'Henderson', 'Hendricks', 'Hendrix', 'Henry', 'Hensley', 'Henson',
         'Herman', 'Hernandez', 'Herrera', 'Herring', 'Hess', 'Hester', 'Hewitt', 'Hickman', 'Hicks', 'Higgins', 'Hill',
         'Hines', 'Hinton', 'Hobbs', 'Hodge', 'Hodges', 'Hoffman', 'Hogan', 'Holcomb', 'Holden', 'Holder', 'Holland',
         'Holloway', 'Holman', 'Holmes', 'Holt', 'Hood', 'Hooper', 'Hoover', 'Hopkins', 'Hopper', 'Horn', 'Horne',
         'Horton', 'House', 'Houston', 'Howard', 'Howe', 'Howell', 'Hubbard', 'Huber', 'Hudson', 'Huff', 'Huffman',
         'Hughes', 'Hull', 'Humphrey', 'Hunt', 'Hunter', 'Hurley', 'Hurst', 'Hutchinson', 'Hyde', 'Ingram', 'Irwin',
         'Jackson', 'Jacobs', 'Jacobson', 'James', 'Jarvis', 'Jefferson', 'Jenkins', 'Jennings', 'Jensen', 'Jimenez',
         'Johns', 'Johnson', 'Johnston', 'Jones', 'Jordan', 'Joseph', 'Joyce', 'Joyner', 'Juarez', 'Justice', 'Kane',
         'Kaufman', 'Keith', 'Keller', 'Kelley', 'Kelly', 'Kemp', 'Kennedy', 'Kent', 'Kerr', 'Key', 'Kidd', 'Kim',
         'King', 'Kinney', 'Kirby', 'Kirk', 'Kirkland', 'Klein', 'Kline', 'Knapp', 'Knight', 'Knowles', 'Knox', 'Koch',
         'Kramer', 'Lamb', 'Lambert', 'Lancaster', 'Landry', 'Lane', 'Lang', 'Langley', 'Lara', 'Larsen', 'Larson',
         'Lawrence', 'Lawson', 'Le', 'Leach', 'Leblanc', 'Lee', 'Leon', 'Leonard', 'Lester', 'Levine', 'Levy', 'Lewis',
         'Lindsay', 'Lindsey', 'Little', 'Livingston', 'Lloyd', 'Logan', 'Long', 'Lopez', 'Lott', 'Love', 'Lowe',
         'Lowery', 'Lucas', 'Luna', 'Lynch', 'Lynn', 'Lyons', 'Macdonald', 'Macias', 'Mack', 'Madden', 'Maddox',
         'Maldonado', 'Malone', 'Mann', 'Manning', 'Marks', 'Marquez', 'Marsh', 'Marshall', 'Martin', 'Martinez',
         'Mason', 'Massey', 'Mathews', 'Mathis', 'Matthews', 'Maxwell', 'May', 'Mayer', 'Maynard', 'Mayo', 'Mays',
         'Mcbride', 'Mccall', 'Mccarthy', 'Mccarty', 'Mcclain', 'Mcclure', 'Mcconnell', 'Mccormick', 'Mccoy', 'Mccray',
         'Mccullough', 'Mcdaniel', 'Mcdonald', 'Mcdowell', 'Mcfadden', 'Mcfarland', 'Mcgee', 'Mcgowan', 'Mcguire',
         'Mcintosh', 'Mcintyre', 'Mckay', 'Mckee', 'Mckenzie', 'Mckinney', 'Mcknight', 'Mclaughlin', 'Mclean', 'Mcleod',
         'Mcmahon', 'Mcmillan', 'Mcneil', 'Mcpherson', 'Meadows', 'Medina', 'Mejia', 'Melendez', 'Melton', 'Mendez',
         'Mendoza', 'Mercado', 'Mercer', 'Merrill', 'Merritt', 'Meyer', 'Meyers', 'Michael', 'Middleton', 'Miles',
         'Miller', 'Mills', 'Miranda', 'Mitchell', 'Molina', 'Monroe', 'Montgomery', 'Montoya', 'Moody', 'Moon',
         'Mooney', 'Moore', 'Morales', 'Moran', 'Moreno', 'Morgan', 'Morin', 'Morris', 'Morrison', 'Morrow', 'Morse',
         'Morton', 'Moses', 'Mosley', 'Moss', 'Mueller', 'Mullen', 'Mullins', 'Munoz', 'Murphy', 'Murray', 'Myers',
         'Nash', 'Navarro', 'Neal', 'Nelson', 'Newman', 'Newton', 'Nguyen', 'Nichols', 'Nicholson', 'Nielsen', 'Nieves',
         'Nixon', 'Noble', 'Noel', 'Nolan', 'Norman', 'Norris', 'Norton', 'Nunez', 'Obrien', 'Ochoa', 'Oconnor', 'Odom',
         'Odonnell', 'Oliver', 'Olsen', 'Olson', 'Oneal', 'Oneil', 'Oneill', 'Orr', 'Ortega', 'Ortiz', 'Osborn',
         'Osborne', 'Owen', 'Owens', 'Pace', 'Pacheco', 'Padilla', 'Page', 'Palmer', 'Park', 'Parker', 'Parks',
         'Parrish', 'Parsons', 'Pate', 'Patel', 'Patrick', 'Patterson', 'Patton', 'Paul', 'Payne', 'Pearson', 'Peck',
         'Pena', 'Pennington', 'Perez', 'Perkins', 'Perry', 'Peters', 'Petersen', 'Peterson', 'Petty', 'Phelps',
         'Phillips', 'Pickett', 'Pierce', 'Pittman', 'Pitts', 'Pollard', 'Poole', 'Pope', 'Porter', 'Potter', 'Potts',
         'Powell', 'Powers', 'Pratt', 'Preston', 'Price', 'Prince', 'Pruitt', 'Puckett', 'Pugh', 'Quinn', 'Ramirez',
         'Ramos', 'Ramsey', 'Randall', 'Randolph', 'Rasmussen', 'Ratliff', 'Ray', 'Raymond', 'Reed', 'Reese', 'Reeves',
         'Reid', 'Reilly', 'Reyes', 'Reynolds', 'Rhodes', 'Rice', 'Rich', 'Richard', 'Richards', 'Richardson',
         'Richmond', 'Riddle', 'Riggs', 'Riley', 'Rios', 'Rivas', 'Rivera', 'Rivers', 'Roach', 'Robbins', 'Roberson',
         'Roberts', 'Robertson', 'Robinson', 'Robles', 'Rocha', 'Rodgers', 'Rodriguez', 'Rodriquez', 'Rogers', 'Rojas',
         'Rollins', 'Roman', 'Romero', 'Rosa', 'Rosales', 'Rosario', 'Rose', 'Ross', 'Roth', 'Rowe', 'Rowland', 'Roy',
         'Ruiz', 'Rush', 'Russell', 'Russo', 'Rutledge', 'Ryan', 'Salas', 'Salazar', 'Salinas', 'Sampson', 'Sanchez',
         'Sanders', 'Sandoval', 'Sanford', 'Santana', 'Santiago', 'Santos', 'Sargent', 'Saunders', 'Savage', 'Sawyer',
         'Schmidt', 'Schneider', 'Schroeder', 'Schultz', 'Schwartz', 'Scott', 'Sears', 'Sellers', 'Serrano', 'Sexton',
         'Shaffer', 'Shannon', 'Sharp', 'Sharpe', 'Shaw', 'Shelton', 'Shepard', 'Shepherd', 'Sheppard', 'Sherman',
         'Shields', 'Short', 'Silva', 'Simmons', 'Simon', 'Simpson', 'Sims', 'Singleton', 'Skinner', 'Slater', 'Sloan',
         'Small', 'Smith', 'Snider', 'Snow', 'Snyder', 'Solis', 'Solomon', 'Sosa', 'Soto', 'Sparks', 'Spears', 'Spence',
         'Spencer', 'Stafford', 'Stanley', 'Stanton', 'Stark', 'Steele', 'Stein', 'Stephens', 'Stephenson', 'Stevens',
         'Stevenson', 'Stewart', 'Stokes', 'Stone', 'Stout', 'Strickland', 'Strong', 'Stuart', 'Suarez', 'Sullivan',
         'Summers', 'Sutton', 'Swanson', 'Sweeney', 'Sweet', 'Sykes', 'Talley', 'Tanner', 'Tate', 'Taylor', 'Terrell',
         'Terry', 'Thomas', 'Thompson', 'Thornton', 'Tillman', 'Todd', 'Torres', 'Townsend', 'Tran', 'Travis',
         'Trevino', 'Trujillo', 'Tucker', 'Turner', 'Tyler', 'Tyson', 'Underwood', 'Valdez', 'Valencia', 'Valentine',
         'Valenzuela', 'Vance', 'Vang', 'Vargas', 'Vasquez', 'Vaughan', 'Vaughn', 'Vazquez', 'Vega', 'Velasquez',
         'Velazquez', 'Velez', 'Villarreal', 'Vincent', 'Vinson', 'Wade', 'Wagner', 'Walker', 'Wall', 'Wallace',
         'Waller', 'Walls', 'Walsh', 'Walter', 'Walters', 'Walton', 'Ward', 'Ware', 'Warner', 'Warren', 'Washington',
         'Waters', 'Watkins', 'Watson', 'Watts', 'Weaver', 'Webb', 'Weber', 'Webster', 'Weeks', 'Weiss', 'Welch',
         'Wells', 'West', 'Wheeler', 'Whitaker', 'White', 'Whitehead', 'Whitfield', 'Whitley', 'Whitney', 'Wiggins',
         'Wilcox', 'Wilder', 'Wiley', 'Wilkerson', 'Wilkins', 'Wilkinson', 'William', 'Williams', 'Williamson',
         'Willis', 'Wilson', 'Winters', 'Wise', 'Witt', 'Wolf', 'Wolfe', 'Wong', 'Wood', 'Woodard', 'Woods', 'Woodward',
         'Wooten', 'Workman', 'Wright', 'Wyatt', 'Wynn', 'Yang', 'Yates', 'York', 'Young', 'Zamora', 'Zimmerman']
personalities = [
    'ISTJ',
    'ISFJ',
    'INFJ',
    'INTJ',
    'ISTP',
    'ISFP',
    'INFP',
    'INTP',
    'ESTP',
    'ESFP',
    'ENFP',
    'ENTP',
    'ESTJ',
    'ESFJ',
    'ENFJ',
    'ENTJ']
# <QueryDict: {'csrfmiddlewaretoken': ['4CaVMCovQl2IbysucPRCKrUxuVNRe4Tcr6LUcSxhaftsnuHiO8HXlGZW3gTx4tkF'], 
# 'taskId': ['week 1'], 'description': ['test'], 'minReqAbility': ['0.3'], 'profileWeight': ['0.5'], 
# 'difficultyWeight': ['0.5'], 'initDate': ['2022-07-20'], 'finalDate': ['2022-07-27'], 'profileDim0': ['0'], 
# 'profileDim1': ['0']}> <MultiValueDict: {'files': [<InMemoryUploadedFile: testTask_BBn7DVn.png (image/png)>]}>
task_ids = ["week1_01", "week1_10", "week1_11", "week2_00", "week2_01", "week2_10", "week2_11", "week3_00", "week3_01",
            "week3_10", "week3_11", "week4_00", "week4_01", "week4_10", "week4_11", "week5_00", "week5_01", "week5_10",
            "week5_11"]
description = '.'

min_req_ability = ["0.2", "0.2", "0.2", "0.3", "0.3", "0.3", "0.3", "0.5", "0.5", "0.5", "0.5", "0.6", "0.6", "0.6",
                   "0.6", "0.7", "0.7", "0.7", "0.7"]
task_w = '0.5'

profile_dim0 = ['0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1']
profile_dim1 = ['1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1']


# region Questionnaire Auxiliary Functions
def is_questionnaire_completed(questionnaire, user):
    return Submission.objects.filter(questionnaire=questionnaire, student=user).exists()


# endregion


class Views:  # acts as a namespace

    # region Global Functions
    def init_server(request):
        server_state_model_bridge.set_curr_adaptation_state([])
        server_state_model_bridge.set_ready_for_new_activity(True)
        server_state_model_bridge.set_curr_selected_users([])
        server_state_model_bridge.set_curr_free_users(player_bridge.get_all_stored_student_usernames())
        server_state_model_bridge.set_curr_selected_tasks([])
        server_state_model_bridge.set_curr_free_tasks(task_bridge.get_all_stored_task_ids())

        server_state_model_bridge.set_sim_is_link_shared(False)
        server_state_model_bridge.set_sim_is_task_created(False)
        server_state_model_bridge.set_sim_week_one_users_evaluated(False)
        server_state_model_bridge.set_sim_simulate_reaction(False)
        server_state_model_bridge.set_sim_week_four_done_once(False)

        server_state_model_bridge.set_simulation_week(0)
        server_state_model_bridge.set_sim_student_to_evaluate("")
        server_state_model_bridge.set_sim_unavailable_student("")
        server_state_model_bridge.set_sim_student_x("")
        server_state_model_bridge.set_sim_student_y("")
        server_state_model_bridge.set_sim_student_z("")
        server_state_model_bridge.set_sim_student_w("")

        for player in player_bridge.get_all_stored_student_usernames():
            player_bridge.reset_player_curr_state(player)
            player_bridge.reset_player_past_model_increases(player)

        if not Questionnaire.objects.filter(title="First_Questionnaire").exists():
            OEJTS_questionnaire.create_MBTI_questionnaire()

        if not Tag.objects.filter(name="All", target="student").exists():
            Tag.objects.create(name="All", target="student", is_removable=False, is_assignable=False)

        if not Tag.objects.filter(name="All", target="task").exists():
            Tag.objects.create(name="All", target="task", is_removable=False, is_assignable=False)

        # if not Tag.objects.filter(name="Group A").exists():
        #     Tag.objects.create(name="Group A", is_removable=False)
        # 
        # if not Tag.objects.filter(name="Group B").exists():
        #     Tag.objects.create(name="Group B", is_removable=False)
        # 
        # if not Tag.objects.filter(name="E").exists():
        #     Tag.objects.create(name="E", is_removable=False, is_assignable=False)
        # 
        # if not Tag.objects.filter(name="I").exists():
        #     Tag.objects.create(name="I", is_removable=False, is_assignable=False)
        # 
        # if not Tag.objects.filter(name="S").exists():
        #     Tag.objects.create(name="S", is_removable=False, is_assignable=False)
        # 
        # if not Tag.objects.filter(name="N").exists():
        #     Tag.objects.create(name="N", is_removable=False, is_assignable=False)
        # 
        # if not Tag.objects.filter(name="T").exists():
        #     Tag.objects.create(name="T", is_removable=False, is_assignable=False)
        # 
        # if not Tag.objects.filter(name="F").exists():
        #     Tag.objects.create(name="F", is_removable=False, is_assignable=False)
        # 
        # if not Tag.objects.filter(name="J").exists():
        #     Tag.objects.create(name="J", is_removable=False, is_assignable=False)
        # 
        # if not Tag.objects.filter(name="P").exists():
        #     Tag.objects.create(name="P", is_removable=False, is_assignable=False)

        # create default professor for tests
        http_request = HttpRequest()
        http_request.method = 'POST'
        http_request.POST['fullname'] = 'default'
        http_request.POST['username'] = 'default'
        http_request.POST['role'] = 'Professor'
        http_request.POST['email'] = 'default@tecnico.ulisboa.pt'
        http_request.POST['password1'] = 'VW8fiAUkGs7QLwn'
        http_request.POST['password2'] = 'VW8fiAUkGs7QLwn'
        http_request.POST['age'] = '20'
        http_request.POST['gender'] = 'Male'
        http_request.POST['description'] = '.'
        http_request.POST['Create User'] = 'Register'

        http_request.user = request.user

        Views.user_registration(http_request)

        return HttpResponse('ok')

    def simulate_reaction(request):
        all_users = player_bridge.get_all_player_ids()

        sim_flags = server_state_model_bridge.get_sim_flags()

        for playerId in all_users:

            prev_state = player_bridge.get_player_states_data_frame(playerId).states[-1]

            new_state = Views.calc_reaction(
                player_bridge=player_bridge,
                state=prev_state,
                player_id=playerId)

            if sim_flags['simWeek'] == 2:
                if playerId == sim_flags['simStudentX']:
                    new_state.characteristics.ability = 0.3
                    new_state.characteristics.engagement = 0.3

                elif playerId == sim_flags['simStudentY']:
                    new_state.characteristics.ability = 0.2
                    new_state.characteristics.engagement = 0.2

                elif playerId == sim_flags['simStudentW']:
                    new_state.characteristics.engagement = 0.95

                elif playerId == sim_flags['simStudentZ']:
                    new_state.characteristics.engagement = 0.95

            Views.save_player_characteristics(playerId, new_state.characteristics.ability,
                                              new_state.characteristics.engagement)

        server_state_model_bridge.set_sim_simulate_reaction(True)
        return HttpResponse('ok')

    def home(request):
        Views.login_check(request)
        if request.user.is_authenticated:
            return redirect('/dash')
        else:
            return render(request, 'home.html')

    def login_check(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('[INFO] login check performed on user with id - ' + str(username) + ', password - ' + str(password))

        if username is None:
            return

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.info(request, 'Login failed! Credentials not recognized.')

    def logout_check(request):
        logout(request)
        return redirect('/home')

    def user_registration(request):
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            profile_form = CreateUserProfileForm(request.POST, request.FILES)

            if form.is_valid() and profile_form.is_valid():
                user = form.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.curr_state = json.dumps(PlayerState(profile=int_prof_template.generate_copy()),
                                                default=lambda o: o.__dict__)
                profile.past_data_frame = json.dumps(
                    PlayerStatesDataFrame(
                        interactions_profile_template=int_prof_template.generate_copy().reset(),
                        trim_alg=trim_alg_template
                    ),
                    default=lambda o: o.__dict__, sort_keys=True)
                profile.preferences = json.dumps(int_prof_template.generate_copy().reset(),
                                                 default=lambda o: o.__dict__,
                                                 sort_keys=True)
                profile.characteristics = json.dumps(PlayerCharacteristics(ability=0, engagement=0),
                                                     default=lambda o: o.__dict__,
                                                     sort_keys=True)
                profile.save()

                # add All tag to student
                http_request = HttpRequest()
                http_request.method = 'POST'
                http_request.POST['targetId'] = user.username
                http_request.POST['name'] = 'All'
                http_request.POST['target'] = 'student'
                Views.assign_tag(http_request)

                if 'Student' in profile.role:
                    currFreeUsers = server_state_model_bridge.get_curr_free_users()
                    currFreeUsers.append(user.username)
                    server_state_model_bridge.set_curr_free_users(currFreeUsers)
                    player_bridge.set_player_grade(user.username, 0)

                if not request.user.is_authenticated:
                    login(request, user)
                return redirect('/dash')
            else:
                context = {'form': form, 'profileForm': profile_form}
                return render(request, 'userRegistration.html', context)

        elif request.method == 'GET':
            form = CreateUserForm()
            profile_form = CreateUserProfileForm()

            context = {'form': form, 'profileForm': profile_form}
            return render(request, 'userRegistration.html', context)

    def user_update(request):
        if request.method == 'POST':

            instance = request.user
            username_to_update = request.GET.get('username_to_update')
            if username_to_update:
                try:
                    instance = User.objects.get(username=username_to_update)
                except User.DoesNotExist:
                    messages.info(request, 'Account not updated! Username not found.')
                    return redirect('/userUpdate')

            form = UpdateUserForm(request.POST, instance=instance)
            profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=instance.userprofile)

            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                profile = profile_form.save()
                return redirect('/dash')
            else:
                context = {'form': form, 'profileForm': profile_form}
                return render(request, 'userUpdate.html', context)

        elif request.method == 'GET':
            instance = request.user
            username_to_update = request.GET.get('username_to_update')
            if username_to_update:
                try:
                    instance = User.objects.get(username=username_to_update)
                except User.DoesNotExist:
                    messages.info(request, 'Account not updated! Username not found.')
                    return redirect('/userUpdate')

            form = UpdateUserForm(instance=instance)
            profile_form = UpdateUserProfileForm(instance=instance.userprofile)

            context = {'form': form, 'profileForm': profile_form}
            return render(request, 'userUpdate.html', context)

    def user_deletion(request):
        if request.method == 'GET':
            can_logout = False
            username = request.GET.get('usernameToDelete')
            if not username:
                username = request.user.username
                can_logout = True

            try:
                if can_logout:
                    logout(request)  # logout player before removing it
                Views.delete_user(username)

            except User.DoesNotExist:
                messages.info(request, 'Account not deleted! Username not found.')
                return redirect('/userUpdate')

            return redirect('/home')

    def delete_user(username):
        player = User.objects.get(username=username)
        player.delete()

        curr_free_users = server_state_model_bridge.get_curr_free_users()
        if username in curr_free_users:
            curr_free_users.remove(username)
            server_state_model_bridge.set_curr_free_users(curr_free_users)

        curr_selected_users = server_state_model_bridge.get_curr_selected_users()
        if username in curr_selected_users:
            curr_selected_users.remove(username)
            server_state_model_bridge.set_curr_selected_users(curr_selected_users)

    def is_user_registered(username):
        returned = {}
        if username is not None:
            try:
                returned['user'] = User.objects.get(username=username).userprofile
                returned['storedUsers'] = UserProfile.objects.filter(username__contains=username)
            except ObjectDoesNotExist as e:
                print('user does not exist!')
                returned = {'user': False, 'storedUsers': User.objects.filter(username__contains=username)}
        return returned

    def dash(request):
        dash_switch = {
            'Student': 'student/dash.html',
            'Professor': 'professor/dash.html',
            'Developer': 'designer/dash.html'
        }

        # check for active questionnaires
        active_questionnaires = Questionnaire.objects.filter(is_active=True)
        available_questionnaires = []

        for questionnaire in active_questionnaires:
            if not is_questionnaire_completed(questionnaire, request.user):
                available_questionnaires.append(questionnaire)

        context = {"availableQuestionnaires": available_questionnaires}
        try:
            return render(request, dash_switch.get(str(request.user.userprofile.role)), context)
        except UserProfile.DoesNotExist:
            return redirect('/admin')

    def get_random_string(length):
        letters = string.ascii_lowercase
        numbers = '0123456789'
        chars = letters + numbers
        result_str = random.choice(numbers) + ''.join(random.choice(chars) for i in range(length))
        return result_str

    # endregion

    # region Student Functions
    def start_activity(request):
        # remove from selected and move to occupied list
        curr_selected_users = server_state_model_bridge.get_curr_selected_users()
        curr_free_users = server_state_model_bridge.get_curr_free_users()

        curr_selected_users.remove(request.session.get('username'))
        curr_free_users.append(request.session.get('username'))
        server_state_model_bridge.set_curr_selected_users(curr_selected_users)
        server_state_model_bridge.set_curr_free_users(curr_free_users)
        return render(request, 'student/activity.html')

    def save_task_results(request):
        if request.POST:
            username = request.session.get('username')
            Views.save_player_characteristics(username, request.POST['ability'], request.POST['engagement'])
            return Views.dash(request)

    def save_player_characteristics(username, ability, engagement):
        characteristics = player_bridge.get_player_states_data_frame(username).states[-1].characteristics
        ability_to_save = (float(ability) - characteristics.ability)

        sim_flags = server_state_model_bridge.get_sim_flags()
        if username == sim_flags['simStudentX'] and sim_flags['simWeek'] == 2:
            ability_to_save = 0.3
        elif username == sim_flags['simStudentY'] and sim_flags['simWeek'] == 2:
            ability_to_save = 0.2

        characteristics = PlayerCharacteristics(ability=ability_to_save, engagement=float(engagement))
        player_bridge.set_player_characteristics(username, characteristics)
        player_bridge.set_player_grade(username=username, grade=round(
            float(player_bridge.get_player_grade(username=username)) + characteristics.ability / 5.0, 2))

    # endregion

    # region Professor Functions
    def start_adaptation(request):
        server_state_model_bridge.set_ready_for_new_activity(False)
        try:
            # store current states in players' state window, after the adaptation returns
            for username in server_state_model_bridge.get_curr_selected_users():
                player_bridge.set_and_save_player_state_to_data_frame(username,
                                                                      player_bridge.get_player_curr_state(username))

            curr_adaptation_state = adaptation.iterate()

        except (Exception, ArithmeticError, ValueError) as e:
            template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
            message = template.format(type(e).__name__, e.args)
            print(message)
            server_state_model_bridge.set_ready_for_new_activity(True)
            return HttpResponse('error')

        if server_state_model_bridge.get_simulation_week() == 2 and curr_adaptation_state != []:
            sim_student_x = curr_adaptation_state["groups"][0][0]
            sim_student_y = curr_adaptation_state["groups"][0][1]

            sim_student_w = curr_adaptation_state["groups"][1][0]
            sim_student_z = curr_adaptation_state["groups"][1][1]

            server_state_model_bridge.set_sim_student_x(sim_student_x)
            server_state_model_bridge.set_sim_student_y(sim_student_y)
            server_state_model_bridge.set_sim_student_w(sim_student_w)
            server_state_model_bridge.set_sim_student_z(sim_student_z)

        server_state_model_bridge.set_curr_adaptation_state(curr_adaptation_state)
        server_state_model_bridge.set_ready_for_new_activity(True)

        return Views.fetch_server_state(request)

    def config_adaptation(request):

        global curr_config_params

        new_config_params = request.POST
        if curr_config_params == new_config_params:
            return HttpResponse('ok')

        # switch algorithms
        def quality_eval_alg_switcher_knn(request):
            return KNNRegQualityEvalAlg(
                player_model_bridge=player_bridge,
                k=int(new_config_params['k']),
                quality_weights=PlayerCharacteristics(ability=float(new_config_params['qualityWeightAb']),
                                                      engagement=float(new_config_params['qualityWeightEng']))
            )

        def quality_eval_alg_switcher_synergy(request):
            return SynergiesTabQualityEvalAlg(
                player_model_bridge=player_bridge,
                synergy_table_path=new_config_params['synergyTablePath']
            )

        def quality_eval_alg_switcher_diversity(request):
            return DiversityQualityEvalAlg(
                player_model_bridge=player_bridge,
                diversity_weight=float(new_config_params['diversityWeight'])
            )

        sel_quality_eval_alg = {}
        sel_quality_eval_alg_id = new_config_params['selectedQualityEvalAlgId']

        print(sel_quality_eval_alg_id)
        if sel_quality_eval_alg_id == 'K-Nearest-Neighbors (KNN)':
            sel_quality_eval_alg = quality_eval_alg_switcher_knn(request)
            # sel_pref_est_alg = sel_quality_eval_alg
        elif sel_quality_eval_alg_id == 'KNN w/ Synergy Between Students':
            sel_quality_eval_alg = quality_eval_alg_switcher_synergy(request)
            # sel_pref_est_alg = KNNRegQualityEvalAlg(
            #     player_bridge,
            #     int(new_config_params['synergiesK']),
            #     quality_weights=PlayerCharacteristics(
            #         ability=float(new_config_params['synergiesQualityWeightsAb']),
            #         engagement=float(new_config_params['synergiesQualityWeightsEng'])
            #     )
            # )
        elif sel_quality_eval_alg_id == 'KNN w/ Personality Diversity':
            sel_quality_eval_alg = quality_eval_alg_switcher_diversity(request)
            # sel_pref_est_alg = KNNRegQualityEvalAlg(
            #     player_bridge,
            #     int(new_config_params['synergiesK']),
            #     quality_weights=PlayerCharacteristics(
            #         ability=float(new_config_params['synergiesQualityWeightsAb']),
            #         engagement=float(new_config_params['synergiesQualityWeightsEng'])
            #     )
            # )

        sel_pref_est_alg = ExplorationPreferencesEstAlg(
            player_model_bridge=player_bridge,
            interactions_profile_template=int_prof_template,
            quality_eval_alg=sel_quality_eval_alg,
            num_tested_player_profiles=100)

        def sel_configs_alg_switcher_random(request):
            return RandomConfigsGenAlg(
                player_model_bridge=player_bridge,
                interactions_profile_template=int_prof_template.generate_copy(),
                min_num_players_per_group=int(new_config_params['minNumPlayersPerGroup']),
                max_num_players_per_group=int(new_config_params['maxNumPlayersPerGroup']),
                # preferred_num_players_per_group=int(new_config_params['preferredNumPlayersPerGroup']),
                joint_player_constraints=new_config_params['jointPlayerConstraints'],
                separated_player_constraints=new_config_params['separatedPlayerConstraints'])

        def sel_configs_alg_switcher_prs(request):
            return PureRandomSearchConfigsGenAlg(
                player_model_bridge=player_bridge,
                interactions_profile_template=int_prof_template.generate_copy(),
                quality_eval_alg=sel_quality_eval_alg,
                pref_est_alg=sel_pref_est_alg,
                num_config_choices=int(new_config_params['numberOfConfigChoices']),
                min_num_players_per_group=int(new_config_params['minNumPlayersPerGroup']),
                max_num_players_per_group=int(new_config_params['maxNumPlayersPerGroup']),
                # preferred_num_players_per_group=int(new_config_params['preferredNumPlayersPerGroup']),
                joint_player_constraints=new_config_params['jointPlayerConstraints'],
                separated_player_constraints=new_config_params['separatedPlayerConstraints'])

        def sel_configs_alg_switcher_evl(request):
            return EvolutionaryConfigsGenAlg(
                player_model_bridge=player_bridge,
                interactions_profile_template=int_prof_template.generate_copy(),
                quality_eval_alg=sel_quality_eval_alg,

                min_num_players_per_group=int(new_config_params['minNumPlayersPerGroup']),
                max_num_players_per_group=int(new_config_params['maxNumPlayersPerGroup']),
                # preferred_num_players_per_group=int(new_config_params['preferredNumberOfPlayersPerGroup']),

                initial_population_size=int(new_config_params['initialPopulationSize']),
                num_evolutions_per_iteration=int(new_config_params['numEvolutionsPerIteration']),

                prob_cross=float(new_config_params['probCross']),
                prob_mut=float(new_config_params['probMutation']),

                prob_mut_config=float(new_config_params['probMutationConfig']),
                prob_mut_profiles=float(new_config_params['probMutationProfiles']),

                num_children_per_iteration=int(new_config_params['numChildrenPerIteration']),
                num_survivors=int(new_config_params['numSurvivors']),

                cx_op="order",
                joint_player_constraints=new_config_params['jointPlayerConstraints'],
                separated_player_constraints=new_config_params['separatedPlayerConstraints'])

        def sel_configs_alg_switcher_odpip(request):
            return ODPIPConfigsGenAlg(
                player_model_bridge=player_bridge,
                interactions_profile_template=int_prof_template.generate_copy(),
                quality_eval_alg=sel_quality_eval_alg,
                pref_est_alg=sel_pref_est_alg,

                min_num_players_per_group=int(new_config_params['minNumPlayersPerGroup']),
                max_num_players_per_group=int(new_config_params['maxNumPlayersPerGroup']),
                # preferred_num_players_per_group=int(new_config_params['preferredNumPlayersPerGroup']),

                joint_player_constraints=new_config_params['jointPlayerConstraints'],
                separated_player_constraints=new_config_params['separatedPlayerConstraints'])

        def sel_configs_alg_switcher_clink(request):
            return CLinkConfigsGenAlg(
                player_model_bridge=player_bridge,
                interactions_profile_template=int_prof_template.generate_copy(),
                quality_eval_alg=sel_quality_eval_alg,
                pref_est_alg=sel_pref_est_alg,

                min_num_players_per_group=int(new_config_params['minNumPlayersPerGroup']),
                max_num_players_per_group=int(new_config_params['maxNumPlayersPerGroup']))

        # switch config. gen. algs
        selected_gen_alg_id = new_config_params['selectedGenAlgId']
        sel_configs_gen_alg = defaultConfigsAlg
        if selected_gen_alg_id == 'Random (no search)':
            sel_configs_gen_alg = sel_configs_alg_switcher_random(request)
        elif selected_gen_alg_id == 'Pure Random Search':
            sel_configs_gen_alg = sel_configs_alg_switcher_prs(request)
        elif selected_gen_alg_id == 'Evolutionary Search':
            sel_configs_gen_alg = sel_configs_alg_switcher_evl(request)
        elif selected_gen_alg_id == 'ODPIP Search':
            sel_configs_gen_alg = sel_configs_alg_switcher_odpip(request)
        elif selected_gen_alg_id == 'Coalition Link Search':
            sel_configs_gen_alg = sel_configs_alg_switcher_clink(request)

        global adaptation
        adaptation = Adaptation(player_model_bridge=player_bridge,
                                task_model_bridge=task_bridge,
                                configs_gen_alg=sel_configs_gen_alg,
                                name='GIMME')

        if new_config_params['isBootstrapped'] == 'true':
            adaptation.bootstrap(num_bootstrap_iterations=int(new_config_params['numBootstrapIterations']))

        curr_config_params = new_config_params
        return HttpResponse('ok')

    def task_registration(request):
        if 'Professor' not in request.user.userprofile.role:
            return HttpResponse('500')
        else:
            if request.method == 'POST':
                request_info = request.POST
                form = CreateTaskForm(request_info, request.FILES)
                if form.is_valid():
                    task = form.save(commit=False)

                    task.profile = json.dumps(InteractionsProfile(
                        {
                            'Challenge': float(request_info['profileDim0']),
                            'Focus': float(request_info['profileDim1'])
                        }
                    ), default=lambda o: o.__dict__, sort_keys=True)

                    print(request_info)
                    task.task_id = request_info['taskId']
                    task.init_date = request_info['initDate']
                    task.final_date = request_info['finalDate']

                    task.profile_w = request_info['taskW']
                    task.difficulty_w = str(1.0 - float(request_info['taskW']))

                    task.min_req_ability = request_info['difficulty']

                    task.save()

                    # add All tag to task
                    http_request = HttpRequest()
                    http_request.method = 'POST'
                    http_request.POST['targetId'] = task.task_id
                    http_request.POST['name'] = 'All'
                    http_request.POST['target'] = 'task'
                    Views.assign_tag(http_request)

                    # add task to free tasks
                    curr_free_tasks = server_state_model_bridge.get_curr_free_tasks()
                    curr_free_tasks.append(str(task.task_id))
                    server_state_model_bridge.set_curr_free_tasks(curr_free_tasks)

                    server_state_model_bridge.set_sim_is_task_created(True)
                    return redirect('/dash')
                else:
                    context = {'form': form}
                    return render(request, 'taskRegistration.html', context)

            elif request.method == 'GET':
                form = CreateTaskForm()
                context = {'form': form}
                return render(request, 'taskRegistration.html', context)

    def task_update(request):
        if 'Professor' not in request.user.userprofile.role:
            return HttpResponse('500')
        else:
            if request.method == 'POST':
                task_id_to_update = request.GET.get('taskIdToUpdate')
                request_info = request.POST
                try:
                    instance = Task.objects.get(task_id=task_id_to_update)

                    post = request.POST
                    _mutable = post._mutable
                    post._mutable = True
                    post['taskId'] = task_id_to_update
                    post['minReqAbility'] = request_info['difficulty']
                    post['profileW'] = request_info['taskW']
                    post['difficultyW'] = str(1.0 - float(request_info['taskW']))
                    post['initDate'] = request_info['initDate']
                    post['finalDate'] = request_info['finalDate']

                    post['profile'] = json.dumps(InteractionsProfile(
                        {
                            'Challenge': float(request_info['profileDim0']),
                            'Focus': float(request_info['profileDim1'])
                        }
                    ), default=lambda o: o.__dict__, sort_keys=True)

                    post._mutable = _mutable
                    form = UpdateTaskForm(post, instance=instance)

                    if form.is_valid():
                        form.save()
                        return redirect('/dash')
                    else:
                        messages.info(request, 'Task not updated! Form not valid.')
                        return redirect('/taskUpdate')

                except Task.DoesNotExist:
                    messages.info(request, 'Task not updated! Id not found.')
                    return redirect('/taskUpdate')


            elif request.method == 'GET':
                task_id_to_update = request.GET.get('taskIdToUpdate')
                try:
                    instance = Task.objects.get(task_id=task_id_to_update)
                    form = UpdateTaskForm(instance=instance)
                    context = {'form': form}
                    return render(request, 'taskUpdate.html', context)

                except Task.DoesNotExist:
                    messages.info(request, 'Task not updated! Id not found.')
                    return redirect('/dash')

    def task_deletion(request):
        if request.method == 'GET':
            task_id = request.GET.get('taskIdToDelete')
            print(task_id)
            try:
                Views.delete_task(task_id)

            except Task.DoesNotExist:
                messages.info(request, 'Task not deleted! Id not found.')
                return redirect('/dash')

            return redirect('/dash')

    def delete_task(task_id):
        task = Task.objects.get(task_id=task_id)
        task.delete()

        curr_free_tasks = server_state_model_bridge.get_curr_free_tasks()
        if task_id in curr_free_tasks:
            curr_free_tasks.remove(task_id)
            server_state_model_bridge.set_curr_free_tasks(curr_free_tasks)

        curr_selected_tasks = server_state_model_bridge.get_curr_selected_tasks()
        if task_id in curr_selected_tasks:
            curr_selected_tasks.remove(task_id)
            server_state_model_bridge.set_curr_selected_tasks(curr_selected_tasks)

    def is_task_registered(task_id):
        returned = {}
        if task_id is not None:
            try:
                returned['task'] = Task.objects.get(taskId=task_id)
                returned['storedTasks'] = Task.objects.filter(taskId__contains=task_id)
            except ObjectDoesNotExist as e:
                print('task does not exist!')
                returned = {'task': False, 'storedTasks': Task.objects.filter(taskId__contains=task_id)}
        return returned

    def add_all_users_selected(request):  # reads (player) from args
        if request.method == 'POST':
            server_state_model_bridge.set_curr_selected_users(
                server_state_model_bridge.get_curr_selected_users() + server_state_model_bridge.get_curr_free_users())
            server_state_model_bridge.set_curr_free_users([])
            return HttpResponse('ok')

    def remove_all_users_selected(request):  # reads (player) from args
        if request.method == 'POST':
            server_state_model_bridge.set_curr_free_users(
                server_state_model_bridge.get_curr_selected_users() + server_state_model_bridge.get_curr_free_users())
            server_state_model_bridge.set_curr_selected_users([])

            tags = Tag.objects.all()
            for tag in tags:
                tag.is_selected = False
                tag.save()

            return HttpResponse('ok')

    def add_selected_user(request):  # reads (player) from args
        if request.method == 'POST':
            username_to_add = request.POST.get('username')

            curr_selected_users = server_state_model_bridge.get_curr_selected_users()
            curr_free_users = server_state_model_bridge.get_curr_free_users()

            if not username_to_add in curr_selected_users:
                curr_selected_users.append(username_to_add)
                curr_free_users.remove(username_to_add)

            server_state_model_bridge.set_curr_selected_users(curr_selected_users)
            server_state_model_bridge.set_curr_free_users(curr_free_users)
            return HttpResponse('ok')

    def remove_selected_user(request):  # reads (player) from args
        if request.method == 'POST':
            username_to_remove = request.POST.get('username')
            curr_selected_users = server_state_model_bridge.get_curr_selected_users()
            curr_free_users = server_state_model_bridge.get_curr_free_users()
            if username_to_remove in curr_selected_users:
                curr_selected_users.remove(username_to_remove)
                curr_free_users.append(username_to_remove)
            server_state_model_bridge.set_curr_selected_users(curr_selected_users)
            server_state_model_bridge.set_curr_free_users(curr_free_users)
            return HttpResponse('ok')

    def add_all_tasks_selected(request):  # reads (player) from args
        if request.method == 'POST':
            server_state_model_bridge.set_curr_selected_tasks(
                server_state_model_bridge.get_curr_selected_tasks() + server_state_model_bridge.get_curr_free_tasks())
            server_state_model_bridge.set_curr_free_tasks([])
            return HttpResponse('ok')

    def remove_all_tasks_selected(request):  # reads (player) from args
        if request.method == 'POST':
            server_state_model_bridge.set_curr_free_tasks(
                server_state_model_bridge.get_curr_selected_tasks() + server_state_model_bridge.get_curr_free_tasks())
            server_state_model_bridge.set_curr_selected_tasks([])
            return HttpResponse('ok')

    def add_selected_task(request):  # reads (player) from args
        if request.method == 'POST':
            task_to_add = request.POST.get('taskId')
            curr_selected_tasks = server_state_model_bridge.get_curr_selected_tasks()
            curr_free_tasks = server_state_model_bridge.get_curr_free_tasks()
            if task_to_add not in curr_selected_tasks:
                curr_selected_tasks.append(task_to_add)
                curr_free_tasks.remove(task_to_add)
            server_state_model_bridge.set_curr_selected_tasks(curr_selected_tasks)
            server_state_model_bridge.set_curr_free_tasks(curr_free_tasks)
            return HttpResponse('ok')

    def remove_selected_task(request):  # reads (player) from args
        if request.method == 'POST':
            task_id_to_remove = request.POST.get('taskId')
            curr_selected_tasks = server_state_model_bridge.get_curr_selected_tasks();
            curr_free_tasks = server_state_model_bridge.get_curr_free_tasks();
            if task_id_to_remove in curr_selected_tasks:
                curr_selected_tasks.remove(task_id_to_remove)
                curr_free_tasks.append(task_id_to_remove)
            server_state_model_bridge.set_curr_selected_tasks(curr_selected_tasks)
            server_state_model_bridge.set_curr_free_tasks(curr_free_tasks)
            return HttpResponse('ok')

    # region Auxiliary Functions
    def fetch_student_states(request):
        if request.method == 'POST':
            selected_user_ids = player_bridge.get_all_stored_student_usernames()

            user_info_request = HttpRequest()
            user_info_request.method = 'POST'
            user_states = {}
            for username in selected_user_ids:
                user_info_request.POST = {'username': username}
                user_info = Views.fetch_student_info(user_info_request).content.decode('utf-8')
                user_states[username] = user_info

            user_states = json.dumps(user_states, default=lambda o: o.__dict__, sort_keys=True)
            return HttpResponse(user_states)
        return HttpResponse('error')

    def fetch_student_info(request):
        if request.method == 'POST':
            username = request.POST['username']

            user_info = {}
            user_info['fullname'] = player_bridge.get_player_full_name(username)
            user_info['email'] = player_bridge.get_player_email(username)
            user_info['characteristics'] = player_bridge.get_player_curr_characteristics(username)
            user_info['group'] = player_bridge.get_player_curr_group(username)
            user_info['groupProfile'] = player_bridge.get_player_curr_profile(username).dimensions
            user_info['tasks'] = player_bridge.get_player_curr_tasks(username)
            user_info['statesDataFrame'] = player_bridge.get_player_states_data_frame(username)
            user_info['grade'] = player_bridge.get_player_grade(username)
            user_info['tags'] = player_bridge.get_player_tags(username)

            personality = player_bridge.get_player_personality(username)

            if personality:
                user_info['personality'] = personality.get_personality_string()
            else:
                user_info['personality'] = ''

            user_info = json.dumps(user_info, default=lambda o: o.__dict__, sort_keys=True)

            return HttpResponse(user_info)
        return HttpResponse('error')

    def fetch_server_state(request):
        try:
            if request.method == 'GET':
                sim_state = server_state_model_bridge.get_sim_flags()

                task_object = HttpRequest()
                task_object.method = 'POST'

                curr_selected_tasks_ids = server_state_model_bridge.get_curr_selected_tasks()
                task_object.POST = {'tasks': str(curr_selected_tasks_ids)[1:][:-1].replace(' ', '').replace('\'', '')}
                curr_selected_tasks = Views.fetch_tasks_from_id(task_object).content.decode('utf-8')

                task_object = HttpRequest()
                task_object.method = 'POST'

                curr_free_tasks_ids = server_state_model_bridge.get_curr_free_tasks()
                task_object.POST = {'tasks': str(curr_free_tasks_ids)[1:][:-1].replace(' ', '').replace('\'', '')}
                curr_free_tasks = Views.fetch_tasks_from_id(task_object).content.decode('utf-8')

                new_session_state = {'timestamp': time.time(),
                                     'simWeek': sim_state['simWeek'],
                                     'simStudentToEvaluate': sim_state['simStudentToEvaluate'],
                                     'simUnavailableStudent': sim_state['simUnavailableStudent'],
                                     'simStudentX': sim_state['simStudentX'],
                                     'simStudentY': sim_state['simStudentY'],
                                     'simStudentW': sim_state['simStudentW'],
                                     'simStudentZ': sim_state['simStudentZ'],
                                     'simIsLinkShared': sim_state['simIsLinkShared'],
                                     'simIsTaskCreated': sim_state['simIsTaskCreated'],
                                     'simSimulateReaction': sim_state['simSimulateReaction'],
                                     'simWeekOneUsersEvaluated': sim_state['simWeekOneUsersEvaluated'],
                                     'currSelectedUsers': server_state_model_bridge.get_curr_selected_users(),
                                     'currFreeUsers': server_state_model_bridge.get_curr_free_users(),
                                     'studentTags': server_state_model_bridge.get_tags(target='student'),
                                     'taskTags': server_state_model_bridge.get_tags(target='task'),
                                     'currSelectedTasks': curr_selected_tasks,
                                     'currFreeTasks': curr_free_tasks,
                                     'readyForNewActivity': server_state_model_bridge.is_ready_for_new_activity()}

                if 'Professor' in request.user.userprofile.role:
                    new_session_state['currAdaptationState'] = server_state_model_bridge.get_curr_adaptation_state()

                new_session = json.dumps(new_session_state, default=lambda o: o.__dict__, sort_keys=True)

                return HttpResponse(new_session)
        except UserProfile.DoesNotExist:
            return HttpResponse('error')
        return HttpResponse('error')

    def fetch_tasks_from_id(request):
        if request.method == 'POST':
            tasks = request.POST['tasks']
            if tasks == '':
                tasks = []
            else:
                tasks = tasks.split(',')
            returned_tasks = []
            for task_id in tasks:
                if not task_id in task_bridge.get_all_stored_task_ids():
                    return HttpResponse('error')

                task = task_bridge.get_task(task_id)
                returned_task = {'taskId': task_id,
                                 'description': task.description,
                                 'files': str(task.files),
                                 'tags': task_bridge.get_task_tags(task_id=task_id)}
                returned_tasks.append(returned_task)

            returned_tasks = json.dumps(returned_tasks, default=lambda o: o.__dict__, sort_keys=True)
            return HttpResponse(returned_tasks)
        return HttpResponse('error')

    def fetch_group_from_id(request):
        if request.method == 'POST':
            group_id = int(request.POST['groupId'])
            all_groups = server_state_model_bridge.get_curr_adaptation_state()['groups']
            if group_id < 0 or group_id > len(all_groups):
                return HttpResponse({})

            group = all_groups[group_id]
            returned_group = {'group': group}
            returned_group = json.dumps(returned_group, default=lambda o: o.__dict__, sort_keys=True)
            return HttpResponse(returned_group)
        return HttpResponse('error')

    def fetch_user_state(request):
        if request.method == 'POST':
            username = request.POST['username']

            returned_state = {'curr_state': player_bridge.get_player_curr_state(username),
                              'data_frame': player_bridge.get_player_states_data_frame(username)}
            return HttpResponse(json.dumps(returned_state,
                                           default=lambda o: o.__dict__, sort_keys=True))
        return HttpResponse('error')

    def upload_task_results(request):
        if request.method == 'POST':
            username = request.POST['username']
            characteristics_delta = json.loads(request.POST['characteristicsDelta'])

            characteristics = player_bridge.get_player_curr_characteristics(username)
            characteristics.ability += characteristics_delta['abilityInc']
            characteristics.engagement += characteristics_delta['engagementInc']

            player_bridge.set_player_characteristics(username, characteristics)

            grade = float(player_bridge.get_player_grade(username))
            grade += characteristics_delta['gradeInc']
            player_bridge.set_player_grade(username, grade)

            return HttpResponse('ok')
        return HttpResponse('error')

    def manually_change_student_group(request):
        if request.method == 'POST':
            adapt_state = server_state_model_bridge.get_curr_adaptation_state()

            gi_index = int(request.POST['student[groupId]'])
            gf_index = int(request.POST['group[groupId]'])

            u = str(request.POST['student[userId]'])

            # change groups
            gi = adapt_state['groups'][gi_index]
            gf = adapt_state['groups'][gf_index]

            # print("limits: "+str(adaptation.configsGenAlg.minNumberOfPlayersPerGroup)+"; "+str(adaptation.configsGenAlg.maxNumberOfPlayersPerGroup))
            # print(str(len(gi))+"; "+str(len(gf)))
            if (len(gi) == (adaptation.configsGenAlg.minNumberOfPlayersPerGroup - 1) or
                    len(gf) == (adaptation.configsGenAlg.maxNumberOfPlayersPerGroup + 1)):
                return HttpResponse('error')

            gi.remove(u)
            gf.append(u)

            for g_index in [gi_index, gf_index]:
                g = adapt_state['groups'][g_index]

                # recalculate averages
                curr_avg_characteristics = PlayerCharacteristics()
                curr_avg_characteristics.reset()
                for curr_player_i in g:
                    curr_player_chars = player_bridge.get_player_curr_characteristics(curr_player_i)
                    group_size = len(g)
                    curr_avg_characteristics.ability += curr_player_chars.ability / group_size
                    curr_avg_characteristics.engagement += curr_player_chars.engagement / group_size

                    adapt_state['avgCharacteristics'][g_index] = curr_avg_characteristics

                    server_state_model_bridge.set_curr_adaptation_state(adapt_state)

                    # change student information
                    player_bridge.set_player_profile(curr_player_i, adapt_state['profiles'][g_index])
                    player_bridge.set_player_group(curr_player_i, g)
                    player_bridge.set_player_tasks(curr_player_i, adapt_state['tasks'][g_index])

            return render(request, 'professor/manuallyManageStudent.html')

    def manually_manage_student(request):
        if request.method == 'GET':
            return render(request, 'professor/manuallyManageStudent.html')

    def fetch_synergies_table(request):
        if request.method == 'POST':
            tbl_file = open(os.path.join(settings.BASE_DIR, 'synergyTable.txt'), "r")
            returned_table = {"textual_tbl": tbl_file.read()}
            tbl_file.close()
            return HttpResponse(json.dumps(returned_table,
                                           default=lambda o: o.__dict__, sort_keys=True))
        return HttpResponse('error')

    def save_synergies_table(request):
        if request.method == 'POST':
            tbl_file = open(os.path.join(settings.BASE_DIR, 'synergyTable.txt'), "w")
            tbl_file.write(request.POST["textual_tbl"])
            tbl_file.close()
            return HttpResponse('ok')
        return HttpResponse('error')

    def reset_sim_week(request):
        if request.method == 'POST':
            server_state_model_bridge.set_simulation_week(0)
            players_ids = player_bridge.get_all_stored_student_usernames()
            for playerId in players_ids:
                Views.delete_user(playerId)

            task_ids = task_bridge.get_all_stored_task_ids()
            for task_id in task_ids:
                Views.delete_task(task_id)

            # server_state_model_bridge.setSimIsLinkShared(False)
            # server_state_model_bridge.setSimIsTaskCreated(False)
            # server_state_model_bridge.setSimWeekOneUsersEvaluated(False)
            # server_state_model_bridge.setSimSimulateReaction(False)
            Views.init_server(request)
            return HttpResponse('ok')
        return HttpResponse('error')

    def advance_sim_week(request):
        simulation_week = server_state_model_bridge.get_simulation_week()
        sim_simulate_reaction = server_state_model_bridge.get_sim_simulate_reaction()
        sim_week_one_users_evaluated = server_state_model_bridge.get_sim_week_one_users_evaluated()
        if request.method == 'POST':
            if simulation_week > 5:
                simulation_week = 6
            else:
                simulation_week += 1

            if simulation_week == 1:
                players = player_bridge.get_all_stored_student_usernames()
                tasks = task_bridge.get_all_stored_task_ids()
                if len(players) >= 12 and len(tasks) >= 16:
                    server_state_model_bridge.set_sim_student_to_evaluate(players[0])
                else:
                    simulation_week -= 1

            if simulation_week == 2:
                if sim_week_one_users_evaluated:
                    server_state_model_bridge.set_sim_unavailable_student(
                        player_bridge.get_all_stored_student_usernames()[10])
                else:
                    simulation_week -= 1

            if simulation_week == 3:
                if not sim_simulate_reaction:
                    simulation_week -= 1
                else:
                    sim_simulate_reaction = False

            if simulation_week == 5:
                if sim_simulate_reaction:
                    sim_simulate_reaction = False
                else:
                    simulation_week -= 1

            server_state_model_bridge.set_simulation_week(simulation_week)
            server_state_model_bridge.set_sim_simulate_reaction(sim_simulate_reaction)
            return HttpResponse('ok')

        return HttpResponse('error')

    def share_link_sim(request):
        if request.method == 'POST':
            server_state_model_bridge.set_sim_is_link_shared(True)
            for _ in range(int(request.POST['numUsersToGenerate'])):
                time.sleep(random.uniform(float(request.POST['minDelay']), float(request.POST['maxDelay'])))

                name = "".join(random.choice(names) + " " + random.choice(names))

                rand_number = random.random()
                one_third = 1.0 / 3.0
                if rand_number <= one_third:
                    gender = 'Male'

                elif rand_number >= 2 * one_third:
                    gender = 'Female'
                else:
                    gender = 'Other'

                http_request = HttpRequest()
                http_request.method = 'POST'

                http_request.POST['fullname'] = name
                name = name.replace(" ", "_")
                http_request.POST['username'] = name
                http_request.POST['role'] = role
                name = name.replace("_", ".").lower()
                http_request.POST['email'] = name + '@tecnico.ulisboa.pt'
                http_request.POST['password1'] = password
                http_request.POST['password2'] = password
                http_request.POST['age'] = age
                http_request.POST['gender'] = gender
                http_request.POST['description'] = description
                http_request.POST['Create User'] = createUser

                http_request.user = request.user

                Views.user_registration(http_request)

            return HttpResponse('ok')

        return HttpResponse('error')

    def task_registration_sim(request):
        if request.method == 'POST':
            today = date.today()
            init_week2 = today + timedelta(days=7)
            init_week3 = init_week2 + timedelta(days=7)
            init_week4 = init_week3 + timedelta(days=7)

            str_init_week1 = str(today)
            str_init_week2 = str(init_week2)
            str_init_week3 = str(init_week3)
            str_init_week4 = str(init_week4)

            init_date = [today, today, today, init_week2, init_week2, init_week2, init_week2, init_week3, init_week3,
                         init_week3, init_week3, init_week4, init_week4, init_week4, init_week4]

            str_init_date = [str_init_week1, str_init_week1, str_init_week1, str_init_week2, str_init_week2,
                             str_init_week2,
                             str_init_week2, str_init_week3, str_init_week3, str_init_week3, str_init_week3,
                             str_init_week4,
                             str_init_week4, str_init_week4, str_init_week4]
            str_final_date = []
            for j in init_date:
                str_final_date.append(str(j + timedelta(days=7)))

            for i in range(len(task_ids)):
                time.sleep(random.uniform(float(request.POST['min_delay']), float(request.POST['max_delay'])))

                http_request = HttpRequest()
                http_request.method = 'POST'

                http_request.POST['taskId'] = task_ids[i]
                http_request.POST['description'] = description
                http_request.POST['difficulty'] = min_req_ability[i]
                http_request.POST['taskW'] = task_w
                http_request.POST['initDate'] = str_init_date[i]
                http_request.POST['finalDate'] = str_final_date[i]
                http_request.POST['profileDim0'] = profile_dim0[i]
                http_request.POST['profileDim1'] = profile_dim1[i]

                http_request.user = request.user

                Views.task_registration(http_request)

            return HttpResponse('ok')

        return HttpResponse('error')

    def evaluate_sim(request):
        if request.method == 'POST':

            curr_selected_users = server_state_model_bridge.get_curr_selected_users()
            curr_selected_users.pop(0)
            for playerId in curr_selected_users:
                prev_state = player_bridge.get_player_states_data_frame(playerId).states[-1]
                new_state = Views.calc_reaction(
                    player_bridge=player_bridge,
                    state=prev_state,
                    player_id=playerId)

                Views.save_player_characteristics(playerId, new_state.characteristics.ability,
                                                  new_state.characteristics.engagement)

            server_state_model_bridge.set_sim_week_one_users_evaluated(True)
            return HttpResponse('ok')

        return HttpResponse('error')

    def calc_reaction(player_bridge, state, player_id):
        preferences = player_bridge.get_player_preferences_est(player_id)
        num_dims = len(preferences.dimensions)
        new_state = PlayerState(
            type=1,
            characteristics=PlayerCharacteristics(
                ability=state.characteristics.ability,
                engagement=state.characteristics.engagement
            ),
            profile=state.profile)
        new_state.characteristics.engagement = 1 - (
                preferences.distanceBetween(state.profile) / math.sqrt(num_dims))  #between 0 and 1
        if new_state.characteristics.engagement > 1:
            breakpoint()
        ability_increase_sim = new_state.characteristics.engagement
        new_state.characteristics.ability = new_state.characteristics.ability + ability_increase_sim
        return new_state

    # endregion

    # region Tags
    def create_new_tag(request):
        if request.method == 'POST':
            request_data = request.POST
            if Tag.objects.filter(name=request_data.get('name'), target=request_data.get('target')).exists():
                response_data = {
                    'status': 'error',
                    'message': 'Tag already exists'
                }
                return JsonResponse(response_data)
            form = CreateTagForm(request_data)
            response_data = {
                'status': 'error',
                'message': 'Create tag form invalid'
            }
            if form.is_valid():
                form.save()
                response_data = {
                    'status': 'success',
                    'message': 'Tag saved successfully'
                }
            return JsonResponse(response_data)

    def delete_tag(request):
        if request.method == 'POST':
            tag_name = request.POST.get('name')
            tag_target = request.POST.get('target')
            Tag.objects.filter(name=tag_name, target=tag_target).delete()
            response_data = {
                'status': 'success',
                'message': 'Tag deleted successfully'
            }
            return JsonResponse(response_data)

    def select_tag(request):
        if request.method == 'POST':
            tag_name = request.POST.get('name')
            tag_target = request.POST.get('target')
            try:
                tag = Tag.objects.get(name=tag_name, target=tag_target)
                tag_status = tag.is_selected
                tag.is_selected = not tag_status
                tag.save()
            except Tag.DoesNotExist:
                response_data = {
                    'status': 'error',
                    'message': 'Tag does not exist'
                }
                return JsonResponse(response_data)

            curr_free_users = server_state_model_bridge.get_curr_free_users()
            curr_selected_users = server_state_model_bridge.get_curr_selected_users()

            if not tag_status:
                # Select students
                students_to_select = []
                for student in curr_free_users:
                    if student in curr_selected_users:
                        continue
                    student_tags = User.objects.get(username=student).userprofile.tags.all()

                    for studentTag in student_tags:
                        if studentTag.name == tag_name:
                            students_to_select.append(student)
                            break
                for student in students_to_select:
                    curr_selected_users.append(student)
                    curr_free_users.remove(student)
                response_data = {
                    'status': 'success',
                    'message': 'Tag selected successfully',
                    'isSelected': True
                }
            else:
                # Deselect students
                students_to_deselect = []
                for student in curr_selected_users:

                    if student in curr_free_users:
                        continue

                    student_tags = User.objects.get(username=student).userprofile.tags.all()

                    deselect = True

                    for studentTag in student_tags:
                        if studentTag.is_selected:
                            deselect = False
                            break

                    if deselect:
                        students_to_deselect.append(student)
                for student in students_to_deselect:
                    curr_free_users.append(student)
                    curr_selected_users.remove(student)
                response_data = {
                    'status': 'success',
                    'message': 'Tag deselected successfully',
                    'isSelected': False
                }

            server_state_model_bridge.set_curr_selected_users(curr_selected_users)
            server_state_model_bridge.set_curr_free_users(curr_free_users)

            return JsonResponse(response_data)

    def assign_tag(request):
        if request.method == 'POST':
            tag_name = request.POST.get('name')
            target_id = request.POST.get('targetId')
            target = request.POST.get('target')

            print(request.POST)

            if target == 'student':
                player_bridge.add_player_tag(username=target_id, tag_name=tag_name)
            elif target == 'task':
                task_bridge.add_task_tag(task_id=target_id, tag_name=tag_name)

            response_data = {
                'status': 'success',
                'message': 'Tag assigned successfully'
            }

            return JsonResponse(response_data)

    def remove_assigned_tag(request):
        if request.method == 'POST':
            tag_name = request.POST.get('tag')
            target_id = request.POST.get('targetId')
            target = request.POST.get('target')

            if target == 'student':
                player_bridge.remove_player_tag(username=target_id, tag_name=tag_name)
            elif target == 'task':
                task_bridge.remove_task_tag(task_id=target_id, tag_name=tag_name)

            response_data = {
                'status': 'success',
                'message': 'Tag assigned successfully'
            }

            return JsonResponse(response_data)

    def randomize_group_tags(request):
        if request.method == 'POST':
            student_profiles = UserProfile.objects.filter(role__contains="Student")
            # students = [profile.user for profile in student_profiles]

            half_length = len(student_profiles) / 2
            count = 0

            group1_tag = Tag.objects.get(name="Group A")
            group2_tag = Tag.objects.get(name="Group B")

            student_profiles = student_profiles.order_by('?')

            for student in student_profiles:

                student.tags.remove(group1_tag)
                student.tags.remove(group2_tag)

                if count < half_length:
                    student.tags.add(group1_tag)
                else:
                    student.tags.add(group2_tag)

                student.save()
                count += 1

            response_data = {
                'status': 'success',
                'message': 'Groups randomized successfully'
            }

            return JsonResponse(response_data)

    # endregion

    # endregion

    # region Questionnaire Functions
    def questionnaire_MBTI(request, questionnaire_title):
        questionnaire = Questionnaire.objects.get(title=questionnaire_title)
        user = request.user

        # # Check if the user has already submitted their answers for this questionnaire
        if is_questionnaire_completed(questionnaire, user):
            return render(request, 'student/thanks.html')

        if request.method == 'POST':
            form = LikertForm(request.POST)
            if form.is_valid():
                submission = Submission.objects.create(questionnaire=questionnaire, student=request.user)
                submission.save()
                # Save the student's answers
                for question, value in form.cleaned_data.items():
                    if question.startswith('question_'):
                        question_id = int(question[9:])
                        answer = LikertResponse(student=user, question_id=question_id, value=value)
                        answer.save()

                # Calculate the result based on the user's answers
                result = OEJTS_questionnaire.calculate_personality_MBTI(form.cleaned_data)

                player_bridge.set_player_personality(user, result)

                return render(request, 'student/thanks.html')
        else:
            form = LikertForm()

        return render(request, 'student/questionnaire.html', {'form': form, 'questionnaire': questionnaire})

    def questionnaire(request, questionnaire_title):
        # switch(questionnaire.type)
        #	case QuestionnaireType.MBTI:
        #		questionnaire_MBTI(request)
        questionnaire = Questionnaire.objects.get(title=questionnaire_title)
        questionnaire_type = questionnaire.type

        if questionnaire_type == QuestionnaireType.MBTI:
            return Views.questionnaire_MBTI(request, questionnaire_title)

    def add_personality(request):
        if request.method != 'POST':
            return HttpResponse('error')

        personality_type = request.POST['personalityType']
        personality_model = request.POST['personalityModel']

        data = {}

        if personality_model == 'MBTI':
            personality = PersonalityMBTI(personality_type[0], personality_type[1], personality_type[2],
                                          personality_type[3])
            # data = {'personality': personality}
            data = {'personality': json.dumps(personality, default=lambda o: o.__dict__, sort_keys=True)}

        personality_form = UpdateUserPersonalityForm(data, instance=request.user.userprofile)

        if personality_form.is_valid():
            personality_form.save()

        return HttpResponse('ok')

    # endregion
