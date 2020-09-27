import json
import sys

import random
import string
import time
from datetime import datetime, date, time, timedelta

from django.shortcuts import render, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseServerError

from django.contrib.auth.models import User

from GIMMEWeb.core.models import UserProfile
from GIMMEWeb.core.models import Task
from GIMMEWeb.core.models import ServerState

from django.views.decorators.csrf import csrf_protect

from GIMMECore import *


from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages

from GIMMEWeb.core.forms import CreateUserForm, CreateUserProfileForm 


intProfTemplate = InteractionsProfile({"K_cp": 0, "K_ea": 0, "K_i": 0, "K_mh": 0})


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

	def getAllTaskIds(self):
		return serverStateModelBridge.getCurrSelectedTasks()
	
	def getAllStoredTaskIds(self):
		allTasks = Task.objects.all()
		allTasksIds = []
		for task in allTasks:
			allTasksIds.append(task.taskId)
		return allTasksIds


	def getTaskInteractionsProfile(self, taskId):
		task = Task.objects.get(taskId = taskId)
		return InteractionsProfile(dimensions = json.loads(task.profile)["dimensions"])

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
	
	def savePlayer(self, player):
		player.save()

	def getPlayer(self, username):
		return UserProfile.objects.get(username = username)

	def removePlayer(self, username):
		player = UserProfile.objects.get(username = username)
		player.delete()

	def setAndSavePlayerStateToGrid(self, username, newState):
		player = UserProfile.objects.get(username = username)

		self.setPlayerCharacteristics(username, newState.characteristics)
		self.setPlayerProfile(username, newState.profile)

		playerStateGrid = self.getPlayerStateGrid(username)
		playerStateGrid.pushToGrid(newState)
		player.pastModelIncreasesGrid = json.dumps(playerStateGrid, default=lambda o: o.__dict__)
		player.save()

	def resetPlayer(self, username):
		return 0


	def getAllPlayerIds(self): #allPlayers for adaptation
		return serverStateModelBridge.getCurrSelectedUsers()

	def getAllStoredUserIds(self):
		allUsers = UserProfile.objects.all()
		allUsersIds = []
		for player in allUsers:
			if player.role=="student":
				allUsersIds.append(player.username)
		return allUsersIds

	def getPlayerName(self, username):
		player = User.objects.get(username=username).userprofile
		return player.fullName

	
	def getPlayerCurrProfile(self,  username):
		player = User.objects.get(username=username).userprofile
		# print(json.dumps(player, default= lambda o: o.__dict__, sort_keys=True))
		profile = json.loads(player.currState)["profile"]
		profile = InteractionsProfile(dimensions= profile["dimensions"])
		return profile
	
	def getPlayerStateGrid(self, username):
		player = User.objects.get(username=username).userprofile

		playerStateGrid = json.loads(player.pastModelIncreasesGrid)
		cells = [[]]
		for cell in playerStateGrid["cells"]:
			newCell = []
			for state in cell:
				characteristics = state["characteristics"]
				characteristics = PlayerCharacteristics(ability= float(characteristics["ability"]), engagement= float(characteristics["engagement"]))

				profile = state["profile"]
				profile = InteractionsProfile(dimensions= profile["dimensions"])
				
				newCell.append(PlayerState(profile = profile, characteristics = characteristics, dist=state["dist"]))
			cells.append(newCell)

		gridTrimAlg = json.loads(json.dumps(playerStateGrid["gridTrimAlg"]))
		# print(gridTrimAlg)
		return	PlayerStateGrid(
			cells = cells,
			interactionsProfileTemplate = intProfTemplate.generateCopy().reset(), 
			gridTrimAlg = QualitySortGridTrimAlg(
			# gridTrimAlg = AgeSortGridTrimAlg(
				maxNumModelElements = int(gridTrimAlg["maxNumModelElements"]), 
				qualityWeights = PlayerCharacteristics(ability=0.5, engagement=0.5)
				), 
			numCells = int(playerStateGrid["numCells"])
			)

	def getPlayerCurrCharacteristics(self, username):
		player = User.objects.get(username=username).userprofile
		characteristics = json.loads(player.currState)["characteristics"]
		return PlayerCharacteristics(ability= float(characteristics["ability"]), engagement= float(characteristics["engagement"]))
	
	def getPlayerPersonalityEst(self, username):
		player = User.objects.get(username=username).userprofile
		personality = json.loads(player.personality)
		personality = InteractionsProfile(dimensions= personality["dimensions"])
		return personality

	def getPlayerCurrState(self, username):
		player = User.objects.get(username=username).userprofile
		return PlayerState(profile = self.getPlayerCurrProfile(username), characteristics = self.getPlayerCurrCharacteristics(username), dist = json.loads(player.currState)["dist"])

	def getPlayerFullName(self, username):
		player = User.objects.get(username=username).userprofile
		return player.fullName



	def setPlayerPersonalityEst(self, username, personality):
		player = User.objects.get(username=username).userprofile
		player.personality = json.dumps(personality, default=lambda o: o.__dict__)
		player.save()


	def setPlayerCharacteristics(self, username, characteristics):
		player = User.objects.get(username=username).userprofile
		newState = self.getPlayerCurrState(username)
		newState.characteristics = characteristics
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()

	def setPlayerProfile(self, username, profile):
		player = User.objects.get(username=username).userprofile
		newState = self.getPlayerCurrState(username)
		newState.profile = profile
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()

playerBridge = CustomPlayerModelBridge()


adaptation = Adaptation()
# profileTemplate = serverStateModelBridge.getProfileTemplate()
# for d in range(numInteractionDimensions):
# 	profileTemplate.dimensions["dim_"+str(d)] = 0.0


defaultConfigsAlg = StochasticHillclimberConfigsGen(
	playerModelBridge = playerBridge, 
	interactionsProfileTemplate = intProfTemplate.generateCopy(), 
	regAlg = KNNRegression(playerBridge, 5), 
	persEstAlg = ExplorationPersonalityEstAlg(
		playerModelBridge = playerBridge, 
		interactionsProfileTemplate = intProfTemplate.generateCopy(), 
		regAlg = KNNRegression(playerBridge, 5),
		numTestedPlayerProfiles = 100, 
		qualityWeights = PlayerCharacteristics(ability=0.5, engagement=0.5)), 
	numberOfConfigChoices = 300, 
	preferredNumberOfPlayersPerGroup = 5, 
	qualityWeights = PlayerCharacteristics(ability=0.5, engagement=0.5)
)
adaptation.init(playerBridge, taskBridge, configsGenAlg = defaultConfigsAlg, name="GIMME")


class Views(): #acts as a namespace

	def initServer(request):
		serverStateModelBridge.setCurrAdaptationState([])
		serverStateModelBridge.setReadyForNewActivity(False)
		serverStateModelBridge.setCurrSelectedUsers([])
		serverStateModelBridge.setCurrFreeUsers(playerBridge.getAllStoredUserIds())
		serverStateModelBridge.setCurrSelectedTasks([])
		serverStateModelBridge.setCurrFreeTasks(taskBridge.getAllStoredTaskIds())
		return HttpResponse('ok')

	#global methods
	def home(request):
		if request.method == "POST":
			return Views.loginCheck(request)
		else:
			return render(request, 'home.html')

	def loginCheck(request):
		if request.method == "POST":
			username = request.POST.get('username')
			password = request.POST.get('password')
			print('[INFO] login check performed on user with id - ' + str(username) + ', password - '+str(password))

			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/dash')
			else:
				messages.info(request, 'Login failed! Credentials not recognized.')
				return redirect('/home')


	def logoutCheck(request):
		logout(request)
		return redirect('/')

	def userRegistration(request):
		breakpoint()
		form = CreateUserForm(request.POST)
		profileForm = CreateUserProfileForm(request.POST, request.FILES)

		if form.is_valid() and profileForm.is_valid():
			user = form.save()
			
			profile = profileForm.save(commit = False)
			profile.user = user

			profile.currState = json.dumps(PlayerState(), default=lambda o: o.__dict__, sort_keys=True)
			profile.pastModelIncreasesGrid = json.dumps(
				PlayerStateGrid(
					interactionsProfileTemplate = intProfTemplate.generateCopy().reset(), 
					gridTrimAlg = QualitySortGridTrimAlg(
					# gridTrimAlg = AgeSortGridTrimAlg(
						maxNumModelElements = 30, #requestInfo["maxNumModelElements"]
						qualityWeights = PlayerCharacteristics(ability=0.5, engagement=0.5) #requestInfo["ability"]...
						), 
					numCells = 1 #requestInfo["numCells"]
				), 
			default=lambda o: o.__dict__, sort_keys=True)
			profile.personality = json.dumps(InteractionsProfile(), default=lambda o: o.__dict__, sort_keys=True)

			profile.save() 

			return Views.loginCheck(request)

		context = { 'form' : form , 'profileForm': profileForm }
		return render(request, 'userRegistration.html', context)

	def userUpdate(request):
		return render(request, 'userUpdate.html')

	def isUserRegistered(username):
		returned = {}
		if(username != None):
			try:
				returned["user"] = User.objects.get(username=username).userprofile
				returned["storedUsers"] = UserProfile.objects.filter(username__contains=username)
			except ObjectDoesNotExist as e:
				print("user does not exist!")
				returned = {"user": False, "storedUsers": User.objects.filter(username__contains=username)}
		return returned

	def dash(request):
		dashSwitch = {
			'student': 'student/dash.html',
			'professor': 'professor/dash.html',
			'designer': 'designer/dash.html',
			'': 'home.html'
		}
		if(not request.user):
			return render(request,'home.html')
		else:
			# breakpoint()
			print(dashSwitch.get(request.user.userprofile.role))
			return render(request, 'professor/dash.html')
			return render(request, dashSwitch.get(request.user.userprofile.role))

	
	def getRandomString(length):
		letters = string.ascii_lowercase
		numbers = "0123456789"
		chars = letters + numbers
		result_str = random.choice(numbers) + ''.join(random.choice(chars) for i in range(length))
		return result_str
	

	@csrf_protect
	def updateUserRegistration(request):
		if request.POST:
			requestInfo = request.POST
			

			entry = playerBridge.getPlayer(requestInfo["username"])


			entry.user.username = requestInfo["username"]
			entry.email = requestInfo["email"]
			entry.password = requestInfo["password"]
			entry.role = requestInfo["role"]
			entry.age = requestInfo["age"]
			entry.gender = requestInfo["gender"]
			entry.preferences = requestInfo["preferences"]
			entry.fullName = requestInfo["fullName"]

			entry.avatar = ""

			try:
				playerBridge.savePlayer(entry)
			except IntegrityError as e:
				request.session["playerRegistrationError"] = e.__class__.__name__
				return HttpResponseServerError()


			if(request.session.get("username") == entry.username):
				Views.loginCheck(request)
			return HttpResponse('ok')


	@csrf_protect
	def removeUserRegistration(request):
		username = request.POST["username"]

		currFreeUsers = serverStateModelBridge.getCurrFreeUsers()
		if username in currFreeUsers:
			currFreeUsers.remove(username)
			serverStateModelBridge.setCurrFreeUsers(currFreeUsers)

		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers()
		if username in currSelectedUsers:
			currSelectedUsers.remove(username)
			serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)

		playerBridge.removePlayer(username)
		return HttpResponse('ok')



	@csrf_protect
	def addAllUsersSelected(request): #reads (player) from args
		serverStateModelBridge.setCurrSelectedUsers(playerBridge.getAllStoredUserIds())
		serverStateModelBridge.setCurrFreeUsers([])
		return HttpResponse('ok')
	@csrf_protect
	def removeAllUsersSelected(request): #reads (player) from args
		serverStateModelBridge.setCurrSelectedUsers([])
		serverStateModelBridge.setCurrFreeUsers(playerBridge.getAllStoredUserIds())
		return HttpResponse('ok')

	@csrf_protect
	def addSelectedUser(request): #reads (player) from args
		usernameToAdd = request.POST.get('username')
		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
		currFreeUsers = serverStateModelBridge.getCurrFreeUsers();
		if not usernameToAdd in currSelectedUsers:
			currSelectedUsers.append(usernameToAdd)
			currFreeUsers.remove(usernameToAdd)
		serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
		serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
		return HttpResponse('ok')

	@csrf_protect
	def removeSelectedUser(request): #reads (player) from args
		usernameToRemove = request.POST.get('username')
		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
		currFreeUsers = serverStateModelBridge.getCurrFreeUsers();
		if usernameToRemove in currSelectedUsers:
			currSelectedUsers.remove(usernameToRemove)
			currFreeUsers.append(usernameToRemove)
		serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
		serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
		return HttpResponse('ok')



	@csrf_protect
	def addAllTasksSelected(request): #reads (player) from args
		serverStateModelBridge.setCurrSelectedTasks(taskBridge.getAllStoredTaskIds())
		serverStateModelBridge.setCurrFreeTasks([])
		return HttpResponse('ok')

	@csrf_protect
	def removeAllTasksSelected(request): #reads (player) from args
		serverStateModelBridge.setCurrSelectedTasks([])
		serverStateModelBridge.setCurrFreeTasks(taskBridge.getAllStoredTaskIds())
		return HttpResponse('ok')

	@csrf_protect
	def addSelectedTask(request): #reads (player) from args
		usernameToAdd = request.POST.get('taskId')
		currSelectedTasks = serverStateModelBridge.getCurrSelectedTasks();
		currFreeTasks = serverStateModelBridge.getCurrFreeTasks();
		if not usernameToAdd in currSelectedTasks:
			currSelectedTasks.append(usernameToAdd)
			currFreeTasks.remove(usernameToAdd)
		serverStateModelBridge.setCurrSelectedTasks(currSelectedTasks)
		serverStateModelBridge.setCurrFreeTasks(currFreeTasks)
		return HttpResponse('ok')

	@csrf_protect
	def removeSelectedTask(request): #reads (player) from args
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
	@csrf_protect
	def startActivity(request):
		# remove from selected and move to occupied list
		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
		currFreeUsers = serverStateModelBridge.getCurrFreeUsers();

		currSelectedUsers.remove(request.session.get("username"))
		currFreeUsers.append(request.session.get("username"))
		serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
		serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
		return render(request, 'student/activity.html')

	@csrf_protect
	def saveTaskResults(request):

		# remove from occupied list
		currFreeUsers = serverStateModelBridge.getCurrFreeUsers()
		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
		
		currFreeUsers.remove(request.session.get("username"))
		serverStateModelBridge.setcurrFreeUsers(currFreeUsers)
		
		if len(currSelectedUsers) == 0 and len(currSelectedUsers) == 0:
			serverStateModelBridge.setReadyForNewActivity(False)

		if request.POST:
			username = request.session.get("username")
			characteristics = playerBridge.getPlayerCurrCharacteristics(username)
			characteristics = PlayerCharacteristics(ability=float(request.POST["ability"]) - characteristics.ability, engagement=float(request.POST["engagement"]) - characteristics.engagement)
			playerBridge.setPlayerCharacteristics(username, characteristics)
			playerBridge.setAndSavePlayerStateToGrid(username, PlayerState(characteristics=characteristics, profile=playerBridge.getPlayerCurrProfile(username)))
			return Views.dash(request)


	# professor methods
	@csrf_protect
	def startAdaptation(request):
		
		try:
			currAdaptationState = adaptation.iterate()
		except ValueError:
			print("ValueError error!")
			return HttpResponse('error')
			
		serverStateModelBridge.setCurrAdaptationState(currAdaptationState)
		serverStateModelBridge.setReadyForNewActivity(True)
		return Views.fetchServerState(request)


	@csrf_protect
	def configAdaptation(request):
		# breakpoint()

		# print(json.dumps(request.POST, default=lambda o: o.__dict__, sort_keys=True))
		selectedRegAlg = {}		
		def selectedRegAlgSwitcherKNN(request):
			return KNNRegression( 
				playerBridge, 
				int(request.POST["numNNs"])
			)

		selectedRegAlgSwitcher = { 
		    "KNN": selectedRegAlgSwitcherKNN(request)
		} 
		selectedRegAlg = selectedRegAlgSwitcher.get(request.POST["selectedRegAlgId"], None)


		selectedGenAlg = {}
		def selectedGenAlgSwitcherStochasticHillclimber(request):
			return StochasticHillclimberConfigsGen(
							playerModelBridge = playerBridge, 
							interactionsProfileTemplate = intProfTemplate.generateCopy(), 
							regAlg = selectedRegAlg, 
							persEstAlg = ExplorationPersonalityEstAlg(
								playerModelBridge = playerBridge, 
								interactionsProfileTemplate = intProfTemplate.generateCopy(), 
								regAlg = selectedRegAlg,
								numTestedPlayerProfiles = 100, 
								qualityWeights = PlayerCharacteristics(ability=float(request.POST["qualityWeightsAb"]), engagement=float(request.POST["qualityWeightsEng"]))),
							numberOfConfigChoices = int(request.POST["numberOfConfigChoices"]), 
					minNumberOfPlayersPerGroup = int(request.POST["minNumberOfPlayersPerGroup"]), 
					maxNumberOfPlayersPerGroup = int(request.POST["maxNumberOfPlayersPerGroup"]), 
					preferredNumberOfPlayersPerGroup = int(request.POST["preferredNumberOfPlayersPerGroup"]),
							qualityWeights = PlayerCharacteristics(ability=float(request.POST["qualityWeightsAb"]), engagement=float(request.POST["qualityWeightsEng"]))
					)

		def selectedGenAlgSwitcherSimulatedAnnealing(request):
			return SimulatedAnnealingConfigsGen(
							playerModelBridge = playerBridge, 
							interactionsProfileTemplate = intProfTemplate.generateCopy(), 
							regAlg = selectedRegAlg, 
							persEstAlg = ExplorationPersonalityEstAlg(
								playerModelBridge = playerBridge, 
								interactionsProfileTemplate = intProfTemplate.generateCopy(), 
								regAlg = selectedRegAlg,
								numTestedPlayerProfiles = 100, 
								qualityWeights = PlayerCharacteristics(ability=float(request.POST["qualityWeightsAb"]), engagement=float(request.POST["qualityWeightsEng"]))),
							numberOfConfigChoices = int(request.POST["numberOfConfigChoices"]), 
							minNumberOfPlayersPerGroup = int(request.POST["minNumberOfPlayersPerGroup"]), 
							maxNumberOfPlayersPerGroup = int(request.POST["maxNumberOfPlayersPerGroup"]), 
							preferredNumberOfPlayersPerGroup = int(request.POST["preferredNumberOfPlayersPerGroup"]),
							qualityWeights = PlayerCharacteristics(ability=float(request.POST["qualityWeightsAb"]), engagement=float(request.POST["qualityWeightsEng"])),
							temperatureDecay = float(request.POST["temperatureDecay"])
					)


		def selectedGenAlgSwitcherRandom(request):
			return RandomConfigsGen(
				playerModelBridge = playerBridge, 
				interactionsProfileTemplate = intProfTemplate.generateCopy(),
				minNumberOfPlayersPerGroup = int(request.POST["minNumberOfPlayersPerGroup"]), 
				maxNumberOfPlayersPerGroup = int(request.POST["maxNumberOfPlayersPerGroup"]), 
				preferredNumberOfPlayersPerGroup = int(request.POST["preferredNumberOfPlayersPerGroup"]))

		selectedGenAlgSwitcher = { 
		    "Random": selectedGenAlgSwitcherRandom(request), 
		    "StochasticHillclimber": selectedGenAlgSwitcherStochasticHillclimber(request),
		    "SimulatedAnnealing": selectedGenAlgSwitcherSimulatedAnnealing(request)
		} 
		# breakpoint()
		selectedGenAlg = selectedGenAlgSwitcher.get(request.POST["selectedGenAlgId"], defaultConfigsAlg)

		adaptation.init(playerBridge, taskBridge, configsGenAlg = selectedGenAlg, name="GIMME")
		return HttpResponse('ok')




	def taskRegistration(request):
		if(request.session.get('role') != "professor"):
			return HttpResponse('500')
		return render(request, 'taskRegistration.html')
	
	def taskUpdate(request):
		if(request.session.get('role') != "professor"):
			return HttpResponse('500')
		return render(request, 'taskUpdate.html')


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


	@csrf_protect	
	def saveTaskRegistration(request):
		if request.POST:
			requestInfo = request.POST
			isNewRegRequest = json.loads(request.session.get('isNewTaskRegRequest'))

			entry = Task() 

			taskId = ''
			
			entry.creator = request.session.get('username')
			# requestInfo._mutable = True
			# requestInfo['taskId'] = taskId
			# requestInfo._mutable = False

			entry.creationTime = datetime.now()
			entry.title = requestInfo['title']

			if(isNewRegRequest):
				lenOfIsReg = 1
				while(lenOfIsReg > 0):
					taskId = requestInfo['title'].replace(' ', '')
					taskId = taskId + Views.getRandomString(10) #if username exists in other regs, register username1, username2, etc.

					isReg = Views.isTaskRegistered(taskId)
					lenOfIsReg = len(isReg['storedTasks'])
			else:
				taskId = requestInfo['taskId']

			entry.taskId = taskId
			entry.description = requestInfo['description']
			entry.minReqAbility = requestInfo['minReqAbility']
			entry.profile = json.dumps(InteractionsProfile(
				{
				 "K_cp": float(requestInfo['profileDim0']),
				 "K_ea": float(requestInfo['profileDim1']),
				 "K_i":  float(requestInfo['profileDim2']),
				 "K_mh": float(requestInfo['profileDim3'])
				 }
			), default=lambda o: o.__dict__, sort_keys=True)
			entry.profileWeight = requestInfo['profileWeight']
			entry.difficultyWeight = requestInfo['difficultyWeight']

			entry.filePaths = ''

			# Adaptation stuff
			if(isNewRegRequest):
				try:
					taskBridge.saveTask(entry)

					# add task to free tasks
					currFreeTasks = serverStateModelBridge.getCurrFreeTasks();
					currFreeTasks.append(taskId)
					serverStateModelBridge.setCurrFreeTasks(currFreeTasks)

				except IntegrityError as e:
					request.session['playerRegistrationError'] = e.__class__.__name__
					return HttpResponse('500')
			else:
				try:
					UserProfile.objects.filter(username=username).update(**entry.__dict__)
				except IntegrityError as e:
					request.session['playerRegistrationError'] = e.__class__.__name__
					return HttpResponse('500')


			return HttpResponse('200')


	@csrf_protect
	def removeTaskRegistration(request):
		taskId = request.POST["taskId"]

		currFreeTasks = serverStateModelBridge.getCurrFreeTasks()
		if(taskId in currFreeTasks):
			currFreeTasks.remove(taskId)
			serverStateModelBridge.setCurrFreeTasks(currFreeTasks)

		currSelectedTasks = serverStateModelBridge.getCurrSelectedTasks()
		if(taskId in currSelectedTasks):
			currSelectedTasks.remove(taskId)
			serverStateModelBridge.setCurrSelectedTasks(currSelectedTasks)

		taskBridge.removeTask(taskId)
		return HttpResponse('200')


	# auxiliary methods
	@csrf_protect
	def fetchSelectedUserStates(request):
		selectedUserIds = serverStateModelBridge.getCurrSelectedUsers()

		userStates = {}
		for username in selectedUserIds:
			userState = {}
			# userState["myStateGrid"] = playerBridge.getPlayerStateGrid(username)
			userState["fullName"] = playerBridge.getPlayerFullName(username)
			userState["characteristics"] = playerBridge.getPlayerCurrCharacteristics(username)
			userState["personalityEst"] = playerBridge.getPlayerPersonalityEst(username)

			userStates[username] = userState


		userStates = json.dumps(userStates, default=lambda o: o.__dict__, sort_keys=True)
		return HttpResponse(userStates)

	@csrf_protect
	def fetchServerState(request):
		newSessionState = {}
		
		newSessionState['currSelectedUsers'] = serverStateModelBridge.getCurrSelectedUsers()
		newSessionState['currFreeUsers'] = serverStateModelBridge.getCurrFreeUsers()

		newSessionState['currSelectedTasks'] = serverStateModelBridge.getCurrSelectedTasks()
		newSessionState['currFreeTasks'] = serverStateModelBridge.getCurrFreeTasks()

		newSessionState['readyForNewActivity'] = serverStateModelBridge.isReadyForNewActivity()

		if(request.user.userprofile.role == 'professor'):
			newSessionState['currAdaptationState'] = serverStateModelBridge.getCurrAdaptationState()

		newSession = json.dumps(newSessionState, default=lambda o: o.__dict__, sort_keys=True)

		# print(newSessionState)
		return HttpResponse(newSession)