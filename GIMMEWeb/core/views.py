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

        curr_adaptation_state = json.loads(server_state.currAdaptationState)
        return curr_adaptation_state

    def is_ready_for_new_activity(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        ready_for_new_activity = json.loads(server_state.readyForNewActivity)
        return ready_for_new_activity

    def get_curr_selected_users(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_selected_users = json.loads(server_state.currSelectedUsers)
        return curr_selected_users

    def get_curr_free_users(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_free_users = json.loads(server_state.currFreeUsers)
        return curr_free_users

    def get_curr_selected_tasks(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_selected_tasks = json.loads(server_state.currSelectedTasks)
        return curr_selected_tasks

    def get_curr_free_tasks(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()

        curr_free_tasks = json.loads(server_state.currFreeTasks)
        return curr_free_tasks

    def get_simulation_week(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.simulationWeek

    def get_sim_simulate_reaction(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.simSimulateReaction

    def get_sim_week_one_users_evaluated(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.simWeekOneUsersEvaluated

    def get_sim_student_x(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.simStudentX

    def get_sim_student_y(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.simStudentY

    def get_sim_student_w(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.simStudentW

    def get_sim_student_z(self):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        return server_state.simStudentZ

    def get_sim_flags(self):
        server_state = ServerState.objects.first()
        serverStateSimData = {
            "simIsLinkShared": server_state.simIsLinkShared,
            "simIsTaskCreated": server_state.simIsTaskCreated,
            "simWeekOneUsersEvaluated": server_state.simWeekOneUsersEvaluated,
            "simSimulateReaction": server_state.simSimulateReaction,
            "simWeekFourDoneOnce": server_state.simWeekFourDoneOnce,
            "simulationWeek": server_state.simulationWeek,
            "simStudentToEvaluate": server_state.simStudentToEvaluate,
            "simUnavailableStudent": server_state.simUnavailableStudent,
            "simStudentX": server_state.simStudentX,
            "simStudentY": server_state.simStudentY,
            "simStudentW": server_state.simStudentW,
            "simStudentZ": server_state.simStudentZ,
        }
        return serverStateSimData

    def set_curr_adaptation_state(self, curr_adaptation_state):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_adaptation_state = json.dumps(curr_adaptation_state, default=lambda o: o.__dict__, sort_keys=True)
            server_state.currAdaptationState = curr_adaptation_state
        server_state.save()

    def set_ready_for_new_activity(self, ready_for_new_activity):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            ready_for_new_activity = json.dumps(ready_for_new_activity, default=lambda o: o.__dict__, sort_keys=True)
            server_state.readyForNewActivity = ready_for_new_activity
        server_state.save()

    def set_curr_selected_users(self, curr_selected_users):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_selected_users = json.dumps(curr_selected_users, default=lambda o: o.__dict__, sort_keys=True)
            server_state.currSelectedUsers = curr_selected_users
        server_state.save()

    def set_curr_free_users(self, curr_free_users):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_free_users = json.dumps(curr_free_users, default=lambda o: o.__dict__, sort_keys=True)
            server_state.currFreeUsers = curr_free_users
        server_state.save()

    def set_curr_selected_tasks(self, curr_selected_tasks):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_selected_tasks = json.dumps(curr_selected_tasks, default=lambda o: o.__dict__, sort_keys=True)
            server_state.currSelectedTasks = curr_selected_tasks
        server_state.save()

    def set_curr_free_tasks(self, curr_free_tasks):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            curr_free_tasks = json.dumps(curr_free_tasks, default=lambda o: o.__dict__, sort_keys=True)
            server_state.currFreeTasks = curr_free_tasks
        server_state.save()

    def set_sim_is_link_shared(self, sim_is_link_shared):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simIsLinkShared = sim_is_link_shared
        server_state.save()

    def set_sim_is_task_created(self, sim_is_task_created):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simIsTaskCreated = sim_is_task_created
        server_state.save()

    def set_sim_week_one_users_evaluated(self, sim_week_one_users_evaluated):
        server_state = ServerState.objects.first()
        if server_state == None:
            server_state = ServerState()
        else:
            server_state.simWeekOneUsersEvaluated = sim_week_one_users_evaluated
        server_state.save()

    def set_sim_simulate_reaction(self, sim_simulate_reaction):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simSimulateReaction = sim_simulate_reaction
        server_state.save()

    def set_sim_week_four_done_once(self, sim_week_four_done_once):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simWeekFourDoneOnce = sim_week_four_done_once
        server_state.save()

    def set_simulation_week(self, simulation_week):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simulationWeek = simulation_week
        server_state.save()

    def set_sim_student_to_evaluate(self, sim_student_to_evaluate):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simStudentToEvaluate = sim_student_to_evaluate
        server_state.save()

    def set_sim_unavailable_student(self, sim_unavailable_student):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simUnavailableStudent = sim_unavailable_student
        server_state.save()

    def set_sim_student_x(self, sim_student_x):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simStudentX = sim_student_x
        server_state.save()

    def set_sim_student_y(self, sim_student_y):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simStudentY = sim_student_y
        server_state.save()

    def set_sim_student_z(self, sim_student_z):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simStudentZ = sim_student_z
        server_state.save()

    def set_sim_student_w(self, sim_student_w):
        server_state = ServerState.objects.first()
        if server_state is None:
            server_state = ServerState()
        else:
            server_state.simStudentW = sim_student_w
        server_state.save()

    def get_tags(self):
        tags = list(Tag.objects.all())
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
        return task.finalDate

    def get_task_file_paths(self, task_id):
        task = Task.objects.get(task_id=task_id)
        return task.filePaths


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
        all_users = User.objects.all()
        all_user_ids = []
        for player in all_users:
            if 'Student' in player.userprofile.role:
                all_user_ids.append(player.username)
        return all_user_ids

    def get_player_name(self, username):
        player = User.objects.get(username=username)
        return player.username

    def get_player_email(self, username):
        player = User.objects.get(username=username)
        return player.email

    def get_player_curr_profile(self, username):
        player_info = User.objects.get(username=username).userprofile
        # print(json.dumps(player, default= lambda o: o.__dict__, sort_keys=True))
        profile = json.loads(player_info.currState)['profile']
        profile = InteractionsProfile(dimensions=profile['dimensions'])
        return profile

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
        player_info = User.objects.get(username=username).userprofile
        group = json.loads(player_info.curr_state)['group']
        return group

    def get_player_curr_tasks(self, username):
        player_info = User.objects.get(username=username).userprofile
        tasks = json.loads(player_info.curr_state)['tasks']
        return tasks

    def get_player_states_data_frame(self, username):
        player_info = User.objects.get(username=username).userprofile
        past_model_increases_data_frame = json.loads(player_info.past_model_increases_data_frame)

        states = []
        for state in past_model_increases_data_frame['states']:
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

        trim_alg = json.loads(json.dumps(past_model_increases_data_frame['trim_alg']))
        sdf = PlayerStatesDataFrame(
            states=states,
            interactions_profile_template=int_prof_template.generate_copy().reset(),
            trim_alg=ProximitySortPlayerDataTrimAlg(
                max_num_model_elements=int(trim_alg['max_num_model_elements']),
                epsilon=float(trim_alg['epsilon'])
            )
        )
        return sdf

    def get_player_curr_characteristics(self, username):
        player_info = User.objects.get(username=username).userprofile
        characteristics = json.loads(player_info.currState)['characteristics']
        return PlayerCharacteristics(ability=float(characteristics['ability']),
                                     engagement=float(characteristics['engagement']))

    def get_player_grade(self, username):
        player_info = User.objects.get(username=username).userprofile
        return player_info.grade

    def get_player_preferences_est(self, username):
        player_info = User.objects.get(username=username).userprofile
        preferences = json.loads(player_info.preferences)
        preferences = InteractionsProfile(dimensions=preferences['dimensions'])
        return preferences

    def get_player_curr_state(self, username):
        player_info = User.objects.get(username=username).userprofile
        curr_state = json.loads(player_info.currState)
        return PlayerState(profile=self.get_player_curr_profile(username),
                           characteristics=self.get_player_curr_characteristics(username),
                           dist=curr_state['dist'],
                           quality=curr_state['quality'],
                           group=curr_state['group'],
                           tasks=curr_state['tasks'])

    def get_player_full_name(self, username):
        player_info = User.objects.get(username=username).userprofile
        return player_info.fullName

    def reset_player_curr_state(self, username):
        player_info = User.objects.get(username=username).userprofile
        new_state = PlayerState()
        player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
        player_info.save()

    def reset_player_past_model_increases(self, username):
        player_states_data_frame = self.get_player_states_data_frame(username)

        self.set_player_characteristics(username, PlayerCharacteristics())
        self.set_player_profile(username, player_states_data_frame.interactionsProfileTemplate.generateCopy())

        player_states_data_frame.reset()

        player_info = User.objects.get(username=username).userprofile
        player_info.past_model_increases_data_frame = json.dumps(player_states_data_frame, default=lambda o: o.__dict__)
        player_info.save()

    def set_player_preferences_est(self, username, preferences):
        player_info = User.objects.get(username=username).userprofile
        player_info.preferences = json.dumps(preferences, default=lambda o: o.__dict__)
        player_info.save()

    def set_player_characteristics(self, username, characteristics):
        player_info = User.objects.get(username=username).userprofile
        new_state = self.get_player_curr_state(username)
        new_state.characteristics = characteristics
        player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
        player_info.save()

    def set_player_personality(self, username, personality):
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

    def set_player_grade(self, username, grade):
        player_info = User.objects.get(username=username).userprofile
        player_info.grade = grade
        player_info.save()

    def set_player_profile(self, username, profile):
        player_info = User.objects.get(username=username).userprofile
        new_state = self.get_player_curr_state(username)
        new_state.profile = profile
        player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
        player_info.save()

    def set_player_group(self, username, group):
        player_info = User.objects.get(username=username).userprofile
        new_state = self.get_player_curr_state(username)
        new_state.group = group
        player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
        player_info.save()

    def set_player_tasks(self, username, tasks):
        player_info = User.objects.get(username=username).userprofile
        new_state = self.get_player_curr_state(username)
        new_state.tasks = tasks
        player_info.currState = json.dumps(new_state, default=lambda o: o.__dict__)
        player_info.save()

    def add_player_tag(self, username, tag_name):
        userprofile = User.objects.get(username=username).userprofile
        tag = Tag.objects.get(name=tag_name)
        userprofile.tags.add(tag)
        userprofile.save()

    def remove_player_tag(self, username, tag_name):
        userprofile = User.objects.get(username=username).userprofile
        tag = Tag.objects.get(name=tag_name)
        userprofile.tags.remove(tag)
        userprofile.save()

    def get_player_tags(self, username):
        userprofile = User.objects.get(username=username).userprofile
        tags = list(userprofile.tags.all())
        return tags


player_bridge = CustomPlayerModelBridge()
currConfigParams = {}

int_prof_template = InteractionsProfile({'Challenge': 0, 'Focus': 0})
trim_alg_template = ProximitySortPlayerDataTrimAlg(
    max_num_model_elements=10,
    epsilon=0.05
)

defaultConfigsAlg = RandomConfigsGenAlg(
    player_model_bridge=player_bridge,
    interactions_profile_template=int_prof_template.generateCopy(),
    preferred_num_players_per_group=4)
adaptation = Adaptation(name='GIMME',
                        player_model_bridge=player_bridge,
                        task_model_bridge=task_bridge,
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
taskIds = ["week1_01", "week1_10", "week1_11", "week2_00", "week2_01", "week2_10", "week2_11", "week3_00", "week3_01",
           "week3_10", "week3_11", "week4_00", "week4_01", "week4_10", "week4_11", "week5_00", "week5_01", "week5_10",
           "week5_11"]
description = '.'

minReqAbility = ["0.2", "0.2", "0.2", "0.3", "0.3", "0.3", "0.3", "0.5", "0.5", "0.5", "0.5", "0.6", "0.6", "0.6",
                 "0.6", "0.7", "0.7", "0.7", "0.7"]
taskSelectWeigths = '0.5'

profileDim0 = ['0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1']
profileDim1 = ['1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1']


# region Questionnaire Auxiliary Functions
def is_questionnaire_completed(questionnaire, user):
    return Submission.objects.filter(questionnaire=questionnaire, student=user).exists()


# endregion


class Views:  # acts as a namespace

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

        if not Tag.objects.filter(name="Group A").exists():
            Tag.objects.create(name="Group A", is_removable=False)

        if not Tag.objects.filter(name="Group B").exists():
            Tag.objects.create(name="Group B", is_removable=False)

        if not Tag.objects.filter(name="E").exists():
            Tag.objects.create(name="E", is_removable=False, is_assignable=False)

        if not Tag.objects.filter(name="I").exists():
            Tag.objects.create(name="I", is_removable=False, is_assignable=False)

        if not Tag.objects.filter(name="S").exists():
            Tag.objects.create(name="S", is_removable=False, is_assignable=False)

        if not Tag.objects.filter(name="N").exists():
            Tag.objects.create(name="N", is_removable=False, is_assignable=False)

        if not Tag.objects.filter(name="T").exists():
            Tag.objects.create(name="T", is_removable=False, is_assignable=False)

        if not Tag.objects.filter(name="F").exists():
            Tag.objects.create(name="F", is_removable=False, is_assignable=False)

        if not Tag.objects.filter(name="J").exists():
            Tag.objects.create(name="J", is_removable=False, is_assignable=False)

        if not Tag.objects.filter(name="P").exists():
            Tag.objects.create(name="P", is_removable=False, is_assignable=False)

        return HttpResponse('ok')

    def calc_reaction(player_bridge, state, player_id):
        preferences = player_bridge.getPlayerPreferencesEst(player_id)
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

    def simulate_reaction(request):
        all_users = player_bridge.get_all_player_ids()

        sim_flags = server_state_model_bridge.get_sim_flags()

        for playerId in all_users:

            prev_state = player_bridge.get_player_states_data_frame(playerId).states[-1]

            new_state = Views.calc_reaction(
                player_bridge=player_bridge,
                state=prev_state,
                player_id=playerId)

            if sim_flags['simulationWeek'] == 2:
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

            Views.savePlayerCharacteristics(playerId, new_state.characteristics.ability,
                                            new_state.characteristics.engagement)

        server_state_model_bridge.set_sim_simulate_reaction(True)
        return HttpResponse('ok')

    # global methods
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

    # region Questionnaire View Functions
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

    # if request.method == 'POST':
    # 	form = LikertForm(request.POST)
    # 	if form.is_valid():
    # 		submission = Submission.objects.create(questionnaire=questionnaire, student=request.user)
    # 		for question_id, response in form.cleaned_data.items():
    # 			if question_id.startswith('question_'):
    # 				question_id = question_id[len('question_'):]
    # 				#response = LikertResponse(question_id=question_id, submission=submission, response=response)
    # 				#response.save()

    # 		return render(request, 'student/thanks.html')
    # else:
    # 	form = LikertForm()

    # context = { 'questionnaire': questionnaire,
    # 			'form' : form }

    # return render(request, 'student/questionnaire.html', context)

    def add_personality(request):
        if request.method != 'POST':
            return HttpResponse('error')

        personality_type = request.POST['personality_type']
        personality_model = request.POST['personality_model']

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

    # region Student Tag
    def create_new_tag(request):
        if request.method == 'POST':
            if Tag.objects.filter(name=request.POST.get('name')).exists():
                response_data = {
                    'status': 'error',
                    'message': 'Tag already exists'
                }

                return JsonResponse(response_data)

            form = CreateTagForm(request.POST)

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

            Tag.objects.filter(name=tag_name).delete()

            response_data = {
                'status': 'success',
                'message': 'Tag deleted successfully'
            }

            return JsonResponse(response_data)

    def select_tag(request):
        if request.method == 'POST':
            tag_name = request.POST.get('name')

            try:
                tag = Tag.objects.get(name=tag_name)
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
                    'is_selected': True
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
                    'is_selected': False
                }

            server_state_model_bridge.set_curr_selected_users(curr_selected_users)
            server_state_model_bridge.set_curr_free_users(curr_free_users)

            return JsonResponse(response_data)

    def assign_tag(request):
        if request.method == 'POST':
            tag_name = request.POST.get('tag')
            student_name = request.POST.get('student')

            userprofile = User.objects.get(username=student_name).userprofile
            tag = Tag.objects.get(name=tag_name)

            if tag in userprofile.tags.all():
                response_data = {
                    'status': 'error',
                    'message': 'Tag already assigned'
                }

            else:
                userprofile.tags.add(tag)
                userprofile.save()

                response_data = {
                    'status': 'success',
                    'message': 'Tag assigned successfully'
                }

            return JsonResponse(response_data)

    def remove_assigned_tag(request):
        if request.method == 'POST':
            tag_name = request.POST.get('tag')
            student_name = request.POST.get('student')

            userprofile = User.objects.get(username=student_name).userprofile
            tag = Tag.objects.get(name=tag_name)

            userprofile.tags.remove(tag)
            userprofile.save()

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

    def user_registration(request):
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            profile_form = CreateUserProfileForm(request.POST, request.FILES)

            if form.is_valid() and profile_form.is_valid():
                user = form.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.currState = json.dumps(PlayerState(profile=int_prof_template.generate_copy()),
                                               default=lambda o: o.__dict__)
                profile.past_model_increases_data_frame = json.dumps(
                    PlayerStatesDataFrame(
                        interactions_profile_template=int_prof_template.generate_copy().reset(),
                        trim_alg=trim_alg_template
                    ),
                    default=lambda o: o.__dict__, sort_keys=True)
                profile.preferences = json.dumps(int_prof_template.generate_copy().reset(),
                                                 default=lambda o: o.__dict__,
                                                 sort_keys=True)
                # profile.personality = json.dumps(personality, default=lambda o: o.__dict__, sort_keys=True)
                profile.save()

                # UNCOMMENT THIS IF ALL USERS SHOULD HAVE A RANDOM PERSONALITY ASSIGNED UPON REGISTRATION # # Add 
                # random personality ------------------- random_index = random.randint(0, len(personalities)-1) 
                # personalityType = personalities[random_index] personality = PersonalityMBTI(personalityType[0], 
                # personalityType[1], personalityType[2], personalityType[3]) # 
                # ------------------------------------------ playerBridge.setPlayerPersonality(user.username, 
                # personalityType)

                if 'Student' in profile.role:
                    currFreeUsers = server_state_model_bridge.get_curr_free_users()
                    currFreeUsers.append(user.username)
                    server_state_model_bridge.set_curr_free_users(currFreeUsers)
                    player_bridge.set_player_grade(user.username, 0)

                if not request.user.is_authenticated:
                    login(request, user)
                return redirect('/dash')
            else:
                context = {'form': form, 'profile_form': profile_form}
                return render(request, 'userRegistration.html', context)

        elif request.method == 'GET':
            form = CreateUserForm()
            profile_form = CreateUserProfileForm()

            context = {'form': form, 'profile_form': profile_form}
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
                context = {'form': form, 'profile_form': profile_form}
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

            context = {'form': form, 'profile_form': profile_form}
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

        context = {"available_questionnaires": available_questionnaires}

        print(request.user.userprofile.role)
        return render(request, dash_switch.get(str(request.user.userprofile.role)), context)

    def get_random_string(length):
        letters = string.ascii_lowercase
        numbers = '0123456789'
        chars = letters + numbers
        result_str = random.choice(numbers) + ''.join(random.choice(chars) for i in range(length))
        return result_str

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
            task_to_add = request.POST.get('task_id')
            curr_selected_tasks = server_state_model_bridge.get_curr_selected_tasks()
            curr_free_tasks = server_state_model_bridge.get_curr_free_tasks()
            if task_to_add not in curr_selected_tasks:
                curr_selected_tasks.append(task_to_add)
                curr_free_tasks.remove(task_to_add)
            server_state_model_bridge.set_curr_selected_tasks(curr_selected_tasks)
            server_state_model_bridge.set_curr_free_tasks(curr_free_tasks)
            return HttpResponse('ok')

    def removeSelectedTask(request):  # reads (player) from args
        if request.method == 'POST':
            TaskIdToRemove = request.POST.get('taskId')
            currSelectedTasks = server_state_model_bridge.get_curr_selected_tasks();
            currFreeTasks = server_state_model_bridge.get_curr_free_tasks();
            if TaskIdToRemove in currSelectedTasks:
                currSelectedTasks.remove(TaskIdToRemove)
                currFreeTasks.append(TaskIdToRemove)
            server_state_model_bridge.set_curr_selected_tasks(currSelectedTasks)
            server_state_model_bridge.set_curr_free_tasks(currFreeTasks)
            return HttpResponse('ok')

    # student methods
    def startActivity(request):
        # remove from selected and move to occupied list
        currSelectedUsers = server_state_model_bridge.get_curr_selected_users();
        currFreeUsers = server_state_model_bridge.get_curr_free_users();

        currSelectedUsers.remove(request.session.get('username'))
        currFreeUsers.append(request.session.get('username'))
        server_state_model_bridge.set_curr_selected_users(currSelectedUsers)
        server_state_model_bridge.set_curr_free_users(currFreeUsers)
        return render(request, 'student/activity.html')

    def saveTaskResults(request):
        if request.POST:
            username = request.session.get('username')
            Views.savePlayerCharacteristics(username, request.POST['ability'], request.POST['engagement'])
            return Views.dash(request)

    def savePlayerCharacteristics(username, ability, engagement):
        characteristics = player_bridge.get_player_states_data_frame(username).states[-1].characteristics
        abilityToSave = (float(ability) - characteristics.ability)

        simFlags = server_state_model_bridge.get_sim_flags()
        if username == simFlags['simStudentX'] and simFlags['simulationWeek'] == 2:
            abilityToSave = 0.3
        elif username == simFlags['simStudentY'] and simFlags['simulationWeek'] == 2:
            abilityToSave = 0.2

        characteristics = PlayerCharacteristics(ability=abilityToSave, engagement=float(engagement))
        player_bridge.set_player_characteristics(username, characteristics)
        player_bridge.set_player_grade(username=username, grade=round(
            float(player_bridge.get_player_grade(username=username)) + characteristics.ability / 5.0, 2))

    # professor methods
    def startAdaptation(request):
        server_state_model_bridge.set_ready_for_new_activity(False)
        try:
            # store current states in players' state window, after the adaptation returns
            for username in server_state_model_bridge.get_curr_selected_users():
                player_bridge.set_and_save_player_state_to_data_frame(username,
                                                                      player_bridge.get_player_curr_state(username))

            currAdaptationState = adaptation.iterate()

        except (Exception, ArithmeticError, ValueError) as e:
            template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
            message = template.format(type(e).__name__, e.args)
            print(message)
            server_state_model_bridge.set_ready_for_new_activity(True)
            return HttpResponse('error')

        if server_state_model_bridge.get_simulation_week() == 2 and currAdaptationState != []:
            simStudentX = currAdaptationState["groups"][0][0]
            simStudentY = currAdaptationState["groups"][0][1]

            simStudentW = currAdaptationState["groups"][1][0]
            simStudentZ = currAdaptationState["groups"][1][1]

            server_state_model_bridge.set_sim_student_x(simStudentX)
            server_state_model_bridge.set_sim_student_y(simStudentY)
            server_state_model_bridge.set_sim_student_w(simStudentW)
            server_state_model_bridge.set_sim_student_z(simStudentZ)

        server_state_model_bridge.set_curr_adaptation_state(currAdaptationState)
        server_state_model_bridge.set_ready_for_new_activity(True)

        return Views.fetchServerState(request)

    def configAdaptation(request):

        global currConfigParams

        newConfigParams = request.POST
        if (currConfigParams == newConfigParams):
            return HttpResponse('ok')

        # switch reg algs
        selectedRegAlg = {}
        persEstRegAlg = {}

        def selectedRegAlgSwitcherKNN(request):
            return KNNRegression(
                player_bridge,
                int(newConfigParams['numNNs']),
                qualityWeights=PlayerCharacteristics(ability=float(newConfigParams['qualityWeightsAb']),
                                                     engagement=float(newConfigParams['qualityWeightsEng']))
            )

        def selectedRegAlgSwitcherSynergy(request):
            return TabularAgentSynergies(
                playerModelBridge=player_bridge,
                taskModelBridge=task_bridge
            )

        def selectedRegAlgSwitcherDiversity(request):
            return DiversityValueAlg(
                player_bridge,
                float(newConfigParams['diversityWeight'])
            )

        selectedRegAlgId = newConfigParams['selectedRegAlgId']
        # selectedRegAlg = None

        if (selectedRegAlgId == 'K-Nearest-Neighbors (KNN)'):
            selectedRegAlg = selectedRegAlgSwitcherKNN(request)
            persEstRegAlg = selectedRegAlg
        elif (selectedRegAlgId == 'KNN w/ Synergy Between Students'):
            selectedRegAlg = selectedRegAlgSwitcherSynergy(request)
            persEstRegAlg = KNNRegression(
                player_bridge,
                int(newConfigParams['synergiesNumNNs']),
                qualityWeights=PlayerCharacteristics(
                    ability=float(newConfigParams['synergiesQualityWeightsAb']),
                    engagement=float(newConfigParams['synergiesQualityWeightsEng'])
                )
            )
        elif (selectedRegAlgId == 'KNN w/ Personality Diversity'):
            selectedRegAlg = selectedRegAlgSwitcherDiversity(request)
            persEstRegAlg = KNNRegression(
                player_bridge,
                int(newConfigParams['synergiesNumNNs']),
                qualityWeights=PlayerCharacteristics(
                    ability=float(newConfigParams['synergiesQualityWeightsAb']),
                    engagement=float(newConfigParams['synergiesQualityWeightsEng'])
                )
            )

        selectedGenAlg = {}

        def selectedGenAlgSwitcherRandom(request):
            return RandomConfigsGen(
                playerModelBridge=player_bridge,
                interactionsProfileTemplate=int_prof_template.generateCopy(),
                minNumberOfPlayersPerGroup=int(newConfigParams['minNumberOfPlayersPerGroup']),
                maxNumberOfPlayersPerGroup=int(newConfigParams['maxNumberOfPlayersPerGroup']),
                # preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
                jointPlayerConstraints=newConfigParams['jointPlayerConstraints'],
                separatedPlayerConstraints=newConfigParams['separatedPlayerConstraints'])

        def selectedGenAlgSwitcherPRS(request):
            return PureRandomSearchConfigsGen(
                playerModelBridge=player_bridge,
                interactionsProfileTemplate=int_prof_template.generateCopy(),
                regAlg=selectedRegAlg,
                persEstAlg=ExplorationPreferencesEstAlg(
                    playerModelBridge=player_bridge,
                    interactionsProfileTemplate=int_prof_template.generateCopy(),
                    regAlg=persEstRegAlg,
                    numTestedPlayerProfiles=100),
                numberOfConfigChoices=int(newConfigParams['numberOfConfigChoices']),
                minNumberOfPlayersPerGroup=int(newConfigParams['minNumberOfPlayersPerGroup']),
                maxNumberOfPlayersPerGroup=int(newConfigParams['maxNumberOfPlayersPerGroup']),
                # preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
                jointPlayerConstraints=newConfigParams['jointPlayerConstraints'],
                separatedPlayerConstraints=newConfigParams['separatedPlayerConstraints']
            )

        def selectedGenAlgSwitcherAnnealedPRS(request):
            return AnnealedPRSConfigsGen(
                playerModelBridge=player_bridge,
                interactionsProfileTemplate=int_prof_template.generateCopy(),
                regAlg=selectedRegAlg,
                persEstAlg=ExplorationPreferencesEstAlg(
                    playerModelBridge=player_bridge,
                    interactionsProfileTemplate=int_prof_template.generateCopy(),
                    regAlg=persEstRegAlg,
                    numTestedPlayerProfiles=100),
                numberOfConfigChoices=int(newConfigParams['numberOfConfigChoices']),
                minNumberOfPlayersPerGroup=int(newConfigParams['minNumberOfPlayersPerGroup']),
                maxNumberOfPlayersPerGroup=int(newConfigParams['maxNumberOfPlayersPerGroup']),
                # preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
                temperatureDecay=float(newConfigParams['temperatureDecay']),
                jointPlayerConstraints=newConfigParams['jointPlayerConstraints'],
                separatedPlayerConstraints=newConfigParams['separatedPlayerConstraints']
            )

        def selectedGenAlgSwitcherEvolutionary(request):
            return EvolutionaryConfigsGenDEAP(
                playerModelBridge=player_bridge,
                interactionsProfileTemplate=int_prof_template.generateCopy(),
                regAlg=selectedRegAlg,
                persEstAlg=ExplorationPreferencesEstAlg(
                    playerModelBridge=player_bridge,
                    interactionsProfileTemplate=int_prof_template.generateCopy(),
                    regAlg=persEstRegAlg,
                    numTestedPlayerProfiles=100),

                minNumberOfPlayersPerGroup=int(newConfigParams['minNumberOfPlayersPerGroup']),
                maxNumberOfPlayersPerGroup=int(newConfigParams['maxNumberOfPlayersPerGroup']),
                # preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']), 

                initialPopulationSize=int(newConfigParams['initialPopulationSize']),
                numberOfEvolutionsPerIteration=int(newConfigParams['numberOfEvolutionsPerIteration']),

                probOfCross=float(newConfigParams['probOfCross']),
                probOfMutation=float(newConfigParams['probOfMutation']),

                probOfMutationConfig=float(newConfigParams['probOfMutationConfig']),
                probOfMutationGIPs=float(newConfigParams['probOfMutationGIPs']),

                numChildrenPerIteration=int(newConfigParams['numChildrenPerIteration']),
                numSurvivors=int(newConfigParams['numSurvivors']),

                cxOp="order",
                jointPlayerConstraints=newConfigParams['jointPlayerConstraints'],
                separatedPlayerConstraints=newConfigParams['separatedPlayerConstraints'])

        def selectedGenAlgSwitcherODPIP(request):
            return ODPIP(
                playerModelBridge=player_bridge,
                interactionsProfileTemplate=int_prof_template.generateCopy(),
                regAlg=selectedRegAlg,
                persEstAlg=ExplorationPreferencesEstAlg(
                    playerModelBridge=player_bridge,
                    interactionsProfileTemplate=int_prof_template.generateCopy(),
                    regAlg=persEstRegAlg,
                    numTestedPlayerProfiles=100),

                #preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
                minNumberOfPlayersPerGroup=int(newConfigParams['minNumberOfPlayersPerGroup']),
                maxNumberOfPlayersPerGroup=int(newConfigParams['maxNumberOfPlayersPerGroup']),

                taskModelBridge=task_bridge,
                jointPlayerConstraints=newConfigParams['jointPlayerConstraints'],
                separatedPlayerConstraints=newConfigParams['separatedPlayerConstraints']
            )

        def selectedGenAlgSwitcherCLink(request):
            return CLink(
                playerModelBridge=player_bridge,
                interactionsProfileTemplate=int_prof_template.generateCopy(),
                regAlg=selectedRegAlg,
                persEstAlg=ExplorationPreferencesEstAlg(
                    playerModelBridge=player_bridge,
                    interactionsProfileTemplate=int_prof_template.generateCopy(),
                    regAlg=persEstRegAlg,
                    numTestedPlayerProfiles=100),

                #preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
                minNumberOfPlayersPerGroup=int(newConfigParams['minNumberOfPlayersPerGroup']),
                maxNumberOfPlayersPerGroup=int(newConfigParams['maxNumberOfPlayersPerGroup']),
                taskModelBridge=task_bridge
            )

        # switch config. gen. algs
        selectedGenAlgId = newConfigParams['selectedGenAlgId']
        selectedGenAlg = defaultConfigsAlg
        if (selectedGenAlgId == 'Random (no search)'):
            selectedGenAlg = selectedGenAlgSwitcherRandom(request)
        elif (selectedGenAlgId == 'Pure Random Search'):
            selectedGenAlg = selectedGenAlgSwitcherPRS(request)
        elif (selectedGenAlgId == 'Annealed Pure Random Search'):
            selectedGenAlg = selectedGenAlgSwitcherAnnealedPRS(request)
        elif (selectedGenAlgId == 'Evolutionary Search'):
            selectedGenAlg = selectedGenAlgSwitcherEvolutionary(request)
        elif (selectedGenAlgId == 'ODPIP Search'):
            selectedGenAlg = selectedGenAlgSwitcherODPIP(request)
        elif (selectedGenAlgId == 'Coalition Link Search'):
            selectedGenAlg = selectedGenAlgSwitcherCLink(request)

        adaptation.init(player_bridge, task_bridge, configsGenAlg=selectedGenAlg, name='GIMME')

        if (newConfigParams['isBootstrapped'] == 'true'):
            adaptation.bootstrap(int(newConfigParams['numBootstrapIterations']))

        currConfigParams = newConfigParams
        return HttpResponse('ok')

    def taskRegistration(request):
        if (not 'Professor' in request.user.userprofile.role):
            return HttpResponse('500')
        else:
            if request.method == 'POST':
                requestInfo = request.POST
                form = CreateTaskForm(requestInfo, request.FILES)
                if form.is_valid():

                    task = form.save(commit=False)

                    task.profile = json.dumps(InteractionsProfile(
                        {
                            'Challenge': float(requestInfo['profileDim0']),
                            'Focus': float(requestInfo['profileDim1'])
                        }
                    ), default=lambda o: o.__dict__, sort_keys=True)

                    task.initDate = requestInfo['initDate']
                    task.finalDate = requestInfo['finalDate']

                    task.profileWeight = requestInfo['taskSelectWeigths']
                    task.difficultyWeight = str(1.0 - float(requestInfo['taskSelectWeigths']))

                    task.minReqAbility = requestInfo['difficulty']

                    task.save()

                    # add task to free tasks
                    currFreeTasks = server_state_model_bridge.get_curr_free_tasks()
                    currFreeTasks.append(str(task.taskId))
                    server_state_model_bridge.set_curr_free_tasks(currFreeTasks)

                    server_state_model_bridge.set_sim_is_task_created(True)

                    return redirect('/dash')
                else:
                    context = {'form': form}
                    return render(request, 'taskRegistration.html', context)

            elif request.method == 'GET':
                form = CreateTaskForm()
                context = {'form': form}
                return render(request, 'taskRegistration.html', context)

    def taskUpdate(request):
        if (not 'Professor' in request.user.userprofile.role):
            return HttpResponse('500')
        else:
            if request.method == 'POST':
                taskIdToUpdate = request.GET.get('taskIdToUpdate')
                requestInfo = request.POST
                try:
                    instance = Task.objects.get(taskId=taskIdToUpdate)

                    post = request.POST
                    _mutable = post._mutable
                    post._mutable = True
                    post['taskId'] = taskIdToUpdate
                    post['minReqAbility'] = requestInfo['difficulty']
                    post['profileWeight'] = requestInfo['taskSelectWeigths']
                    post['difficultyWeight'] = str(1.0 - float(requestInfo['taskSelectWeigths']))
                    post['initDate'] = requestInfo['initDate']
                    post['finalDate'] = requestInfo['finalDate']

                    post['profile'] = json.dumps(InteractionsProfile(
                        {
                            'Challenge': float(requestInfo['profileDim0']),
                            'Focus': float(requestInfo['profileDim1'])
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
                taskIdToUpdate = request.GET.get('taskIdToUpdate')
                try:
                    instance = Task.objects.get(taskId=taskIdToUpdate)
                    form = UpdateTaskForm(instance=instance)
                    context = {'form': form}
                    return render(request, 'taskUpdate.html', context)

                except Task.DoesNotExist:
                    messages.info(request, 'Task not updated! Id not found.')
                    return redirect('/dash')

    def taskDeletion(request):
        if request.method == 'GET':
            taskId = request.GET.get('taskIdToDelete')
            try:
                Views.deleteTask(taskId)

            except Task.DoesNotExist:
                messages.info(request, 'Task not deleted! Id not found.')
                return redirect('/dash')

            return redirect('/dash')

    def deleteTask(taskId):
        task = Task.objects.get(taskId=taskId)
        task.delete()

        currFreeTasks = server_state_model_bridge.get_curr_free_tasks()
        if (taskId in currFreeTasks):
            currFreeTasks.remove(taskId)
            server_state_model_bridge.set_curr_free_tasks(currFreeTasks)

        currSelectedTasks = server_state_model_bridge.get_curr_selected_tasks()
        if (taskId in currSelectedTasks):
            currSelectedTasks.remove(taskId)
            server_state_model_bridge.set_curr_selected_tasks(currSelectedTasks)

    def isTaskRegistered(taskId):
        returned = {}
        if (taskId != None):
            try:
                returned['task'] = Task.objects.get(taskId=taskId)
                returned['storedTasks'] = Task.objects.filter(taskId__contains=taskId)
            except ObjectDoesNotExist as e:
                print('task does not exist!')
                returned = {'task': False, 'storedTasks': Task.objects.filter(taskId__contains=taskId)}
        return returned

    # auxiliary methods
    def fetchStudentStates(request):
        if request.method == 'POST':
            selectedUserIds = player_bridge.get_all_stored_student_usernames()

            userInfoRequest = HttpRequest()
            userInfoRequest.method = 'POST'
            userStates = {}
            for username in selectedUserIds:
                userInfoRequest.POST = {'username': username}
                userInfo = Views.fetchStudentInfo(userInfoRequest).content.decode('utf-8')
                userStates[username] = userInfo

            userStates = json.dumps(userStates, default=lambda o: o.__dict__, sort_keys=True)
            return HttpResponse(userStates)
        return HttpResponse('error')

    def fetchStudentInfo(request):
        if request.method == 'POST':
            username = request.POST['username']

            userInfo = {}
            # userState['myStateGrid'] = playerBridge.getPlayerStateGrid(username)
            userInfo['fullName'] = player_bridge.get_player_full_name(username)
            userInfo['email'] = player_bridge.get_player_email(username)
            userInfo['characteristics'] = player_bridge.get_player_curr_characteristics(username)
            userInfo['group'] = player_bridge.get_player_curr_group(username)
            userInfo['groupProfile'] = player_bridge.get_player_curr_profile(username).dimensions
            userInfo['tasks'] = player_bridge.get_player_curr_tasks(username)
            userInfo['statesDataFrame'] = player_bridge.get_player_states_data_frame(username)
            userInfo['grade'] = player_bridge.get_player_grade(username)
            userInfo['tags'] = player_bridge.get_player_tags(username)

            personality = player_bridge.get_player_personality(username)

            if personality:
                userInfo['personality'] = personality.getPersonalityString()
            else:
                userInfo['personality'] = ''

            userInfo = json.dumps(userInfo, default=lambda o: o.__dict__, sort_keys=True)

            return HttpResponse(userInfo)
        return HttpResponse('error')

    def fetchServerState(request):
        if request.method == 'GET':
            newSessionState = {}
            newSessionState['timestamp'] = time.time()

            simState = server_state_model_bridge.get_sim_flags()

            newSessionState['simWeek'] = simState['simulationWeek']
            newSessionState['studentToEvaluate'] = simState['simStudentToEvaluate']
            newSessionState['unavailableStudent'] = simState['simUnavailableStudent']

            newSessionState['studentX'] = simState['simStudentX']
            newSessionState['studentY'] = simState['simStudentY']
            newSessionState['studentW'] = simState['simStudentW']
            newSessionState['studentZ'] = simState['simStudentZ']

            newSessionState['linkShared'] = simState['simIsLinkShared']
            newSessionState['isTaskCreated'] = simState['simIsTaskCreated']
            newSessionState['simSimulateReaction'] = simState['simSimulateReaction']
            newSessionState['simWeekOneUsersEvaluated'] = simState['simWeekOneUsersEvaluated']

            newSessionState['currSelectedUsers'] = server_state_model_bridge.get_curr_selected_users()
            newSessionState['currFreeUsers'] = server_state_model_bridge.get_curr_free_users()

            newSessionState['tags'] = server_state_model_bridge.get_tags()

            currSelectedTasks = []
            currFreeTasks = []

            taskObject = HttpRequest()
            taskObject.method = 'POST'

            currSelectedTasksIds = server_state_model_bridge.get_curr_selected_tasks()
            taskObject.POST = {'tasks': str(currSelectedTasksIds)[1:][:-1].replace(' ', '').replace('\'', '')}
            currSelectedTasks = Views.fetchTasksFromId(taskObject).content.decode('utf-8')

            taskObject = HttpRequest()
            taskObject.method = 'POST'

            currFreeTasksIds = server_state_model_bridge.get_curr_free_tasks()
            taskObject.POST = {'tasks': str(currFreeTasksIds)[1:][:-1].replace(' ', '').replace('\'', '')}
            currFreeTasks = Views.fetchTasksFromId(taskObject).content.decode('utf-8')

            newSessionState['currSelectedTasks'] = currSelectedTasks
            newSessionState['currFreeTasks'] = currFreeTasks

            newSessionState['readyForNewActivity'] = server_state_model_bridge.is_ready_for_new_activity()

            if ('Professor' in request.user.userprofile.role):
                newSessionState['currAdaptationState'] = server_state_model_bridge.get_curr_adaptation_state()

            newSession = json.dumps(newSessionState, default=lambda o: o.__dict__, sort_keys=True)

            return HttpResponse(newSession)
        return HttpResponse('error')

    def fetchTasksFromId(request):
        if request.method == 'POST':
            tasks = request.POST['tasks']
            if tasks == '':
                tasks = []
            else:
                tasks = tasks.split(',')
            returnedTasks = []
            for taskId in tasks:
                if not taskId in task_bridge.get_all_stored_task_ids():
                    return HttpResponse('error')

                task = task_bridge.get_task(taskId)
                returnedTask = {}
                returnedTask['taskId'] = taskId
                returnedTask['description'] = task.description
                returnedTask['files'] = str(task.files)
                returnedTasks.append(returnedTask)

            returnedTasks = json.dumps(returnedTasks, default=lambda o: o.__dict__, sort_keys=True)
            return HttpResponse(returnedTasks)
        return HttpResponse('error')

    def fetchGroupFromId(request):
        if request.method == 'POST':
            groupId = int(request.POST['groupId'])

            allGroups = server_state_model_bridge.get_curr_adaptation_state()['groups'];

            if groupId < 0 or groupId > len(allGroups):
                return HttpResponse({})

            group = allGroups[groupId];
            returnedGroup = {}
            returnedGroup['group'] = group

            returnedGroup = json.dumps(returnedGroup, default=lambda o: o.__dict__, sort_keys=True)
            return HttpResponse(returnedGroup)
        return HttpResponse('error')

    def fetchUserState(request):
        if request.method == 'POST':
            username = request.POST['username']

            returnedState = {}
            returnedState['currState'] = player_bridge.get_player_curr_state(username)
            returnedState['grid'] = player_bridge.getPlayerStateGrid(username)
            return HttpResponse(json.dumps(returnedState,
                                           default=lambda o: o.__dict__, sort_keys=True))
        return HttpResponse('error')

    def uploadTaskResults(request):
        if request.method == 'POST':
            username = request.POST['username']
            characteristicsDelta = json.loads(request.POST['characteristicsDelta'])

            characteristics = player_bridge.get_player_curr_characteristics(username)
            characteristics.ability += characteristicsDelta['abilityInc']
            characteristics.engagement += characteristicsDelta['engagementInc']

            player_bridge.set_player_characteristics(username, characteristics)

            grade = float(player_bridge.get_player_grade(username))
            grade += characteristicsDelta['gradeInc']
            player_bridge.set_player_grade(username, grade)

            return HttpResponse('ok')
        return HttpResponse('error')

    def manuallyChangeStudentGroup(request):
        if request.method == 'POST':
            adaptState = server_state_model_bridge.get_curr_adaptation_state()

            giIndex = int(request.POST['student[groupId]'])
            gfIndex = int(request.POST['group[groupId]'])

            u = str(request.POST['student[userId]'])

            # change groups
            gi = adaptState['groups'][giIndex]
            gf = adaptState['groups'][gfIndex]

            #print("limits: "+str(adaptation.configsGenAlg.minNumberOfPlayersPerGroup)+"; "+str(adaptation.configsGenAlg.maxNumberOfPlayersPerGroup))
            #print(str(len(gi))+"; "+str(len(gf)))
            if (len(gi) == (adaptation.configsGenAlg.minNumberOfPlayersPerGroup - 1) or
                    len(gf) == (adaptation.configsGenAlg.maxNumberOfPlayersPerGroup + 1)):
                return HttpResponse('error')

            gi.remove(u)
            gf.append(u)

            for gIndex in [giIndex, gfIndex]:
                g = adaptState['groups'][gIndex]

                # recalculate averages
                currAvgCharacteristics = PlayerCharacteristics()
                currAvgCharacteristics.reset()
                for currPlayerI in g:
                    currPlayerChars = player_bridge.get_player_curr_characteristics(currPlayerI)
                    groupSize = len(g)
                    currAvgCharacteristics.ability += currPlayerChars.ability / groupSize
                    currAvgCharacteristics.engagement += currPlayerChars.engagement / groupSize

                    adaptState['avgCharacteristics'][gIndex] = currAvgCharacteristics

                    server_state_model_bridge.set_curr_adaptation_state(adaptState)

                    # change student information
                    player_bridge.set_player_profile(currPlayerI, adaptState['profiles'][gIndex])
                    player_bridge.set_player_group(currPlayerI, g)
                    player_bridge.set_player_tasks(currPlayerI, adaptState['tasks'][gIndex])

            return render(request, 'manuallyManageStudent.html')

    def manuallyManageStudent(request):
        if request.method == 'GET':
            return render(request, 'manuallyManageStudent.html')

    def fetchSynergiesTable(request):
        if request.method == 'POST':
            tblFile = open(os.path.join(settings.BASE_DIR, 'synergyTable.txt'), "r")

            returnedTable = {}
            returnedTable["textualTbl"] = tblFile.read()

            tblFile.close()

            return HttpResponse(json.dumps(returnedTable,
                                           default=lambda o: o.__dict__, sort_keys=True))
        return HttpResponse('error')

    def saveSynergiesTable(request):
        if request.method == 'POST':
            tblFile = open(os.path.join(settings.BASE_DIR, 'synergyTable.txt'), "w")

            returnedTable = {}
            tblFile.write(request.POST["textualTbl"])

            tblFile.close()

            return HttpResponse('ok')
        return HttpResponse('error')

    def resetSimWeek(request):
        if request.method == 'POST':
            server_state_model_bridge.set_simulation_week(0)
            playersIds = player_bridge.get_all_stored_student_usernames()
            for playerId in playersIds:
                Views.delete_user(playerId)

            taskIds = task_bridge.get_all_stored_task_ids()
            for taskId in taskIds:
                Views.deleteTask(taskId)

            #serverStateModelBridge.setSimIsLinkShared(False)
            #serverStateModelBridge.setSimIsTaskCreated(False)
            #serverStateModelBridge.setSimWeekOneUsersEvaluated(False)
            #serverStateModelBridge.setSimSimulateReaction(False)
            Views.init_server(request)
            return HttpResponse('ok')

        return HttpResponse('error')

    def advanceSimWeek(request):
        simulationWeek = server_state_model_bridge.get_simulation_week()
        simSimulateReaction = server_state_model_bridge.get_sim_simulate_reaction()
        simWeekOneUsersEvaluated = server_state_model_bridge.get_sim_week_one_users_evaluated()
        if request.method == 'POST':
            if (simulationWeek > 5):
                simulationWeek = 6
            else:
                simulationWeek += 1

            if (simulationWeek == 1):
                players = player_bridge.get_all_stored_student_usernames()
                tasks = task_bridge.get_all_stored_task_ids()
                if (len(players) >= 12 and len(tasks) >= 16):
                    server_state_model_bridge.set_sim_student_to_evaluate(players[0])
                else:
                    simulationWeek -= 1

            if (simulationWeek == 2):
                if (simWeekOneUsersEvaluated):
                    server_state_model_bridge.set_sim_unavailable_student(
                        player_bridge.get_all_stored_student_usernames()[10])
                else:
                    simulationWeek -= 1

            if (simulationWeek == 3):
                if (not simSimulateReaction):
                    simulationWeek -= 1
                else:
                    simSimulateReaction = False

            if (simulationWeek == 5):
                if (simSimulateReaction):
                    simSimulateReaction = False
                else:
                    simulationWeek -= 1

            server_state_model_bridge.set_simulation_week(simulationWeek)
            server_state_model_bridge.set_sim_simulate_reaction(simSimulateReaction)
            return HttpResponse('ok')

        return HttpResponse('error')

    def shareLinkSim(request):
        if request.method == 'POST':
            server_state_model_bridge.set_sim_is_link_shared(True)
            for _ in range(int(request.POST['numUsersToGenerate'])):
                time.sleep(random.uniform(float(request.POST['minDelay']), float(request.POST['maxDelay'])))

                name = "".join(random.choice(names) + " " + random.choice(names))

                randNumber = random.random()
                if (randNumber <= 0.333333):
                    gender = 'Male'

                elif (randNumber >= 0.6666666):
                    gender = 'Female'

                else:
                    gender = 'Other'

                httpRequest = HttpRequest()
                httpRequest.method = 'POST'

                httpRequest.POST['fullName'] = name
                name = name.replace(" ", "_")
                httpRequest.POST['username'] = name
                httpRequest.POST['role'] = role
                name = name.replace("_", ".").lower()
                httpRequest.POST['email'] = name + '@tecnico.ulisboa.pt'
                httpRequest.POST['password1'] = password
                httpRequest.POST['password2'] = password
                httpRequest.POST['age'] = age
                httpRequest.POST['gender'] = gender
                httpRequest.POST['description'] = description
                httpRequest.POST['Create User'] = createUser

                httpRequest.user = request.user

                Views.user_registration(httpRequest)

            return HttpResponse('ok')

        return HttpResponse('error')

    def taskRegistrationSim(request):
        if request.method == 'POST':
            today = date.today()
            initWeek2 = today + timedelta(days=7)
            initWeek3 = initWeek2 + timedelta(days=7)
            initWeek4 = initWeek3 + timedelta(days=7)

            strInitWeek1 = str(today)
            strInitWeek2 = str(initWeek2)
            strInitWeek3 = str(initWeek3)
            strInitWeek4 = str(initWeek4)

            initDate = [today, today, today, initWeek2, initWeek2, initWeek2, initWeek2, initWeek3, initWeek3,
                        initWeek3, initWeek3, initWeek4, initWeek4, initWeek4, initWeek4]

            strInitDate = [strInitWeek1, strInitWeek1, strInitWeek1, strInitWeek2, strInitWeek2, strInitWeek2,
                           strInitWeek2, strInitWeek3, strInitWeek3, strInitWeek3, strInitWeek3, strInitWeek4,
                           strInitWeek4, strInitWeek4, strInitWeek4]
            strFinalDate = []
            for j in initDate:
                strFinalDate.append(str(j + timedelta(days=7)))

            for i in range(len(taskIds)):
                time.sleep(random.uniform(float(request.POST['minDelay']), float(request.POST['maxDelay'])))

                httpRequest = HttpRequest()
                httpRequest.method = 'POST'

                httpRequest.POST['taskId'] = taskIds[i]
                httpRequest.POST['description'] = description
                httpRequest.POST['difficulty'] = minReqAbility[i]
                httpRequest.POST['taskSelectWeigths'] = taskSelectWeigths
                httpRequest.POST['initDate'] = strInitDate[i]
                httpRequest.POST['finalDate'] = strFinalDate[i]
                httpRequest.POST['profileDim0'] = profileDim0[i]
                httpRequest.POST['profileDim1'] = profileDim1[i]

                httpRequest.user = request.user

                Views.taskRegistration(httpRequest)

            return HttpResponse('ok')

        return HttpResponse('error')

    def evaluateSim(request):
        if request.method == 'POST':

            currSelectedUsers = server_state_model_bridge.get_curr_selected_users()
            currSelectedUsers.pop(0)
            for playerId in currSelectedUsers:
                prevState = player_bridge.get_player_states_data_frame(playerId).states[-1]
                newState = Views.calc_reaction(
                    player_bridge=player_bridge,
                    state=prevState,
                    player_id=playerId)

                Views.savePlayerCharacteristics(playerId, newState.characteristics.ability,
                                                newState.characteristics.engagement)

            server_state_model_bridge.set_sim_week_one_users_evaluated(True)
            return HttpResponse('ok')

        return HttpResponse('error')
