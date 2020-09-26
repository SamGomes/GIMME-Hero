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
from django.http import HttpResponse, HttpResponseNotFound

from django.contrib.auth.models import User

from GIMMEWeb.core.models import UserProfile
from GIMMEWeb.core.models import Task
from GIMMEWeb.core.models import ServerState

from django.views.decorators.csrf import csrf_protect

from GIMMECore import *


from django.contrib.auth import authenticate
from django.contrib.auth import logout


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

	def getPlayer(self, userId):
		return UserProfile.objects.get(userId = userId)

	def removePlayer(self, userId):
		player = UserProfile.objects.get(userId = userId)
		player.delete()

	def setAndSavePlayerStateToGrid(self, userId, newState):
		player = UserProfile.objects.get(userId = userId)

		self.setPlayerCharacteristics(userId, newState.characteristics)
		self.setPlayerProfile(userId, newState.profile)

		playerStateGrid = self.getPlayerStateGrid(userId)
		playerStateGrid.pushToGrid(newState)
		player.pastModelIncreasesGrid = json.dumps(playerStateGrid, default=lambda o: o.__dict__)
		player.save()

	def resetPlayer(self, userId):
		return 0


	def getAllPlayerIds(self): #allPlayers for adaptation
		return serverStateModelBridge.getCurrSelectedUsers()

	def getAllStoredUserIds(self):
		allUsers = UserProfile.objects.all()
		allUsersIds = []
		for player in allUsers:
			if player.role=="student":
				allUsersIds.append(player.userId)
		return allUsersIds

	def getPlayerName(self, userId):
		player = User.objects.get(username=userId).userprofile
		return player.fullName

	
	def getPlayerCurrProfile(self,  userId):
		player = User.objects.get(username=userId).userprofile
		# print(json.dumps(player, default= lambda o: o.__dict__, sort_keys=True))
		profile = json.loads(player.currState)["profile"]
		profile = InteractionsProfile(dimensions= profile["dimensions"])
		return profile
	
	def getPlayerStateGrid(self, userId):
		player = User.objects.get(username=userId).userprofile

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

	def getPlayerCurrCharacteristics(self, userId):
		player = User.objects.get(username=userId).userprofile
		characteristics = json.loads(player.currState)["characteristics"]
		return PlayerCharacteristics(ability= float(characteristics["ability"]), engagement= float(characteristics["engagement"]))
	
	def getPlayerPersonalityEst(self, userId):
		player = User.objects.get(username=userId).userprofile
		personality = json.loads(player.personality)
		personality = InteractionsProfile(dimensions= personality["dimensions"])
		return personality

	def getPlayerCurrState(self, userId):
		player = User.objects.get(username=userId).userprofile
		return PlayerState(profile = self.getPlayerCurrProfile(userId), characteristics = self.getPlayerCurrCharacteristics(userId), dist = json.loads(player.currState)["dist"])

	def getPlayerFullName(self, userId):
		player = User.objects.get(username=userId).userprofile
		return player.fullName



	def setPlayerPersonalityEst(self, userId, personality):
		player = User.objects.get(username=userId).userprofile
		player.personality = json.dumps(personality, default=lambda o: o.__dict__)
		player.save()


	def setPlayerCharacteristics(self, userId, characteristics):
		player = User.objects.get(username=userId).userprofile
		newState = self.getPlayerCurrState(userId)
		newState.characteristics = characteristics
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()

	def setPlayerProfile(self, userId, profile):
		player = User.objects.get(username=userId).userprofile
		newState = self.getPlayerCurrState(userId)
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
		return render(request, 'home.html')

	def loginCheck(request):
		userId = request.POST.get('userId')
		password = request.POST.get('password')
		print('[INFO] login check performed on user with id - ' + str(userId) + ', password - '+str(password))

		user = authenticate(request, username=userId, password=password)
		if user is not None:
			request.user = user
			return Views.dash(request)
		else:
			return HttpResponseNotFound("userId not found")


	def logoutCheck(request):
		logout(request)

	def userRegistration(request):
		return render(request, 'userRegistration.html')
	def userUpdate(request):
		return render(request, 'userUpdate.html')

	def isUserRegistered(userId):
		returned = {}
		if(userId != None):
			try:
				returned["user"] = User.objects.get(username=userId).userprofile
				returned["storedUsers"] = UserProfile.objects.filter(userId__contains=userId)
			except ObjectDoesNotExist as e:
				print("user does not exist!")
				returned = {"user": False, "storedUsers": User.objects.filter(username__contains=userId)}
		return returned

	def dash(request):
		dashSwitch = {
			'student': 'student/dash.html',
			'professor': 'professor/dash.html',
			'designer': 'designer/dash.html',
			None: 'home.html'
		}
		if(not hasattr(request.user,'userprofile')):
			return render(request,'home.html')
		else:
			return render(request, dashSwitch.get(request.user.userprofile.role))

	
	def getRandomString(length):
		letters = string.ascii_lowercase
		numbers = "0123456789"
		chars = letters + numbers
		result_str = random.choice(numbers) + ''.join(random.choice(chars) for i in range(length))
		return result_str
		
	@csrf_protect
	def saveUserRegistration(request):
		if request.POST:
			requestInfo = request.POST
			
			entry = User()

			userId = ""

			lenOfIsReg = 1
			while(lenOfIsReg > 0):
				userId = requestInfo["fullName"].replace(" ", "")
				userId = userId + Views.getRandomString(10) #if userId exists in other regs, register userId1, userId2, etc.

				isReg = Views.isUserRegistered(userId)
				lenOfIsReg = len(isReg["storedUsers"])


			entry.username = userId
			# requestInfo._mutable = True
			# requestInfo["userId"] = userId
			# requestInfo._mutable = False


			entry.email = requestInfo["email"]
			entry.set_password(requestInfo["password"])
			entry.role = requestInfo["role"]
			entry.age = requestInfo["age"]
			entry.gender = requestInfo["gender"]
			entry.description = requestInfo["description"]
			entry.fullName = requestInfo["fullName"]

			entry.avatar = ""

			entry.currState = json.dumps(PlayerState(), default=lambda o: o.__dict__, sort_keys=True)
			entry.pastModelIncreasesGrid = json.dumps(
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
			entry.personality = json.dumps(InteractionsProfile(), default=lambda o: o.__dict__, sort_keys=True)
			
			try:
				playerBridge.savePlayer(entry)
				# add user to free users
				if entry.userprofile.role=="student":
					currFreeUsers = serverStateModelBridge.getCurrFreeUsers()
					currFreeUsers.append(userId)
					serverStateModelBridge.setCurrFreeUsers(currFreeUsers)

			except IntegrityError as e:
				request.session["playerRegistrationError"] = e.__class__.__name__
				return HttpResponse('500')

			if(request.session.get("userId") == None):
				Views.loginCheck(request)
			return HttpResponse('200')

	@csrf_protect
	def updateUserRegistration(request):
		if request.POST:
			requestInfo = request.POST
			

			entry = playerBridge.getPlayer(requestInfo["userId"])


			entry.user.username = requestInfo["userId"]
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
				return HttpResponse('500')


			if(request.session.get("userId") == entry.userId):
				Views.loginCheck(request)
			return HttpResponse('200')


	@csrf_protect
	def removeUserRegistration(request):
		userId = request.POST["userId"]

		currFreeUsers = serverStateModelBridge.getCurrFreeUsers()
		if userId in currFreeUsers:
			currFreeUsers.remove(userId)
			serverStateModelBridge.setCurrFreeUsers(currFreeUsers)

		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers()
		if userId in currSelectedUsers:
			currSelectedUsers.remove(userId)
			serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)

		playerBridge.removePlayer(userId)
		return HttpResponse('200')



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
		userIdToAdd = request.POST.get('userId')
		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
		currFreeUsers = serverStateModelBridge.getCurrFreeUsers();
		if not userIdToAdd in currSelectedUsers:
			currSelectedUsers.append(userIdToAdd)
			currFreeUsers.remove(userIdToAdd)
		serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
		serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
		return HttpResponse('ok')

	@csrf_protect
	def removeSelectedUser(request): #reads (player) from args
		userIdToRemove = request.POST.get('userId')
		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
		currFreeUsers = serverStateModelBridge.getCurrFreeUsers();
		if userIdToRemove in currSelectedUsers:
			currSelectedUsers.remove(userIdToRemove)
			currFreeUsers.append(userIdToRemove)
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
		userIdToAdd = request.POST.get('taskId')
		currSelectedTasks = serverStateModelBridge.getCurrSelectedTasks();
		currFreeTasks = serverStateModelBridge.getCurrFreeTasks();
		if not userIdToAdd in currSelectedTasks:
			currSelectedTasks.append(userIdToAdd)
			currFreeTasks.remove(userIdToAdd)
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

		currSelectedUsers.remove(request.session.get("userId"))
		currFreeUsers.append(request.session.get("userId"))
		serverStateModelBridge.setCurrSelectedUsers(currSelectedUsers)
		serverStateModelBridge.setCurrFreeUsers(currFreeUsers)
		return render(request, 'student/activity.html')

	@csrf_protect
	def saveTaskResults(request):

		# remove from occupied list
		currFreeUsers = serverStateModelBridge.getCurrFreeUsers()
		currSelectedUsers = serverStateModelBridge.getCurrSelectedUsers();
		
		currFreeUsers.remove(request.session.get("userId"))
		serverStateModelBridge.setcurrFreeUsers(currFreeUsers)
		
		if len(currSelectedUsers) == 0 and len(currSelectedUsers) == 0:
			serverStateModelBridge.setReadyForNewActivity(False)

		if request.POST:
			userId = request.session.get("userId")
			characteristics = playerBridge.getPlayerCurrCharacteristics(userId)
			characteristics = PlayerCharacteristics(ability=float(request.POST["ability"]) - characteristics.ability, engagement=float(request.POST["engagement"]) - characteristics.engagement)
			playerBridge.setPlayerCharacteristics(userId, characteristics)
			playerBridge.setAndSavePlayerStateToGrid(userId, PlayerState(characteristics=characteristics, profile=playerBridge.getPlayerCurrProfile(userId)))
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
			
			entry.creator = request.session.get('userId')
			# requestInfo._mutable = True
			# requestInfo['taskId'] = taskId
			# requestInfo._mutable = False

			entry.creationTime = datetime.now()
			entry.title = requestInfo['title']

			if(isNewRegRequest):
				lenOfIsReg = 1
				while(lenOfIsReg > 0):
					taskId = requestInfo['title'].replace(' ', '')
					taskId = taskId + Views.getRandomString(10) #if userId exists in other regs, register userId1, userId2, etc.

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
					UserProfile.objects.filter(userId=userId).update(**entry.__dict__)
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
		for userId in selectedUserIds:
			userState = {}
			# userState["myStateGrid"] = playerBridge.getPlayerStateGrid(userId)
			userState["fullName"] = playerBridge.getPlayerFullName(userId)
			userState["characteristics"] = playerBridge.getPlayerCurrCharacteristics(userId)
			userState["personalityEst"] = playerBridge.getPlayerPersonalityEst(userId)

			userStates[userId] = userState


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

		if(request.session['role'] == 'professor'):
			newSessionState['currAdaptationState'] = serverStateModelBridge.getCurrAdaptationState()

		newSession = json.dumps(newSessionState, default=lambda o: o.__dict__, sort_keys=True)

		# print(newSessionState)
		return HttpResponse(newSession)