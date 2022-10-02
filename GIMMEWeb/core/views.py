import http
import sys
import os
import json

import random
import string
import copy
import time

from datetime import datetime, date, time, timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseServerError

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect


from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages

from GIMMEWeb.core.models import UserProfile
from GIMMEWeb.core.models import Task
from GIMMEWeb.core.models import ServerState
from GIMMEWeb.core.forms import CreateUserForm, CreateUserProfileForm, CreateTaskForm, UpdateUserForm, UpdateUserProfileForm, UpdateTaskForm

from GIMMECore import *




class ServerStateModelBridge():

	def getCurrAdaptationState(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
			
		currAdaptationState = json.loads(serverState.currAdaptationState)
		return currAdaptationState
		
	def isReadyForNewActivity(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
			
		readyForNewActivity = json.loads(serverState.readyForNewActivity)
		return readyForNewActivity
	
	def getCurrSelectedUsers(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
			
		currSelectedUsers = json.loads(serverState.currSelectedUsers)
		return currSelectedUsers
		
	def getCurrFreeUsers(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
			
		currFreeUsers = json.loads(serverState.currFreeUsers)
		return currFreeUsers
		
	def getCurrSelectedTasks(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
			
		currSelectedTasks = json.loads(serverState.currSelectedTasks)
		return currSelectedTasks
	
	def getCurrFreeTasks(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
			
		currFreeTasks = json.loads(serverState.currFreeTasks)
		return currFreeTasks
	
	def getSimulationWeek(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		return serverState.simulationWeek
	def getSimSimulateReaction(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		return serverState.simSimulateReaction
	def getSimWeekOneUsersEvaluated(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		return serverState.simWeekOneUsersEvaluated
	def getSimStudentX(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		return serverState.simStudentX
	def getSimStudentY(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		return serverState.simStudentY
	def getSimStudentW(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		return serverState.simStudentW
	def getSimStudentZ(self):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		return serverState.simStudentZ
		
	def getSimFlags(self):
		serverState = ServerState.objects.first()
		serverStateSimData = {
			"simIsLinkShared" : serverState.simIsLinkShared,
			"simIsTaskCreated" : serverState.simIsTaskCreated,
			"simWeekOneUsersEvaluated" : serverState.simWeekOneUsersEvaluated,
			"simSimulateReaction" : serverState.simSimulateReaction,
			"simWeekFourDoneOnce" : serverState.simWeekFourDoneOnce,
			"simulationWeek" : serverState.simulationWeek,
			"simStudentToEvaluate" : serverState.simStudentToEvaluate,
			"simUnavailableStudent" : serverState.simUnavailableStudent,
			"simStudentX" : serverState.simStudentX,
			"simStudentY" : serverState.simStudentY,
			"simStudentW" : serverState.simStudentW,
			"simStudentZ" : serverState.simStudentZ,
		}
		return serverStateSimData


	def setCurrAdaptationState(self, currAdaptationState):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currAdaptationState = json.dumps(currAdaptationState, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currAdaptationState = currAdaptationState
		serverState.save()

	def setReadyForNewActivity(self, readyForNewActivity):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			readyForNewActivity = json.dumps(readyForNewActivity, default=lambda o: o.__dict__, sort_keys=True)
			serverState.readyForNewActivity = readyForNewActivity
		serverState.save()
		

	def setCurrSelectedUsers(self, currSelectedUsers):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currSelectedUsers = json.dumps(currSelectedUsers, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currSelectedUsers = currSelectedUsers
		serverState.save()

	def setCurrFreeUsers(self, currFreeUsers):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currFreeUsers = json.dumps(currFreeUsers, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currFreeUsers = currFreeUsers
		serverState.save()


	def setCurrSelectedTasks(self, currSelectedTasks):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currSelectedTasks = json.dumps(currSelectedTasks, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currSelectedTasks = currSelectedTasks
		serverState.save()
	def setCurrFreeTasks(self, currFreeTasks):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currFreeTasks = json.dumps(currFreeTasks, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currFreeTasks = currFreeTasks
		serverState.save()
		
		
	def setSimIsLinkShared(self, simIsLinkShared):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simIsLinkShared = simIsLinkShared
		serverState.save()
	def setSimIsTaskCreated(self, simIsTaskCreated):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simIsTaskCreated = simIsTaskCreated
		serverState.save()
	def setSimWeekOneUsersEvaluated(self, simWeekOneUsersEvaluated):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simWeekOneUsersEvaluated = simWeekOneUsersEvaluated
		serverState.save()
	def setSimSimulateReaction(self, simSimulateReaction):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simSimulateReaction = simSimulateReaction
		serverState.save()
	def setSimWeekFourDoneOnce(self, simWeekFourDoneOnce):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simWeekFourDoneOnce = simWeekFourDoneOnce
		serverState.save()
	def setSimulationWeek(self, simulationWeek):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simulationWeek = simulationWeek
		serverState.save()
	def setSimStudentToEvaluate(self, simStudentToEvaluate):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simStudentToEvaluate = simStudentToEvaluate
		serverState.save()
	def setSimUnavailableStudent(self, simUnavailableStudent):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simUnavailableStudent = simUnavailableStudent
		serverState.save()
	def setSimStudentX(self, simStudentX):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simStudentX = simStudentX
		serverState.save()
	def setSimStudentY(self, simStudentY):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simStudentY = simStudentY
		serverState.save()
	def setSimStudentZ(self, simStudentZ):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simStudentZ = simStudentZ
		serverState.save()
	def setSimStudentW(self, simStudentW):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			serverState.simStudentW = simStudentW
		serverState.save()
		

serverStateModelBridge = ServerStateModelBridge()



class CustomTaskModelBridge(TaskModelBridge):
	

	def saveTask(self, task):
		task.save()

	def getTask(self, taskId):
		return Task.objects.get(taskId = taskId)

	def removeTask(self, taskId):
		task = Task.objects.get(taskId=taskId)
		task.delete()

	def getAllTaskIds(self): #all tasks for adaptation
		return serverStateModelBridge.getCurrSelectedTasks()

	def getAllStoredTaskIds(self):
		allTasks = Task.objects.all()
		allTasksIds = []
		for task in allTasks:
			allTasksIds.append(str(task.taskId))
		return allTasksIds

	def getTaskInteractionsProfile(self, taskId):
		task = Task.objects.get(taskId = taskId)
		return InteractionsProfile(dimensions = json.loads(task.profile)['dimensions'])

	def getMinTaskRequiredAbility(self, taskId):
		task = Task.objects.get(taskId = taskId)
		return float(task.minReqAbility)


	def getMinTaskDuration(self, taskId):
		pass

	def getTaskDifficultyWeight(self, taskId):
		task = Task.objects.get(taskId = taskId)
		return float(task.difficultyWeight)

	def getTaskProfileWeight(self, taskId):
		task = Task.objects.get(taskId = taskId)
		return float(task.profileWeight)


	def getTaskInitDate(self, taskId):
		task = Task.objects.get(taskId = taskId)
		return task.initDate

	def getTaskFinalDate(self, taskId):
		task = Task.objects.get(taskId = taskId)
		return task.finalDate


	def getTaskFilePaths(self, taskId):
		task = Task.objects.get(taskId = taskId)
		return task.filePaths

taskBridge = CustomTaskModelBridge()



class CustomPlayerModelBridge(PlayerModelBridge):
	
	def getPlayer(self, username):
		return User.objects.get(username = username).userprofile

	def setAndSavePlayerStateToDataFrame(self, username, newState):
		self.setPlayerCharacteristics(username, newState.characteristics)
		self.setPlayerProfile(username, newState.profile)

		playerStatesDataFrame = self.getPlayerStatesDataFrame(username)
		playerStatesDataFrame.pushToDataFrame(newState)

		playerInfo = User.objects.get(username=username).userprofile
		playerInfo.pastModelIncreasesDataFrame = json.dumps(playerStatesDataFrame, default=lambda o: o.__dict__)
		playerInfo.save()


	def resetPlayer(self, username):
		return 0


	def getAllPlayerIds(self): #allPlayers for adaptation
		return serverStateModelBridge.getCurrSelectedUsers()

	def getAllStoredStudentUsernames(self):
		allUsers = User.objects.all()
		allUsersIds = []
		for player in allUsers:
			if 'student' in player.userprofile.role:
				allUsersIds.append(player.username)
		return allUsersIds

	def getPlayerName(self, username):
		player = User.objects.get(username=username)
		return player.username

	def getPlayerEmail(self, username):
		player = User.objects.get(username=username)
		return player.email
	
	def getPlayerCurrProfile(self,  username):
		playerInfo = User.objects.get(username=username).userprofile
		# print(json.dumps(player, default= lambda o: o.__dict__, sort_keys=True))
		profile = json.loads(playerInfo.currState)['profile']
		profile = InteractionsProfile(dimensions= profile['dimensions'])
		return profile

	def getPlayerCurrGroup(self,  username):
		playerInfo = User.objects.get(username=username).userprofile
		group = json.loads(playerInfo.currState)['group']
		return group

	def getPlayerCurrTasks(self,  username):
		playerInfo = User.objects.get(username=username).userprofile
		tasks = json.loads(playerInfo.currState)['tasks']
		return tasks
	
	def getPlayerStatesDataFrame(self, username):
		playerInfo = User.objects.get(username=username).userprofile
		pastModelIncreasesDataFrame = json.loads(playerInfo.pastModelIncreasesDataFrame)

		states = []
		for state in pastModelIncreasesDataFrame['states']:
			characteristics = state['characteristics']
			characteristics = PlayerCharacteristics(
				ability= float(characteristics['ability']), 
				engagement= float(characteristics['engagement']))

			profile = state['profile']
			profile = InteractionsProfile(dimensions= profile['dimensions'])
			
			playerState = PlayerState(profile = profile, 
				characteristics = characteristics, 
				dist=state['dist'], 
				quality=state['quality'])
			
			playerState.creationTime = -1
			states.append(playerState)

		trimAlg = json.loads(json.dumps(pastModelIncreasesDataFrame['trimAlg']))
		sdf = PlayerStatesDataFrame(
				states = states,
				interactionsProfileTemplate = intProfTemplate.generateCopy().reset(), 
				trimAlg = ProximitySortPlayerDataTrimAlg(
					maxNumModelElements = int(trimAlg['maxNumModelElements']), 
					epsilon = float(trimAlg['epsilon'])
				)
			)
		return sdf


	def getPlayerCurrCharacteristics(self, username):
		playerInfo = User.objects.get(username=username).userprofile
		characteristics = json.loads(playerInfo.currState)['characteristics']
		return PlayerCharacteristics(ability= float(characteristics['ability']), 
			engagement= float(characteristics['engagement']))

	def getPlayerGrade(self, username):
		playerInfo = User.objects.get(username=username).userprofile
		return playerInfo.grade;

	
	def getPlayerPreferencesEst(self, username):
		playerInfo = User.objects.get(username=username).userprofile
		preferences = json.loads(playerInfo.preferences)
		preferences = InteractionsProfile(dimensions= preferences['dimensions'])
		return preferences

	def getPlayerCurrState(self, username):
		playerInfo = User.objects.get(username=username).userprofile
		currState = json.loads(playerInfo.currState)
		return PlayerState(profile = self.getPlayerCurrProfile(username), 
			characteristics = self.getPlayerCurrCharacteristics(username), 
			dist = currState['dist'],
			quality = currState['quality'],
			group = currState['group'],
			tasks = currState['tasks'])

	def getPlayerFullName(self, username):
		playerInfo = User.objects.get(username=username).userprofile
		return playerInfo.fullName


	def resetPlayerCurrState(self, username):
		playerInfo = User.objects.get(username=username).userprofile
		newState = PlayerState()
		playerInfo.currState = json.dumps(newState, default=lambda o: o.__dict__)
		playerInfo.save()

	def resetPlayerPastModelIncreases(self, username):
		playerStatesDataFrame = self.getPlayerStatesDataFrame(username)
		
		self.setPlayerCharacteristics(username, PlayerCharacteristics())
		self.setPlayerProfile(username, playerStatesDataFrame.interactionsProfileTemplate.generateCopy())
		
		playerStatesDataFrame.reset()
		

		playerInfo = User.objects.get(username=username).userprofile
		playerInfo.pastModelIncreasesDataFrame = json.dumps(playerStatesDataFrame, default=lambda o: o.__dict__)
		playerInfo.save()

	def setPlayerPreferencesEst(self, username, preferences):
		playerInfo = User.objects.get(username=username).userprofile
		playerInfo.preferences = json.dumps(preferences, default=lambda o: o.__dict__)
		playerInfo.save()


	def setPlayerCharacteristics(self, username, characteristics):
		playerInfo = User.objects.get(username=username).userprofile
		newState = self.getPlayerCurrState(username)
		newState.characteristics = characteristics
		playerInfo.currState = json.dumps(newState, default=lambda o: o.__dict__)
		playerInfo.save()

	def setPlayerGrade(self, username, grade):
		playerInfo = User.objects.get(username=username).userprofile
		playerInfo.grade = grade
		playerInfo.save()


	def setPlayerProfile(self, username, profile):
		playerInfo = User.objects.get(username=username).userprofile
		newState = self.getPlayerCurrState(username)
		newState.profile = profile
		playerInfo.currState = json.dumps(newState, default=lambda o: o.__dict__)
		playerInfo.save()

	def setPlayerGroup(self, username, group):
		playerInfo = User.objects.get(username=username).userprofile
		newState = self.getPlayerCurrState(username)
		newState.group = group
		playerInfo.currState = json.dumps(newState, default=lambda o: o.__dict__)
		playerInfo.save()

	def setPlayerTasks(self, username, tasks):
		playerInfo = User.objects.get(username=username).userprofile
		newState = self.getPlayerCurrState(username)
		newState.tasks = tasks
		playerInfo.currState = json.dumps(newState, default=lambda o: o.__dict__)
		playerInfo.save()


playerBridge = CustomPlayerModelBridge()
adaptation = Adaptation()
currConfigParams = {}

intProfTemplate = InteractionsProfile({'Challenge': 0, 'Focus': 0})
trimAlgTemplate = ProximitySortPlayerDataTrimAlg(
				maxNumModelElements = 10, 
				epsilon = 0.05
			) 

defaultConfigsAlg = RandomConfigsGen(
				playerModelBridge = playerBridge, 
				interactionsProfileTemplate = intProfTemplate.generateCopy(),
				preferredNumberOfPlayersPerGroup = 4)
adaptation.init(playerBridge, taskBridge, configsGenAlg = defaultConfigsAlg, name='GIMME')

# sim stuff

# {'csrfmiddlewaretoken': ['3GuQuFgTG1tPLHK0bvD4kO5H0c4F2keftFkiQRIcpyDbrxlEEWmjazhfmCEx0p80'], 'username': ['s17'], 'role': ['student'], 'email': ['s17@s17.com'], 'password1': ['VW8fiAUkGs7QLwn'], 'password2': ['VW8fiAUkGs7QLwn'], 'fullName': ['s17'], 'age': ['20'], 'gender': ['Male'], 'description': ['.'], 'Create User': ['Register']}
role = 'student'
password = 'VW8fiAUkGs7QLwn'
age = '20'
description = '.'
createUser = 'Register'

names = ['Abbott',  'Acevedo',  'Acosta',  'Adams',  'Adkins',  'Aguilar',  'Aguirre',  'Albert',  'Alexander',  'Alford',  'Allen',  'Allison',  'Alston',  'Alvarado',  'Alvarez',  'Anderson',  'Andrews',  'Anthony',  'Armstrong',  'Arnold',  'Ashley',  'Atkins',  'Atkinson',  'Austin',  'Avery',  'Avila',  'Ayala',  'Ayers',  'Bailey',  'Baird',  'Baker',  'Baldwin',  'Ball',  'Ballard',  'Banks',  'Barber',  'Barker',  'Barlow',  'Barnes',  'Barnett',  'Barr',  'Barrera',  'Barrett',  'Barron',  'Barry',  'Bartlett',  'Barton',  'Bass',  'Bates',  'Battle',  'Bauer',  'Baxter',  'Beach',  'Bean',  'Beard',  'Beasley',  'Beck',  'Becker',  'Bell',  'Bender',  'Benjamin',  'Bennett',  'Benson',  'Bentley',  'Benton',  'Berg',  'Berger',  'Bernard',  'Berry',  'Best',  'Bird',  'Bishop',  'Black',  'Blackburn',  'Blackwell',  'Blair',  'Blake',  'Blanchard',  'Blankenship',  'Blevins',  'Bolton',  'Bond',  'Bonner',  'Booker',  'Boone',  'Booth',  'Bowen',  'Bowers',  'Bowman',  'Boyd',  'Boyer',  'Boyle',  'Bradford',  'Bradley',  'Bradshaw',  'Brady',  'Branch',  'Bray',  'Brennan',  'Brewer',  'Bridges',  'Briggs',  'Bright',  'Britt',  'Brock',  'Brooks',  'Brown',  'Browning',  'Bruce',  'Bryan',  'Bryant',  'Buchanan',  'Buck',  'Buckley',  'Buckner',  'Bullock',  'Burch',  'Burgess',  'Burke',  'Burks',  'Burnett',  'Burns',  'Burris',  'Burt',  'Burton',  'Bush',  'Butler',  'Byers',  'Byrd',  'Cabrera',  'Cain',  'Calderon',  'Caldwell',  'Calhoun',  'Callahan',  'Camacho',  'Cameron',  'Campbell',  'Campos',  'Cannon',  'Cantrell',  'Cantu',  'Cardenas',  'Carey',  'Carlson',  'Carney',  'Carpenter',  'Carr',  'Carrillo',  'Carroll',  'Carson',  'Carter',  'Carver',  'Case',  'Casey',  'Cash',  'Castaneda',  'Castillo',  'Castro',  'Cervantes',  'Chambers',  'Chan',  'Chandler',  'Chaney',  'Chang',  'Chapman',  'Charles',  'Chase',  'Chavez',  'Chen',  'Cherry',  'Christensen',  'Christian',  'Church',  'Clark',  'Clarke',  'Clay',  'Clayton',  'Clements',  'Clemons',  'Cleveland',  'Cline',  'Cobb',  'Cochran',  'Coffey',  'Cohen',  'Cole',  'Coleman',  'Collier',  'Collins',  'Colon',  'Combs',  'Compton',  'Conley',  'Conner',  'Conrad',  'Contreras',  'Conway',  'Cook',  'Cooke',  'Cooley',  'Cooper',  'Copeland',  'Cortez',  'Cote',  'Cotton',  'Cox',  'Craft',  'Craig',  'Crane',  'Crawford',  'Crosby',  'Cross',  'Cruz',  'Cummings',  'Cunningham',  'Curry',  'Curtis',  'Dale',  'Dalton',  'Daniel',  'Daniels',  'Daugherty',  'Davenport',  'David',  'Davidson',  'Davis',  'Dawson',  'Day',  'Dean',  'Decker',  'Dejesus',  'Delacruz',  'Delaney',  'Deleon',  'Delgado',  'Dennis',  'Diaz',  'Dickerson',  'Dickson',  'Dillard',  'Dillon',  'Dixon',  'Dodson',  'Dominguez',  'Donaldson',  'Donovan',  'Dorsey',  'Dotson',  'Douglas',  'Downs',  'Doyle',  'Drake',  'Dudley',  'Duffy',  'Duke',  'Duncan',  'Dunlap',  'Dunn',  'Duran',  'Durham',  'Dyer',  'Eaton',  'Edwards',  'Elliott',  'Ellis',  'Ellison',  'Emerson',  'England',  'English',  'Erickson',  'Espinoza',  'Estes',  'Estrada',  'Evans',  'Everett',  'Ewing',  'Farley',  'Farmer',  'Farrell',  'Faulkner',  'Ferguson',  'Fernandez',  'Ferrell',  'Fields',  'Figueroa',  'Finch',  'Finley',  'Fischer',  'Fisher',  'Fitzgerald',  'Fitzpatrick',  'Fleming',  'Fletcher',  'Flores',  'Flowers',  'Floyd',  'Flynn',  'Foley',  'Forbes',  'Ford',  'Foreman',  'Foster',  'Fowler',  'Fox',  'Francis',  'Franco',  'Frank',  'Franklin',  'Franks',  'Frazier',  'Frederick',  'Freeman',  'French',  'Frost',  'Fry',  'Frye',  'Fuentes',  'Fuller',  'Fulton',  'Gaines',  'Gallagher',  'Gallegos',  'Galloway',  'Gamble',  'Garcia',  'Gardner',  'Garner',  'Garrett',  'Garrison',  'Garza',  'Gates',  'Gay',  'Gentry',  'George',  'Gibbs',  'Gibson',  'Gilbert',  'Giles',  'Gill',  'Gillespie',  'Gilliam',  'Gilmore',  'Glass',  'Glenn',  'Glover',  'Goff',  'Golden',  'Gomez',  'Gonzales',  'Gonzalez',  'Good',  'Goodman',  'Goodwin',  'Gordon',  'Gould',  'Graham',  'Grant',  'Graves',  'Gray',  'Green',  'Greene',  'Greer',  'Gregory',  'Griffin',  'Griffith',  'Grimes',  'Gross',  'Guerra',  'Guerrero',  'Guthrie',  'Gutierrez',  'Guy',  'Guzman',  'Hahn',  'Hale',  'Haley',  'Hall',  'Hamilton',  'Hammond',  'Hampton',  'Hancock',  'Haney',  'Hansen',  'Hanson',  'Hardin',  'Harding',  'Hardy',  'Harmon',  'Harper',  'Harrell',  'Harrington',  'Harris',  'Harrison',  'Hart',  'Hartman',  'Harvey',  'Hatfield',  'Hawkins',  'Hayden',  'Hayes',  'Haynes',  'Hays',  'Head',  'Heath',  'Hebert',  'Henderson',  'Hendricks',  'Hendrix',  'Henry',  'Hensley',  'Henson',  'Herman',  'Hernandez',  'Herrera',  'Herring',  'Hess',  'Hester',  'Hewitt',  'Hickman',  'Hicks',  'Higgins',  'Hill',  'Hines',  'Hinton',  'Hobbs',  'Hodge',  'Hodges',  'Hoffman',  'Hogan',  'Holcomb',  'Holden',  'Holder',  'Holland',  'Holloway',  'Holman',  'Holmes',  'Holt',  'Hood',  'Hooper',  'Hoover',  'Hopkins',  'Hopper',  'Horn',  'Horne',  'Horton',  'House',  'Houston',  'Howard',  'Howe',  'Howell',  'Hubbard',  'Huber',  'Hudson',  'Huff',  'Huffman',  'Hughes',  'Hull',  'Humphrey',  'Hunt',  'Hunter',  'Hurley',  'Hurst',  'Hutchinson',  'Hyde',  'Ingram',  'Irwin',  'Jackson',  'Jacobs',  'Jacobson',  'James',  'Jarvis',  'Jefferson',  'Jenkins',  'Jennings',  'Jensen',  'Jimenez',  'Johns',  'Johnson',  'Johnston',  'Jones',  'Jordan',  'Joseph',  'Joyce',  'Joyner',  'Juarez',  'Justice',  'Kane',  'Kaufman',  'Keith',  'Keller',  'Kelley',  'Kelly',  'Kemp',  'Kennedy',  'Kent',  'Kerr',  'Key',  'Kidd',  'Kim',  'King',  'Kinney',  'Kirby',  'Kirk',  'Kirkland',  'Klein',  'Kline',  'Knapp',  'Knight',  'Knowles',  'Knox',  'Koch',  'Kramer',  'Lamb',  'Lambert',  'Lancaster',  'Landry',  'Lane',  'Lang',  'Langley',  'Lara',  'Larsen',  'Larson',  'Lawrence',  'Lawson',  'Le',  'Leach',  'Leblanc',  'Lee',  'Leon',  'Leonard',  'Lester',  'Levine',  'Levy',  'Lewis',  'Lindsay',  'Lindsey',  'Little',  'Livingston',  'Lloyd',  'Logan',  'Long',  'Lopez',  'Lott',  'Love',  'Lowe',  'Lowery',  'Lucas',  'Luna',  'Lynch',  'Lynn',  'Lyons',  'Macdonald',  'Macias',  'Mack',  'Madden',  'Maddox',  'Maldonado',  'Malone',  'Mann',  'Manning',  'Marks',  'Marquez',  'Marsh',  'Marshall',  'Martin',  'Martinez',  'Mason',  'Massey',  'Mathews',  'Mathis',  'Matthews',  'Maxwell',  'May',  'Mayer',  'Maynard',  'Mayo',  'Mays',  'Mcbride',  'Mccall',  'Mccarthy',  'Mccarty',  'Mcclain',  'Mcclure',  'Mcconnell',  'Mccormick',  'Mccoy',  'Mccray',  'Mccullough',  'Mcdaniel',  'Mcdonald',  'Mcdowell',  'Mcfadden',  'Mcfarland',  'Mcgee',  'Mcgowan',  'Mcguire',  'Mcintosh',  'Mcintyre',  'Mckay',  'Mckee',  'Mckenzie',  'Mckinney',  'Mcknight',  'Mclaughlin',  'Mclean',  'Mcleod',  'Mcmahon',  'Mcmillan',  'Mcneil',  'Mcpherson',  'Meadows',  'Medina',  'Mejia',  'Melendez',  'Melton',  'Mendez',  'Mendoza',  'Mercado',  'Mercer',  'Merrill',  'Merritt',  'Meyer',  'Meyers',  'Michael',  'Middleton',  'Miles',  'Miller',  'Mills',  'Miranda',  'Mitchell',  'Molina',  'Monroe',  'Montgomery',  'Montoya',  'Moody',  'Moon',  'Mooney',  'Moore',  'Morales',  'Moran',  'Moreno',  'Morgan',  'Morin',  'Morris',  'Morrison',  'Morrow',  'Morse',  'Morton',  'Moses',  'Mosley',  'Moss',  'Mueller',  'Mullen',  'Mullins',  'Munoz',  'Murphy',  'Murray',  'Myers',  'Nash',  'Navarro',  'Neal',  'Nelson',  'Newman',  'Newton',  'Nguyen',  'Nichols',  'Nicholson',  'Nielsen',  'Nieves',  'Nixon',  'Noble',  'Noel',  'Nolan',  'Norman',  'Norris',  'Norton',  'Nunez',  'Obrien',  'Ochoa',  'Oconnor',  'Odom',  'Odonnell',  'Oliver',  'Olsen',  'Olson',  'Oneal',  'Oneil',  'Oneill',  'Orr',  'Ortega',  'Ortiz',  'Osborn',  'Osborne',  'Owen',  'Owens',  'Pace',  'Pacheco',  'Padilla',  'Page',  'Palmer',  'Park',  'Parker',  'Parks',  'Parrish',  'Parsons',  'Pate',  'Patel',  'Patrick',  'Patterson',  'Patton',  'Paul',  'Payne',  'Pearson',  'Peck',  'Pena',  'Pennington',  'Perez',  'Perkins',  'Perry',  'Peters',  'Petersen',  'Peterson',  'Petty',  'Phelps',  'Phillips',  'Pickett',  'Pierce',  'Pittman',  'Pitts',  'Pollard',  'Poole',  'Pope',  'Porter',  'Potter',  'Potts',  'Powell',  'Powers',  'Pratt',  'Preston',  'Price',  'Prince',  'Pruitt',  'Puckett',  'Pugh',  'Quinn',  'Ramirez',  'Ramos',  'Ramsey',  'Randall',  'Randolph',  'Rasmussen',  'Ratliff',  'Ray',  'Raymond',  'Reed',  'Reese',  'Reeves',  'Reid',  'Reilly',  'Reyes',  'Reynolds',  'Rhodes',  'Rice',  'Rich',  'Richard',  'Richards',  'Richardson',  'Richmond',  'Riddle',  'Riggs',  'Riley',  'Rios',  'Rivas',  'Rivera',  'Rivers',  'Roach',  'Robbins',  'Roberson',  'Roberts',  'Robertson',  'Robinson',  'Robles',  'Rocha',  'Rodgers',  'Rodriguez',  'Rodriquez',  'Rogers',  'Rojas',  'Rollins',  'Roman',  'Romero',  'Rosa',  'Rosales',  'Rosario',  'Rose',  'Ross',  'Roth',  'Rowe',  'Rowland',  'Roy',  'Ruiz',  'Rush',  'Russell',  'Russo',  'Rutledge',  'Ryan',  'Salas',  'Salazar',  'Salinas',  'Sampson',  'Sanchez',  'Sanders',  'Sandoval',  'Sanford',  'Santana',  'Santiago',  'Santos',  'Sargent',  'Saunders',  'Savage',  'Sawyer',  'Schmidt',  'Schneider',  'Schroeder',  'Schultz',  'Schwartz',  'Scott',  'Sears',  'Sellers',  'Serrano',  'Sexton',  'Shaffer',  'Shannon',  'Sharp',  'Sharpe',  'Shaw',  'Shelton',  'Shepard',  'Shepherd',  'Sheppard',  'Sherman',  'Shields',  'Short',  'Silva',  'Simmons',  'Simon',  'Simpson',  'Sims',  'Singleton',  'Skinner',  'Slater',  'Sloan',  'Small',  'Smith',  'Snider',  'Snow',  'Snyder',  'Solis',  'Solomon',  'Sosa',  'Soto',  'Sparks',  'Spears',  'Spence',  'Spencer',  'Stafford',  'Stanley',  'Stanton',  'Stark',  'Steele',  'Stein',  'Stephens',  'Stephenson',  'Stevens',  'Stevenson',  'Stewart',  'Stokes',  'Stone',  'Stout',  'Strickland',  'Strong',  'Stuart',  'Suarez',  'Sullivan',  'Summers',  'Sutton',  'Swanson',  'Sweeney',  'Sweet',  'Sykes',  'Talley',  'Tanner',  'Tate',  'Taylor',  'Terrell',  'Terry',  'Thomas',  'Thompson',  'Thornton',  'Tillman',  'Todd',  'Torres',  'Townsend',  'Tran',  'Travis',  'Trevino',  'Trujillo',  'Tucker',  'Turner',  'Tyler',  'Tyson',  'Underwood',  'Valdez',  'Valencia',  'Valentine',  'Valenzuela',  'Vance',  'Vang',  'Vargas',  'Vasquez',  'Vaughan',  'Vaughn',  'Vazquez',  'Vega',  'Velasquez',  'Velazquez',  'Velez',  'Villarreal',  'Vincent',  'Vinson',  'Wade',  'Wagner',  'Walker',  'Wall',  'Wallace',  'Waller',  'Walls',  'Walsh',  'Walter',  'Walters',  'Walton',  'Ward',  'Ware',  'Warner',  'Warren',  'Washington',  'Waters',  'Watkins',  'Watson',  'Watts',  'Weaver',  'Webb',  'Weber',  'Webster',  'Weeks',  'Weiss',  'Welch',  'Wells',  'West',  'Wheeler',  'Whitaker',  'White',  'Whitehead',  'Whitfield',  'Whitley',  'Whitney',  'Wiggins',  'Wilcox',  'Wilder',  'Wiley',  'Wilkerson',  'Wilkins',  'Wilkinson',  'William',  'Williams',  'Williamson',  'Willis',  'Wilson',  'Winters',  'Wise',  'Witt',  'Wolf',  'Wolfe',  'Wong',  'Wood',  'Woodard',  'Woods',  'Woodward',  'Wooten',  'Workman',  'Wright',  'Wyatt',  'Wynn',  'Yang',  'Yates',  'York',  'Young',  'Zamora',  'Zimmerman']

#<QueryDict: {'csrfmiddlewaretoken': ['4CaVMCovQl2IbysucPRCKrUxuVNRe4Tcr6LUcSxhaftsnuHiO8HXlGZW3gTx4tkF'], 'taskId': ['week 1'], 'description': ['test'], 'minReqAbility': ['0.3'], 'profileWeight': ['0.5'], 'difficultyWeight': ['0.5'], 'initDate': ['2022-07-20'], 'finalDate': ['2022-07-27'], 'profileDim0': ['0'], 'profileDim1': ['0']}>
#<MultiValueDict: {'files': [<InMemoryUploadedFile: testTask_BBn7DVn.png (image/png)>]}>
taskIds = ["week1_01", "week1_10", "week1_11", "week2_00", "week2_01", "week2_10", "week2_11", "week3_00", "week3_01", "week3_10", "week3_11", "week4_00", "week4_01", "week4_10", "week4_11", "week5_00", "week5_01", "week5_10", "week5_11"]
description = '.'

minReqAbility = ["0.2", "0.2", "0.2", "0.3", "0.3", "0.3", "0.3", "0.5", "0.5", "0.5", "0.5", "0.6", "0.6", "0.6", "0.6", "0.7", "0.7", "0.7", "0.7"]
profileWeight = '0.5'
difficultyWeight = '0.5'

profileDim0 = ['0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1', '0', '0', '1', '1']
profileDim1 = ['1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1']

class Views(): #acts as a namespace

	def initServer(request):
		
		serverStateModelBridge.setCurrAdaptationState([])
		serverStateModelBridge.setReadyForNewActivity(True)
		serverStateModelBridge.setCurrSelectedUsers([])
		serverStateModelBridge.setCurrFreeUsers(playerBridge.getAllStoredStudentUsernames())
		serverStateModelBridge.setCurrSelectedTasks([])
		serverStateModelBridge.setCurrFreeTasks(taskBridge.getAllStoredTaskIds())


		serverStateModelBridge.setSimIsLinkShared(False)
		serverStateModelBridge.setSimIsTaskCreated(False)
		serverStateModelBridge.setSimWeekOneUsersEvaluated(False)
		serverStateModelBridge.setSimSimulateReaction(False)
		serverStateModelBridge.setSimWeekFourDoneOnce(False)

		serverStateModelBridge.setSimulationWeek(0)
		serverStateModelBridge.setSimStudentToEvaluate("")
		serverStateModelBridge.setSimUnavailableStudent("")
		serverStateModelBridge.setSimStudentX("")
		serverStateModelBridge.setSimStudentY("")
		serverStateModelBridge.setSimStudentZ("")
		serverStateModelBridge.setSimStudentW("")


		for player in playerBridge.getAllStoredStudentUsernames():
			playerBridge.resetPlayerCurrState(player)
			playerBridge.resetPlayerPastModelIncreases(player)

		return HttpResponse('ok')

	def calcReaction(playerBridge, state, playerId):
		preferences = playerBridge.getPlayerPreferencesEst(playerId)
		numDims = len(preferences.dimensions)
		newState = PlayerState(
			stateType = 1, 
			characteristics = PlayerCharacteristics(
				ability=state.characteristics.ability, 
				engagement=state.characteristics.engagement
				), 
			profile=state.profile)
		newState.characteristics.engagement = 1 - (preferences.distanceBetween(state.profile) / math.sqrt(numDims))  #between 0 and 1
		if newState.characteristics.engagement>1:
			breakpoint()
		abilityIncreaseSim = (newState.characteristics.engagement)
		newState.characteristics.ability = newState.characteristics.ability + abilityIncreaseSim
		return newState

	def simulateReaction(request):
		allUsers = playerBridge.getAllPlayerIds()
		
		simFlags = serverStateModelBridge.getSimFlags()
		
		for playerId in allUsers:
			
			prevState = playerBridge.getPlayerStatesDataFrame(playerId).states[-1]

			newState = Views.calcReaction(
				playerBridge = playerBridge, 
				state = prevState, 
				playerId = playerId)

			if simFlags['simulationWeek'] == 2:
				if playerId == simFlags['simStudentX']:
					newState.characteristics.ability = 0.3
					newState.characteristics.engagement = 0.3

				elif playerId == simFlags['simStudentY']:
					newState.characteristics.ability = 0.2
					newState.characteristics.engagement = 0.2

				elif playerId == simFlags['simStudentW']:
					newState.characteristics.engagement = 0.95
				
				elif playerId == simFlags['simStudentZ']:
					newState.characteristics.engagement = 0.95
					


			Views.savePlayerCharacteristics(playerId, newState.characteristics.ability, newState.characteristics.engagement)

		serverStateModelBridge.setSimSimulateReaction(True)
		return HttpResponse('ok')


	#global methods
	def home(request):
		Views.loginCheck(request)
		if(request.user.is_authenticated):
			return redirect('/dash')
		else:
			return render(request, 'home.html')

	def loginCheck(request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		print('[INFO] login check performed on user with id - ' + str(username) + ', password - '+str(password))

		if(username is None):
			return

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
		else:
			messages.info(request, 'Login failed! Credentials not recognized.')


	def logoutCheck(request):
		logout(request)
		return redirect('/home')
	
	
	def userRegistration(request):
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			profileForm = CreateUserProfileForm(request.POST, request.FILES)

			if form.is_valid() and profileForm.is_valid():
				user = form.save()
				
				profile = profileForm.save(commit = False)
				profile.user = user

				profile.currState = json.dumps(PlayerState(), default=lambda o: o.__dict__, sort_keys=True)
				profile.pastModelIncreasesDataFrame = json.dumps(
					PlayerStatesDataFrame(
						interactionsProfileTemplate = intProfTemplate.generateCopy().reset(), 
						trimAlg = trimAlgTemplate
					), 
				default=lambda o: o.__dict__, sort_keys=True)
				profile.preferences = json.dumps(intProfTemplate.generateCopy().reset(), default=lambda o: o.__dict__, sort_keys=True)

				profile.save() 

				if 'student' in profile.role:
					currFreeUsers = serverStateModelBridge.getCurrFreeUsers();
					currFreeUsers.append(user.username)
					serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
					playerBridge.setPlayerGrade(user.username, 0)
					

				if(not request.user.is_authenticated):
					login(request, user)
				return redirect('/dash')
			else:
				context = { 'form' : form , 'profileForm': profileForm }
				return render(request, 'userRegistration.html', context)

		elif request.method == 'GET':
			form = CreateUserForm()
			profileForm = CreateUserProfileForm()

			context = { 'form' : form , 'profileForm': profileForm }
			return render(request, 'userRegistration.html', context)

	
	def userUpdate(request):
		if request.method == 'POST':

			instance = request.user
			usernameToUpdate = request.GET.get('usernameToUpdate')
			if(usernameToUpdate):
				try:
					instance = User.objects.get(username=usernameToUpdate)
				except User.DoesNotExist:
					messages.info(request, 'Account not updated! Username not found.')
					return redirect('/userUpdate')


			form = UpdateUserForm(request.POST, instance=instance)
			profileForm = UpdateUserProfileForm(request.POST, request.FILES, instance=instance.userprofile)

			if form.is_valid() and profileForm.is_valid():
				user = form.save()
				profile = profileForm.save()
				return redirect('/dash')
			else:
				context = { 'form' : form , 'profileForm': profileForm }
				return render(request, 'userUpdate.html',  context)

		elif request.method == 'GET':

			instance = request.user
			usernameToUpdate = request.GET.get('usernameToUpdate')
			if(usernameToUpdate):
				try:
					instance = User.objects.get(username=usernameToUpdate)
				except User.DoesNotExist:
					messages.info(request, 'Account not updated! Username not found.')
					return redirect('/userUpdate')

			form = UpdateUserForm(instance=instance)
			profileForm = UpdateUserProfileForm(instance=instance.userprofile)

			context = { 'form' : form , 'profileForm': profileForm }
			return render(request, 'userUpdate.html',  context)

	
	def userDeletion(request):
		if request.method == 'GET':
			canLogout = False
			username = request.GET.get('usernameToDelete')
			if(not username):
				username = request.user.username
				canLogout = True
			
			try:
				if canLogout:
					logout(request) #logout player before removing it
				Views.deleteUser(username)

			except User.DoesNotExist:
				messages.info(request, 'Account not deleted! Username not found.')
				return redirect('/userUpdate')

			return redirect('/home')

	def deleteUser(username):
		player = User.objects.get(username = username)
		player.delete()

		currFreeUsers = serverStateModelBridge.getCurrFreeUsers()
		if username in currFreeUsers:
			currFreeUsers.remove(username)
			serverStateModelBridge.setCurrFreeUsers(currFreeUsers)

		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers()
		if username in currSelectedUsers:
			currSelectedUsers.remove(username)
			serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)

	def isUserRegistered(username):
		returned = {}
		if(username != None):
			try:
				returned['user'] = User.objects.get(username=username).userprofile
				returned['storedUsers'] = UserProfile.objects.filter(username__contains=username)
			except ObjectDoesNotExist as e:
				print('user does not exist!')
				returned = {'user': False, 'storedUsers': User.objects.filter(username__contains=username)}
		return returned

	def dash(request):
		dashSwitch = {
			'student': 'student/dash.html',
			'professor': 'professor/dash.html',
			'designer': 'designer/dash.html'
		}
		return render(request, dashSwitch.get(str(request.user.userprofile.role)))

	
	def getRandomString(length):
		letters = string.ascii_lowercase
		numbers = '0123456789'
		chars = letters + numbers
		result_str = random.choice(numbers) + ''.join(random.choice(chars) for i in range(length))
		return result_str
	
		


	
	def addAllUsersSelected(request): #reads (player) from args
		if request.method == 'POST':
			serverStateModelBridge.setCurrSelectedUsers(serverStateModelBridge.getCurrSelectedUsers() + serverStateModelBridge.getCurrFreeUsers())
			serverStateModelBridge.setCurrFreeUsers([])
			return HttpResponse('ok')
	
	def removeAllUsersSelected(request): #reads (player) from args
		if request.method == 'POST':
			serverStateModelBridge.setCurrFreeUsers(serverStateModelBridge.getCurrSelectedUsers() + serverStateModelBridge.getCurrFreeUsers())
			serverStateModelBridge.setCurrSelectedUsers([])
			return HttpResponse('ok')

	
	def addSelectedUser(request): #reads (player) from args
		if request.method == 'POST':
			usernameToAdd = request.POST.get('username')
			currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
			currFreeUsers = serverStateModelBridge.getCurrFreeUsers();
			if not usernameToAdd in currSelectedUsers:
				currSelectedUsers.append(usernameToAdd)
				currFreeUsers.remove(usernameToAdd)
			serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
			serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
			return HttpResponse('ok')

	
	def removeSelectedUser(request): #reads (player) from args
		if request.method == 'POST':
			usernameToRemove = request.POST.get('username')
			currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
			currFreeUsers = serverStateModelBridge.getCurrFreeUsers();
			if usernameToRemove in currSelectedUsers:
				currSelectedUsers.remove(usernameToRemove)
				currFreeUsers.append(usernameToRemove)
			serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
			serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
			return HttpResponse('ok')



	
	def addAllTasksSelected(request): #reads (player) from args
		if request.method == 'POST':
			serverStateModelBridge.setCurrSelectedTasks(serverStateModelBridge.getCurrSelectedTasks() + serverStateModelBridge.getCurrFreeTasks())
			serverStateModelBridge.setCurrFreeTasks([])
			return HttpResponse('ok')
	
	def removeAllTasksSelected(request): #reads (player) from args
		if request.method == 'POST':
			serverStateModelBridge.setCurrFreeTasks(serverStateModelBridge.getCurrSelectedTasks() + serverStateModelBridge.getCurrFreeTasks())
			serverStateModelBridge.setCurrSelectedTasks([])
			return HttpResponse('ok')
	
	def addSelectedTask(request): #reads (player) from args
		if request.method == 'POST':
			taskToAdd = request.POST.get('taskId')
			currSelectedTasks = serverStateModelBridge.getCurrSelectedTasks();
			currFreeTasks = serverStateModelBridge.getCurrFreeTasks();
			if not taskToAdd in currSelectedTasks:
				currSelectedTasks.append(taskToAdd)
				currFreeTasks.remove(taskToAdd)
			serverStateModelBridge.setCurrSelectedTasks(currSelectedTasks)
			serverStateModelBridge.setCurrFreeTasks(currFreeTasks)
			return HttpResponse('ok')

	
	def removeSelectedTask(request): #reads (player) from args
		if request.method == 'POST':
			TaskIdToRemove = request.POST.get('taskId')
			currSelectedTasks = serverStateModelBridge.getCurrSelectedTasks();
			currFreeTasks = serverStateModelBridge.getCurrFreeTasks();
			if TaskIdToRemove in currSelectedTasks:
				currSelectedTasks.remove(TaskIdToRemove)
				currFreeTasks.append(TaskIdToRemove)
			serverStateModelBridge.setCurrSelectedTasks(currSelectedTasks)
			serverStateModelBridge.setCurrFreeTasks(currFreeTasks)
			return HttpResponse('ok')



	# student methods
	def startActivity(request):
		# remove from selected and move to occupied list
		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
		currFreeUsers = serverStateModelBridge.getCurrFreeUsers();

		currSelectedUsers.remove(request.session.get('username'))
		currFreeUsers.append(request.session.get('username'))
		serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
		serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
		return render(request, 'student/activity.html')

	
	def saveTaskResults(request):
		if request.POST:
			username = request.session.get('username')
			Views.savePlayerCharacteristics(username, request.POST['ability'], request.POST['engagement'])
			return Views.dash(request)

	def savePlayerCharacteristics(username, ability, engagement):
		characteristics = playerBridge.getPlayerStatesDataFrame(username).states[-1].characteristics
		abilityToSave = (float(ability) - characteristics.ability)
		
		
		simFlags = serverStateModelBridge.getSimFlags()
		if username == simFlags['simStudentX'] and simFlags['simulationWeek'] == 2:
			abilityToSave = 0.3
		elif username == simFlags['simStudentY'] and simFlags['simulationWeek'] == 2:
			abilityToSave = 0.2

		characteristics = PlayerCharacteristics(ability=abilityToSave, engagement=float(engagement))
		playerBridge.setPlayerCharacteristics(username, characteristics)
		playerBridge.setPlayerGrade(username=username, grade=round(float(playerBridge.getPlayerGrade(username=username)) + characteristics.ability / 5.0, 2))

	# professor methods
	
	def startAdaptation(request):
		serverStateModelBridge.setReadyForNewActivity(False)
		try:			
			# store current states in players' state window, after the adaptation returns
			for username in serverStateModelBridge.getCurrSelectedUsers():
				playerBridge.setAndSavePlayerStateToDataFrame(username, playerBridge.getPlayerCurrState(username))

			currAdaptationState = adaptation.iterate()

			# for username in serverStateModelBridge.getCurrSelectedUsers():
			# 	print(playerBridge.getPlayerPreferencesEst(username).dimensions)

		except (Exception, ArithmeticError, ValueError) as e:
			template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
			message = template.format(type(e).__name__, e.args)
			print(message)
			serverStateModelBridge.setReadyForNewActivity(True)
			return HttpResponse('error')
			
		simStudentX = ''
		simStudentY = ''
		simStudentW = ''
		simStudentZ = ''

		if serverStateModelBridge.getSimulationWeek() == 2 and currAdaptationState != []:
			simStudentX = currAdaptationState["groups"][0][0]
			simStudentY = currAdaptationState["groups"][0][1]

			simStudentW = currAdaptationState["groups"][1][0]
			simStudentZ = currAdaptationState["groups"][1][1]


		serverStateModelBridge.setCurrAdaptationState(currAdaptationState)
		serverStateModelBridge.setReadyForNewActivity(True)

		serverStateModelBridge.setSimStudentX(simStudentX)
		serverStateModelBridge.setSimStudentY(simStudentY)
		serverStateModelBridge.setSimStudentW(simStudentW)
		serverStateModelBridge.setSimStudentZ(simStudentZ)

		return Views.fetchServerState(request)


	def configAdaptation(request):
		
		global currConfigParams

		newConfigParams = request.POST
		if(currConfigParams == newConfigParams):
			return HttpResponse('ok')

		# switch reg algs
		selectedRegAlg = {}		
		persEstRegAlg = {}
		def selectedRegAlgSwitcherKNN(request):
			return KNNRegression( 
				playerBridge, 
				int(newConfigParams['numNNs']),
				qualityWeights = PlayerCharacteristics(ability = float(newConfigParams['qualityWeightsAb']), engagement = float(newConfigParams['qualityWeightsEng']))
			)
		def selectedRegAlgSwitcherSynergy(request):
			return TabularAgentSynergies(
				playerModelBridge = playerBridge,
				taskModelBridge = taskBridge
			)

		selectedRegAlgId = newConfigParams['selectedRegAlgId']
		# selectedRegAlg = None
		if (selectedRegAlgId =='K-Nearest-Neighbors (KNN)'):
			selectedRegAlg = selectedRegAlgSwitcherKNN(request)
			persEstRegAlg = selectedRegAlg
		elif (selectedRegAlgId == 'KNN w/ Synergy Between Students'):
			selectedRegAlg = selectedRegAlgSwitcherSynergy(request)
			persEstRegAlg = KNNRegression( 
				playerBridge, 
				int(newConfigParams['synergiesNumNNs']),
				qualityWeights = PlayerCharacteristics(
					ability = float(newConfigParams['synergiesQualityWeightsAb']), 
					engagement = float(newConfigParams['synergiesQualityWeightsEng'])
				)
			)


		selectedGenAlg = {}
		def selectedGenAlgSwitcherRandom(request):
			return RandomConfigsGen(
				playerModelBridge = playerBridge, 
				interactionsProfileTemplate = intProfTemplate.generateCopy(),
				minNumberOfPlayersPerGroup = int(newConfigParams['minNumberOfPlayersPerGroup']), 
				maxNumberOfPlayersPerGroup = int(newConfigParams['maxNumberOfPlayersPerGroup']), 
				# preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
				jointPlayerConstraints = newConfigParams['jointPlayerConstraints'],
				separatedPlayerConstraints = newConfigParams['separatedPlayerConstraints'])

		def selectedGenAlgSwitcherPRS(request):
			return PureRandomSearchConfigsGen(
						playerModelBridge = playerBridge, 
						interactionsProfileTemplate = intProfTemplate.generateCopy(), 
						regAlg = selectedRegAlg, 
						persEstAlg = ExplorationPreferencesEstAlg(
							playerModelBridge = playerBridge, 
							interactionsProfileTemplate = intProfTemplate.generateCopy(), 
							regAlg = persEstRegAlg,
							numTestedPlayerProfiles = 100),
						numberOfConfigChoices = int(newConfigParams['numberOfConfigChoices']), 
						minNumberOfPlayersPerGroup = int(newConfigParams['minNumberOfPlayersPerGroup']), 
						maxNumberOfPlayersPerGroup = int(newConfigParams['maxNumberOfPlayersPerGroup']), 
						# preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
						jointPlayerConstraints = newConfigParams['jointPlayerConstraints'],
						separatedPlayerConstraints = newConfigParams['separatedPlayerConstraints']
					)

		def selectedGenAlgSwitcherAnnealedPRS(request):
			return AnnealedPRSConfigsGen(
						playerModelBridge = playerBridge, 
						interactionsProfileTemplate = intProfTemplate.generateCopy(), 
						regAlg = selectedRegAlg, 
						persEstAlg = ExplorationPreferencesEstAlg(
							playerModelBridge = playerBridge, 
							interactionsProfileTemplate = intProfTemplate.generateCopy(), 
							regAlg = persEstRegAlg,
							numTestedPlayerProfiles = 100),
						numberOfConfigChoices = int(newConfigParams['numberOfConfigChoices']), 
						minNumberOfPlayersPerGroup = int(newConfigParams['minNumberOfPlayersPerGroup']), 
						maxNumberOfPlayersPerGroup = int(newConfigParams['maxNumberOfPlayersPerGroup']), 
						# preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
						temperatureDecay = float(newConfigParams['temperatureDecay']),
						jointPlayerConstraints = newConfigParams['jointPlayerConstraints'],
						separatedPlayerConstraints = newConfigParams['separatedPlayerConstraints']
					)

		def selectedGenAlgSwitcherEvolutionary(request):
			return EvolutionaryConfigsGenDEAP(
				playerModelBridge = playerBridge, 
				interactionsProfileTemplate = intProfTemplate.generateCopy(), 
				regAlg = selectedRegAlg, 
				persEstAlg = ExplorationPreferencesEstAlg(
					playerModelBridge = playerBridge, 
					interactionsProfileTemplate = intProfTemplate.generateCopy(), 
					regAlg = persEstRegAlg,
					numTestedPlayerProfiles = 100),

				minNumberOfPlayersPerGroup = int(newConfigParams['minNumberOfPlayersPerGroup']), 
				maxNumberOfPlayersPerGroup = int(newConfigParams['maxNumberOfPlayersPerGroup']), 
				# preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']), 
				
				initialPopulationSize = int(newConfigParams['initialPopulationSize']), 
				numberOfEvolutionsPerIteration = int(newConfigParams['numberOfEvolutionsPerIteration']), 
				
				probOfCross = float(newConfigParams['probOfCross']), 
				probOfMutation = float(newConfigParams['probOfMutation']),

				probOfMutationConfig = float(newConfigParams['probOfMutationConfig']), 
				probOfMutationGIPs = float(newConfigParams['probOfMutationGIPs']), 
				
				numChildrenPerIteration = int(newConfigParams['numChildrenPerIteration']),
				numSurvivors = int(newConfigParams['numSurvivors']),

				cxOp = "order",
				jointPlayerConstraints = newConfigParams['jointPlayerConstraints'],
				separatedPlayerConstraints = newConfigParams['separatedPlayerConstraints'])

		def selectedGenAlgSwitcherODPIP(request):
			return ODPIP(
				playerModelBridge = playerBridge,
				interactionsProfileTemplate = intProfTemplate.generateCopy(),
				regAlg = selectedRegAlg,
				persEstAlg = ExplorationPreferencesEstAlg(
					playerModelBridge = playerBridge, 
					interactionsProfileTemplate = intProfTemplate.generateCopy(), 
					regAlg = persEstRegAlg,
					numTestedPlayerProfiles = 100),

				#preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
				minNumberOfPlayersPerGroup= int(newConfigParams['minNumberOfPlayersPerGroup']),
				maxNumberOfPlayersPerGroup= int(newConfigParams['maxNumberOfPlayersPerGroup']),


				taskModelBridge = taskBridge,
				jointPlayerConstraints = newConfigParams['jointPlayerConstraints'],
				separatedPlayerConstraints = newConfigParams['separatedPlayerConstraints']
			) 

		def selectedGenAlgSwitcherCLink(request):
			return CLink(
				playerModelBridge = playerBridge,
				interactionsProfileTemplate = intProfTemplate.generateCopy(),
				regAlg = selectedRegAlg,
				persEstAlg = ExplorationPreferencesEstAlg(
					playerModelBridge = playerBridge, 
					interactionsProfileTemplate = intProfTemplate.generateCopy(), 
					regAlg = persEstRegAlg,
					numTestedPlayerProfiles = 100),

				#preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
				minNumberOfPlayersPerGroup = int(newConfigParams['minNumberOfPlayersPerGroup']), 
				maxNumberOfPlayersPerGroup = int(newConfigParams['maxNumberOfPlayersPerGroup']), 
				taskModelBridge = taskBridge
			) 

		# switch config. gen. algs
		# print(newConfigParams['selectedGenAlgId'])
		selectedGenAlgId = newConfigParams['selectedGenAlgId']
		selectedGenAlg = defaultConfigsAlg
		if (selectedGenAlgId =='Random (no search)'):
			selectedGenAlg = selectedGenAlgSwitcherRandom(request)
		elif (selectedGenAlgId =='Pure Random Search'):
			selectedGenAlg = selectedGenAlgSwitcherPRS(request)
		elif (selectedGenAlgId =='Annealed Pure Random Search'):
			selectedGenAlg = selectedGenAlgSwitcherAnnealedPRS(request)
		elif (selectedGenAlgId =='Evolutionary Search'):
			selectedGenAlg = selectedGenAlgSwitcherEvolutionary(request)
		elif (selectedGenAlgId =='ODPIP Search'):
			selectedGenAlg = selectedGenAlgSwitcherODPIP(request)
		elif (selectedGenAlgId =='Coalition Link Search'):
			selectedGenAlg = selectedGenAlgSwitcherCLink(request)

		adaptation.init(playerBridge, taskBridge, configsGenAlg = selectedGenAlg, name='GIMME')

		if(newConfigParams['isBootstrapped']=='true'):
			adaptation.bootstrap(int(newConfigParams['numBootstrapIterations']))

		currConfigParams = newConfigParams
		return HttpResponse('ok')



	
	def taskRegistration(request):
		if(not 'professor' in request.user.userprofile.role):
			return HttpResponse('500')
		else:
			if request.method == 'POST':
				requestInfo = request.POST
				form = CreateTaskForm(requestInfo, request.FILES)
				if form.is_valid():
					
					task = form.save(commit = False)

					task.profile = json.dumps(InteractionsProfile(
						{
						 'Challenge': float(requestInfo['profileDim0']),
						 'Focus': float(requestInfo['profileDim1'])
						 }
					), default=lambda o: o.__dict__, sort_keys=True)

					task.save()

					# add task to free tasks
					currFreeTasks = serverStateModelBridge.getCurrFreeTasks()
					currFreeTasks.append(str(task.taskId))
					serverStateModelBridge.setCurrFreeTasks(currFreeTasks)

					serverStateModelBridge.setSimIsTaskCreated(True)

					return redirect('/dash')
				else:
					context = { 'form' : form }
					return render(request, 'taskRegistration.html', context)

			elif request.method == 'GET':				
				form = CreateTaskForm()
				context = { 'form' : form }
				return render(request, 'taskRegistration.html', context)
	
	def taskUpdate(request):
		if(not 'professor' in request.user.userprofile.role):
			return HttpResponse('500')
		else:
			if request.method == 'POST':
				taskIdToUpdate = request.GET.get('taskIdToUpdate')
				try:
					instance = Task.objects.get(taskId = taskIdToUpdate)
					
					post = request.POST
					_mutable = post._mutable
					post._mutable = True
					post['taskId'] = taskIdToUpdate
					post._mutable = _mutable

					form = UpdateTaskForm(request.POST, instance = instance)
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
					instance = Task.objects.get(taskId = taskIdToUpdate)

					form = UpdateTaskForm(instance = instance)
					context = { 'form' : form }
					return render(request, 'taskUpdate.html',  context)

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
		task = Task.objects.get(taskId = taskId)
		task.delete()

		currFreeTasks = serverStateModelBridge.getCurrFreeTasks()
		if(taskId in currFreeTasks):
			currFreeTasks.remove(taskId)
			serverStateModelBridge.setCurrFreeTasks(currFreeTasks)

		currSelectedTasks = serverStateModelBridge.getCurrSelectedTasks()
		if(taskId in currSelectedTasks):
			currSelectedTasks.remove(taskId)
			serverStateModelBridge.setCurrSelectedTasks(currSelectedTasks)

	def isTaskRegistered(taskId):
		returned = {}
		if(taskId != None):
			try:
				returned['task'] = Task.objects.get(taskId=taskId)
				returned['storedTasks'] = Task.objects.filter(taskId__contains=taskId)
			except ObjectDoesNotExist as e:
				print('task does not exist!')
				returned = { 'task': False, 'storedTasks': Task.objects.filter(taskId__contains=taskId) }
		return returned




	# auxiliary methods
	def fetchStudentStates(request):
		if request.method == 'POST':
			selectedUserIds = playerBridge.getAllStoredStudentUsernames()

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
			userInfo['fullName'] = playerBridge.getPlayerFullName(username)
			userInfo['email'] = playerBridge.getPlayerEmail(username)
			userInfo['characteristics'] = playerBridge.getPlayerCurrCharacteristics(username)
			userInfo['group'] = playerBridge.getPlayerCurrGroup(username)
			userInfo['groupProfile'] = playerBridge.getPlayerCurrProfile(username).dimensions
			userInfo['tasks'] = playerBridge.getPlayerCurrTasks(username)
			userInfo['statesDataFrame'] = playerBridge.getPlayerStatesDataFrame(username)
			userInfo['grade'] = playerBridge.getPlayerGrade(username)

			userInfo = json.dumps(userInfo, default=lambda o: o.__dict__, sort_keys=True)
			return HttpResponse(userInfo)
		return HttpResponse('error')
	



	def fetchServerState(request):
		if request.method == 'GET':
			newSessionState = {}
			newSessionState['timestamp'] = time.time()
			
			simState = serverStateModelBridge.getSimFlags()
			
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

			newSessionState['currSelectedUsers'] = serverStateModelBridge.getCurrSelectedUsers()
			newSessionState['currFreeUsers'] = serverStateModelBridge.getCurrFreeUsers()

			currSelectedTasks = []
			currFreeTasks = []

			taskObject = HttpRequest()
			taskObject.method = 'POST'
			

			currSelectedTasksIds = serverStateModelBridge.getCurrSelectedTasks()
			taskObject.POST = {'tasks': str(currSelectedTasksIds)[1:][:-1].replace(' ','').replace('\'','')}
			currSelectedTasks = Views.fetchTasksFromId(taskObject).content.decode('utf-8')


			taskObject = HttpRequest()
			taskObject.method = 'POST'

			currFreeTasksIds = serverStateModelBridge.getCurrFreeTasks()
			taskObject.POST = {'tasks': str(currFreeTasksIds)[1:][:-1].replace(' ','').replace('\'','')}
			currFreeTasks = Views.fetchTasksFromId(taskObject).content.decode('utf-8')

			newSessionState['currSelectedTasks'] = currSelectedTasks
			newSessionState['currFreeTasks'] = currFreeTasks

			newSessionState['readyForNewActivity'] = serverStateModelBridge.isReadyForNewActivity()

			if('professor' in request.user.userprofile.role):
				newSessionState['currAdaptationState'] = serverStateModelBridge.getCurrAdaptationState()

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
				if not taskId in taskBridge.getAllStoredTaskIds():
					return HttpResponse('error')

				task = taskBridge.getTask(taskId)
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

			allGroups = serverStateModelBridge.getCurrAdaptationState()['groups'];

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
			returnedState['currState'] = playerBridge.getPlayerCurrState(username)
			returnedState['grid'] = playerBridge.getPlayerStateGrid(username)
			return HttpResponse(json.dumps(returnedState, 
				default=lambda o: o.__dict__, sort_keys=True))
		return HttpResponse('error')

	def uploadTaskResults(request):
		if request.method == 'POST':
			username = request.POST['username']
			characteristicsDelta = json.loads(request.POST['characteristicsDelta'])

			characteristics = playerBridge.getPlayerCurrCharacteristics(username)
			characteristics.ability += characteristicsDelta['abilityInc']
			characteristics.engagement += characteristicsDelta['engagementInc']
			
			playerBridge.setPlayerCharacteristics(username, characteristics)
			
			grade = int(playerBridge.getPlayerGrade(username))
			grade += characteristicsDelta['gradeInc']
			playerBridge.setPlayerGrade(username, grade)
			
			return HttpResponse('ok')
		return HttpResponse('error')


	def manuallyChangeStudentGroup(request):
		if request.method == 'POST':
			adaptState = serverStateModelBridge.getCurrAdaptationState()
			
			giIndex = int(request.POST['student[groupId]'])
			gfIndex = int(request.POST['group[groupId]'])


			u = str(request.POST['student[userId]'])

			# change groups
			gi = adaptState['groups'][giIndex]
			gf = adaptState['groups'][gfIndex]
			
			#print("limits: "+str(adaptation.configsGenAlg.minNumberOfPlayersPerGroup)+"; "+str(adaptation.configsGenAlg.maxNumberOfPlayersPerGroup))
			#print(str(len(gi))+"; "+str(len(gf)))
			if(len(gi) == (adaptation.configsGenAlg.minNumberOfPlayersPerGroup - 1) or 
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
					currPlayerChars = playerBridge.getPlayerCurrCharacteristics(currPlayerI) 
					groupSize = len(g)
					currAvgCharacteristics.ability += currPlayerChars.ability / groupSize
					currAvgCharacteristics.engagement += currPlayerChars.engagement / groupSize

					adaptState['avgCharacteristics'][gIndex] = currAvgCharacteristics		

					serverStateModelBridge.setCurrAdaptationState(adaptState)

					# change student information
					playerBridge.setPlayerProfile(currPlayerI, adaptState['profiles'][gIndex])
					playerBridge.setPlayerGroup(currPlayerI, g)
					playerBridge.setPlayerTasks(currPlayerI, adaptState['tasks'][gIndex])


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
			serverStateModelBridge.setSimulationWeek(0)
			playersIds = playerBridge.getAllStoredStudentUsernames()
			for playerId in playersIds:
				Views.deleteUser(playerId)

			taskIds = taskBridge.getAllStoredTaskIds()
			for taskId in taskIds:
				Views.deleteTask(taskId)

			serverStateModelBridge.setSimIsLinkShared(False)
			serverStateModelBridge.setSimIsTaskCreated(False)
			serverStateModelBridge.setSimWeekOneUsersEvaluated(False)
			serverStateModelBridge.setSimSimulateReaction(False)
			return HttpResponse('ok')
		
		return HttpResponse('error')

	def advanceSimWeek(request):
		simulationWeek = serverStateModelBridge.getSimulationWeek()
		simStudentToEvaluate = ''
		simUnavailableStudent = ''
		simSimulateReaction = serverStateModelBridge.getSimSimulateReaction()
		simWeekOneUsersEvaluated = serverStateModelBridge.getSimWeekOneUsersEvaluated()
		if request.method == 'POST':
			if (simulationWeek > 5):
				simulationWeek = 6
			else:
				simulationWeek += 1 

			if (simulationWeek == 1):
				players = playerBridge.getAllStoredStudentUsernames()
				tasks = taskBridge.getAllStoredTaskIds()
				if (len(players) >= 20 and len(tasks) >= 20):
					simStudentToEvaluate = players[0]
				else:
					simulationWeek -= 1


			if (simulationWeek == 2):
				if (simWeekOneUsersEvaluated):
					simUnavailableStudent = playerBridge.getAllStoredStudentUsernames()[10]
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

			serverStateModelBridge.setSimulationWeek(simulationWeek)
			serverStateModelBridge.setSimUnavailableStudent(simUnavailableStudent)
			serverStateModelBridge.setSimStudentToEvaluate(simStudentToEvaluate)
			serverStateModelBridge.setSimSimulateReaction(simSimulateReaction)
			return HttpResponse('ok')
		
		return HttpResponse('error')


	def shareLinkSim(request):
		if request.method == 'POST':
			serverStateModelBridge.setSimIsLinkShared(True)
			for _ in range(int(request.POST['numUsersToGenerate'])):
				time.sleep(random.uniform(float(request.POST['minDelay']), float(request.POST['maxDelay'])))

				name = "".join(random.choice(names)+" "+random.choice(names))

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

				Views.userRegistration(httpRequest)

			Views.initServer(request)
			
			return HttpResponse('ok')

		return HttpResponse('error')


	def taskRegistrationSim(request):
		if request.method == 'POST':
			today = date.today()
			initWeek2 = today + timedelta(days=7)
			initWeek3 = initWeek2 + timedelta(days=7)
			initWeek4 = initWeek3 + timedelta(days=7)
			initWeek5 = initWeek4 + timedelta(days=7)

			strInitWeek1 = str(today)
			strInitWeek2 = str(initWeek2)
			strInitWeek3 = str(initWeek3)
			strInitWeek4 = str(initWeek4)
			strInitWeek5 = str(initWeek5)

			initDate = [today, today, today, initWeek2, initWeek2, initWeek2, initWeek2, initWeek3, initWeek3, initWeek3, initWeek3, initWeek4, initWeek4, initWeek4, initWeek4, initWeek5, initWeek5, initWeek5, initWeek5]

			strInitDate = [strInitWeek1, strInitWeek1, strInitWeek1, strInitWeek2, strInitWeek2, strInitWeek2, strInitWeek2, strInitWeek3, strInitWeek3, strInitWeek3, strInitWeek3, strInitWeek4, strInitWeek4, strInitWeek4, strInitWeek4, strInitWeek5, strInitWeek5, strInitWeek5, strInitWeek5]
			strFinalDate = []
			for j in initDate:
				strFinalDate.append(str(j + timedelta(days = 7)))

			for i in range(len(taskIds)):
				time.sleep(random.uniform(float(request.POST['minDelay']), float(request.POST['maxDelay'])))



				httpRequest = HttpRequest()
				httpRequest.method = 'POST'

				httpRequest.POST['taskId'] = taskIds[i]
				httpRequest.POST['description'] = description
				httpRequest.POST['minReqAbility'] = minReqAbility[i]
				httpRequest.POST['profileWeight'] = profileWeight
				httpRequest.POST['difficultyWeight'] = difficultyWeight
				httpRequest.POST['initDate'] = strInitDate[i]
				httpRequest.POST['finalDate'] = strFinalDate[i]
				httpRequest.POST['profileDim0'] = profileDim0[i]
				httpRequest.POST['profileDim1'] = profileDim1[i]

				httpRequest.user = request.user

				Views.taskRegistration(httpRequest)


			Views.initServer(request)
			return HttpResponse('ok')

		return HttpResponse('error')

	def evaluateSim(request):
		if request.method == 'POST':

			allUsers = playerBridge.getAllPlayerIds()
			allUsers.pop(0)
			for playerId in allUsers:
				prevState = playerBridge.getPlayerStatesDataFrame(playerId).states[-1]
				newState = Views.calcReaction(
					playerBridge = playerBridge, 
					state = prevState, 
					playerId = playerId)

				Views.savePlayerCharacteristics(playerId, newState.characteristics.ability, newState.characteristics.engagement)

			
			serverStateModelBridge.setSimWeekOneUsersEvaluated(True)
			return HttpResponse('ok')

		return HttpResponse('error')
