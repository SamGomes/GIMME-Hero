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
		currAdaptationState = json.loads(serverState.currAdaptationState)
		return currAdaptationState
	def isReadyForNewActivity(self):
		serverState = ServerState.objects.first()
		readyForNewActivity = json.loads(serverState.readyForNewActivity)
		return readyForNewActivity
	
	def getCurrSelectedUsers(self):
		serverState = ServerState.objects.first()
		currSelectedUsers = json.loads(serverState.currSelectedUsers)
		return currSelectedUsers
	def getCurrFreeUsers(self):
		serverState = ServerState.objects.first()
		currFreeUsers = json.loads(serverState.currFreeUsers)
		return currFreeUsers
		
	def getCurrSelectedTasks(self):
		serverState = ServerState.objects.first()
		currSelectedTasks = json.loads(serverState.currSelectedTasks)
		return currSelectedTasks
	def getCurrFreeTasks(self):
		serverState = ServerState.objects.first()
		currFreeTasks = json.loads(serverState.currFreeTasks)
		return currFreeTasks

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


class Views(): #acts as a namespace

	def initServer(request):
		serverStateModelBridge.setCurrAdaptationState([])
		serverStateModelBridge.setReadyForNewActivity(True)
		serverStateModelBridge.setCurrSelectedUsers([])
		serverStateModelBridge.setCurrFreeUsers(playerBridge.getAllStoredStudentUsernames())
		serverStateModelBridge.setCurrSelectedTasks([])
		serverStateModelBridge.setCurrFreeTasks(taskBridge.getAllStoredTaskIds())

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
		print(allUsers)
		for playerId in allUsers:
			prevState = playerBridge.getPlayerStatesDataFrame(playerId).states[-1]
			newState = Views.calcReaction(
				playerBridge = playerBridge, 
				state = prevState, 
				playerId = playerId)

			Views.savePlayerCharacteristics(playerId, newState.characteristics.ability, newState.characteristics.engagement)

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
				player = User.objects.get(username = username)
				player.delete()

			except User.DoesNotExist:
				messages.info(request, 'Account not deleted! Username not found.')
				return redirect('/userUpdate')

			currFreeUsers = serverStateModelBridge.getCurrFreeUsers()
			if username in currFreeUsers:
				currFreeUsers.remove(username)
				serverStateModelBridge.setCurrFreeUsers(currFreeUsers)

			currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers()
			if username in currSelectedUsers:
				currSelectedUsers.remove(username)
				serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
			return redirect('/home')


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
			serverStateModelBridge.setCurrSelectedUsers(playerBridge.getAllStoredStudentUsernames())
			serverStateModelBridge.setCurrFreeUsers([])
			return HttpResponse('ok')
	
	def removeAllUsersSelected(request): #reads (player) from args
		if request.method == 'POST':
			serverStateModelBridge.setCurrSelectedUsers([])
			serverStateModelBridge.setCurrFreeUsers(playerBridge.getAllStoredStudentUsernames())
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
			serverStateModelBridge.setCurrSelectedTasks(taskBridge.getAllStoredTaskIds())
			serverStateModelBridge.setCurrFreeTasks([])
			return HttpResponse('ok')

	
	def removeAllTasksSelected(request): #reads (player) from args
		if request.method == 'POST':
			serverStateModelBridge.setCurrSelectedTasks([])
			serverStateModelBridge.setCurrFreeTasks(taskBridge.getAllStoredTaskIds())
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
		characteristics = PlayerCharacteristics(ability=float(ability) - characteristics.ability, engagement=float(engagement))
		playerBridge.setPlayerCharacteristics(username, characteristics)

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
			
		serverStateModelBridge.setCurrAdaptationState(currAdaptationState)
		serverStateModelBridge.setReadyForNewActivity(True)
		return Views.fetchServerState(request)


	def configAdaptation(request):
		
		global currConfigParams

		newConfigParams = request.POST
		print(currConfigParams == newConfigParams)
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
		if (selectedRegAlgId =='KNN'):
			selectedRegAlg = selectedRegAlgSwitcherKNN(request)
			persEstRegAlg = selectedRegAlg
		elif (selectedRegAlgId == 'Synergy Between Students'):
			selectedRegAlg = selectedRegAlgSwitcherSynergy(request)
			persEstRegAlg = selectedRegAlgSwitcherKNN(request)


		selectedGenAlg = {}
		def selectedGenAlgSwitcherRandom(request):
			# print('RRRRRRRRRRRRRRRRR')
			return RandomConfigsGen(
				playerModelBridge = playerBridge, 
				interactionsProfileTemplate = intProfTemplate.generateCopy(),
				# minNumberOfPlayersPerGroup = int(newConfigParams['minNumberOfPlayersPerGroup']), 
				# maxNumberOfPlayersPerGroup = int(newConfigParams['maxNumberOfPlayersPerGroup']), 
				preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']))

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
						# minNumberOfPlayersPerGroup = int(newConfigParams['minNumberOfPlayersPerGroup']), 
						# maxNumberOfPlayersPerGroup = int(newConfigParams['maxNumberOfPlayersPerGroup']), 
						preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup'])
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
						# minNumberOfPlayersPerGroup = int(newConfigParams['minNumberOfPlayersPerGroup']), 
						# maxNumberOfPlayersPerGroup = int(newConfigParams['maxNumberOfPlayersPerGroup']), 
						preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),
						temperatureDecay = float(newConfigParams['temperatureDecay'])
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

				preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']), 
				
				initialPopulationSize = int(newConfigParams['initialPopulationSize']), 
				numberOfEvolutionsPerIteration = int(newConfigParams['numberOfEvolutionsPerIteration']), 
				
				probOfCross = float(newConfigParams['probOfCross']), 
				probOfMutation = float(newConfigParams['probOfMutation']),

				probOfMutationConfig = float(newConfigParams['probOfMutationConfig']), 
				probOfMutationGIPs = float(newConfigParams['probOfMutationGIPs']), 
				
				numChildrenPerIteration = int(newConfigParams['numChildrenPerIteration']),
				numSurvivors = int(newConfigParams['numSurvivors']),

				cxOp = "order")

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

				preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),

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

				preferredNumberOfPlayersPerGroup = int(newConfigParams['preferredNumberOfPlayersPerGroup']),

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
						 'Challenge': 1.0 - float(requestInfo['profileDim0']),
						 'Focus': float(requestInfo['profileDim1'])
						 }
					), default=lambda o: o.__dict__, sort_keys=True)

					task.save()

					# add task to free tasks
					currFreeTasks = serverStateModelBridge.getCurrFreeTasks()
					currFreeTasks.append(str(task.taskId))
					serverStateModelBridge.setCurrFreeTasks(currFreeTasks)

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
				task = Task.objects.get(taskId = taskId)
				task.delete()

			except Task.DoesNotExist:
				messages.info(request, 'Task not deleted! Id not found.')
				return redirect('/dash')

			currFreeTasks = serverStateModelBridge.getCurrFreeTasks()
			if(taskId in currFreeTasks):
				currFreeTasks.remove(taskId)
				serverStateModelBridge.setCurrFreeTasks(currFreeTasks)

			currSelectedTasks = serverStateModelBridge.getCurrSelectedTasks()
			if(taskId in currSelectedTasks):
				currSelectedTasks.remove(taskId)
				serverStateModelBridge.setCurrSelectedTasks(currSelectedTasks)

			return redirect('/dash')



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
		print("method: "+request.method)
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
			
			g1i = int(request.POST['student1[groupId]'])
			g2i = int(request.POST['student2[groupId]'])

			u1n = str(request.POST['student1[userId]'])
			u2n = str(request.POST['student2[userId]'])

			# change groups
			adaptState['groups'][g1i].remove(u1n)
			adaptState['groups'][g2i].remove(u2n)

			adaptState['groups'][g1i].append(u2n)
			adaptState['groups'][g2i].append(u1n)

			for gi in [g1i, g2i]:
				g = adaptState['groups'][gi]

				# recalculate averages
				currAvgCharacteristics = PlayerCharacteristics()
				currAvgCharacteristics.reset()
				for currPlayerI in g:
					currPlayerChars = playerBridge.getPlayerCurrCharacteristics(currPlayerI) 
					groupSize = len(g)
					currAvgCharacteristics.ability += currPlayerChars.ability / groupSize
					currAvgCharacteristics.engagement += currPlayerChars.engagement / groupSize

					adaptState['avgCharacteristics'][gi] = currAvgCharacteristics		

					serverStateModelBridge.setCurrAdaptationState(adaptState)

					# change student information
					playerBridge.setPlayerProfile(currPlayerI, adaptState['profiles'][gi])
					playerBridge.setPlayerGroup(currPlayerI, g)
					playerBridge.setPlayerTasks(currPlayerI, adaptState['tasks'][gi])


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
