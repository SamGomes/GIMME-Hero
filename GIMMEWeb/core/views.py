import json
import sys

import random
import string

from django.shortcuts import render, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound

from GIMMEWeb.core.models import User
from GIMMEWeb.core.models import Task
from GIMMEWeb.core.models import ServerState

from django.views.decorators.csrf import csrf_protect

from GIMMECore import *


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
		currSelectedPlayers = json.loads(serverState.currSelectedPlayers)
		return currSelectedPlayers
	def getCurrFreeUsers(self):
		serverState = ServerState.objects.first()
		currFreePlayers = json.loads(serverState.currFreePlayers)
		
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


	def setCurrSelectedPlayers(self, currSelectedPlayers):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currSelectedPlayers = json.dumps(currSelectedPlayers, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currSelectedPlayers = currSelectedPlayers
		serverState.save()
	def setCurrFreePlayers(self, currFreePlayers):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currFreePlayers = json.dumps(currFreePlayers, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currFreePlayers = currFreePlayers
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
	
	def getAllTaskIds(self):
		return []

	def getTaskInteractionsProfile(self, taskId):
		return InteractionsProfile()

	def getMinTaskRequiredAbility(self, taskId):
		return 0

	def getMinTaskDuration(self, taskId):
		pass

	def getTaskDifficultyWeight(self, taskId):
		return 0

	def getTaskProfileWeight(self, taskId):
		return 0

taskBridge = CustomTaskModelBridge()



class CustomPlayerModelBridge(PlayerModelBridge):
	
	def setAndSavePlayerStateToGrid(self, playerId, newState):
		player = User.objects.get(userId = playerId)

		self.setPlayerCharacteristics(playerId, newState.characteristics)
		self.setPlayerProfile(playerId, newState.profile)

		playerStateGrid = self.getPlayerStateGrid(playerId)
		playerStateGrid.pushToGrid(newState)
		player.pastModelIncreasesGrid = json.dumps(playerStateGrid, default=lambda o: o.__dict__)
		player.save()

	def resetPlayer(self, playerId):
		return 0


	def getAllPlayerIds(self): #allPlayers for adaptation
		return serverStateModelBridge.getCurrSelectedUsers()

	def getAllStoredUserIds(self):
		allUsers = User.objects.all()
		allUsersIds = []
		for player in allPlayers:
			if player.role=="student":
				allUsersIds.append(player.userId)
		return allUsersIds

	def getPlayerName(self, playerId):
		player = User.objects.get(userId=playerId)
		return player.fullName

	
	def getPlayerCurrProfile(self,  playerId):
		player = User.objects.get(userId=playerId)
		# print(json.dumps(player, default= lambda o: o.__dict__, sort_keys=True))
		profile = json.loads(player.currState)["profile"]
		profile = InteractionsProfile(dimensions= profile["dimensions"])
		return profile
	
	def getPlayerStateGrid(self, playerId):
		player = User.objects.get(userId=playerId)

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

	def getPlayerCurrCharacteristics(self, playerId):
		player = User.objects.get(userId=playerId)
		characteristics = json.loads(player.currState)["characteristics"]
		return PlayerCharacteristics(ability= float(characteristics["ability"]), engagement= float(characteristics["engagement"]))
	
	def getPlayerPersonalityEst(self, playerId):
		player = User.objects.get(userId=playerId)
		personality = json.loads(player.personality)
		personality = InteractionsProfile(dimensions= personality["dimensions"])
		return personality

	def getPlayerCurrState(self,  playerId):
		player = User.objects.get(userId=playerId)
		return PlayerState(profile = self.getPlayerCurrProfile(playerId), characteristics = self.getPlayerCurrCharacteristics(playerId), dist = json.loads(player.currState)["dist"])


	def setPlayerPersonalityEst(self, playerId, personality):
		player = User.objects.get(userId=playerId)
		player.personality = json.dumps(personality, default=lambda o: o.__dict__)
		player.save()


	def setPlayerCharacteristics(self, playerId, characteristics):
		player = User.objects.get(userId=playerId)
		newState = self.getPlayerCurrState(playerId)
		newState.characteristics = characteristics
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()

	def setPlayerProfile(self, playerId, profile):
		player = User.objects.get(userId=playerId)
		newState = self.getPlayerCurrState(playerId)
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
		serverStateModelBridge.setCurrFreeTasks([])
		return HttpResponse('ok')

	#global methods
	def home(request):
		return render(request, 'home.html')

	def loginCheck(request):
		userId = request.POST.get('userId')
		email = request.POST.get('email')
		password = request.POST.get('password')

		print('[INFO] login check performed on user with id - ' + str(userId) + ', password - '+str(password))

		if(not Views.isUserRegistered(userId)["user"]):
			return HttpResponseNotFound("userId not found")

		storedUser = User.objects.get(userId = userId)

		# check if pass is right
		if storedUser.password != password:
			return HttpResponseNotFound("pass not found")
		
		request.session.flush()
		userDict = storedUser.__dict__.copy()
		userDict.pop('_state')
		request.session.update(userDict)

		request.session.save()

		return redirect("/dash")

	def logout(request):
	    try:
	        request.session.flush()
	    except KeyError:
	        pass
	        return HttpResponse("You're already logged out.")
	    return redirect("/home")

	def userRegistration(request):
		return render(request, 'userRegistration.html')

	def isUserRegistered(userId):
		returned = {}
		if(userId != None):
			try:
				returned["user"] = User.objects.get(userId=userId)
				returned["storedUsers"] = User.objects.filter(userId__contains=userId)
			except ObjectDoesNotExist as e:
				print("user does not exist!")
				returned = {"user": False, "storedUsers": User.objects.filter(userId__contains=userId)}
		return returned

	def isLoggedIn(request):
		if(request.session.get('userId') != None):
			return HttpResponse('200')
		else:
			return HttpResponse('500')

	def dash(request):
		dashSwitch = {
	        'student': 'student/dash.html',
	        'professor': 'professor/dash.html',
	        'designer': 'designer/dash.html',
	        None: 'home.html'
	    }
		return render(request, dashSwitch.get(request.session.get("role")), request.session.__dict__)
       
	
	@csrf_protect	
	def updateUserRegMode(request):
		request.session["isNewUserRegRequest"] = request.POST["isNewUserRegRequest"]
		return HttpResponse('ok')
	
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
			isNewRegRequest = json.loads(request.session.get("isNewUserRegRequest"))

			entry = User() 

			userId = ""
			if(isNewRegRequest):
				lenOfIsReg = 1
				while(lenOfIsReg > 0):
					userId = requestInfo["fullName"].replace(" ", "")
					userId = userId + Views.getRandomString(10) #if userId exists in other regs, register userId1, userId2, etc.

					isReg = Views.isUserRegistered(userId)
					lenOfIsReg = len(isReg["storedUsers"])
			else:
				userId = requestInfo["userId"]

			entry.userId = userId
			requestInfo._mutable = True
			requestInfo["userId"] = userId
			requestInfo._mutable = False

			# entry.isAuthenticated = requestInfo["isAuthenticated"]
			entry.email = requestInfo["email"]
			entry.password = requestInfo["password"]
			entry.role = requestInfo["role"]
			entry.age = requestInfo["age"]
			entry.gender = requestInfo["gender"]
			entry.preferences = requestInfo["preferences"]
			entry.fullName = requestInfo["fullName"]

			entry.avatar = ""

			# Adaptation stuff
			if(isNewRegRequest):
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
					entry.save()
				except IntegrityError as e:
					request.session["playerRegistrationError"] = e.__class__.__name__
					return HttpResponse('500')

			else:
				try:
					User.objects.filter(userId=userId).update(**entry.__dict__)
				except IntegrityError as e:
					request.session["playerRegistrationError"] = e.__class__.__name__
					return HttpResponse('500')


			if entry.role=="student":
				currFreePlayers = serverStateModelBridge.getCurrFreeUsers();
				currFreePlayers.append(userId)
				serverStateModelBridge.setCurrFreePlayers(currFreePlayers)

			Views.loginCheck(request)
			return HttpResponse('200')

	@csrf_protect
	def addAllPlayersSelected(request): #reads (player) from args
		serverStateModelBridge.setCurrSelectedPlayers(playerBridge.getAllStoredUserIds())
		serverStateModelBridge.setCurrFreePlayers([])
		return HttpResponse('ok')
	@csrf_protect
	def removeAllPlayersSelected(request): #reads (player) from args
		serverStateModelBridge.setCurrSelectedPlayers([])
		serverStateModelBridge.setCurrFreePlayers(playerBridge.getAllStoredUserIds())
		return HttpResponse('ok')

	@csrf_protect
	def addSelectedPlayer(request): #reads (player) from args
		playerIdToAdd = request.POST.get("userId")
		currSelectedPlayers = serverStateModelBridge.getCurrSelectedUsers();
		currFreePlayers = serverStateModelBridge.getCurrFreeUsers();
		if not playerIdToAdd in currSelectedPlayers:
			currSelectedPlayers.append(playerIdToAdd)
			currFreePlayers.remove(playerIdToAdd)
		serverStateModelBridge.setCurrSelectedPlayers(currSelectedPlayers)
		serverStateModelBridge.setCurrFreePlayers(currFreePlayers)
		return HttpResponse('ok')

	@csrf_protect
	def removeSelectedPlayer(request): #reads (player) from args
		playerIdToRemove = request.POST.get("userId")
		currSelectedPlayers = serverStateModelBridge.getCurrSelectedUsers();
		currFreePlayers = serverStateModelBridge.getCurrFreeUsers();
		if playerIdToRemove in currSelectedPlayers:
			currSelectedPlayers.remove(playerIdToRemove)
			currFreePlayers.append(playerIdToRemove)
		serverStateModelBridge.setCurrSelectedPlayers(currSelectedPlayers)
		serverStateModelBridge.setCurrFreePlayers(currFreePlayers)
		return HttpResponse('ok')



	# student methods
	@csrf_protect
	def startActivity(request):
		# remove from selected and move to occupied list
		currSelectedPlayers = serverStateModelBridge.getCurrSelectedUsers();
		currFreePlayers = serverStateModelBridge.getCurrFreeUsers();

		currSelectedPlayers.remove(request.session.get("userId"))
		currFreePlayers.append(request.session.get("userId"))
		serverStateModelBridge.setCurrSelectedPlayers(currSelectedPlayers)
		serverStateModelBridge.setCurrFreePlayers(currFreePlayers)
		return render(request, 'student/activity.html')

	@csrf_protect
	def saveTaskResults(request):

		# remove from occupied list
		currFreePlayers = serverStateModelBridge.getCurrFreeUsers()
		currSelectedPlayers = serverStateModelBridge.getCurrSelectedUsers();
		
		currFreePlayers.remove(request.session.get("userId"))
		serverStateModelBridge.setCurrFreePlayers(currFreePlayers)
		
		if len(currSelectedPlayers) == 0 and len(currSelectedPlayers) == 0:
			serverStateModelBridge.setReadyForNewActivity(False)

		if request.POST:
			playerId = request.session.get("userId")
			characteristics = playerBridge.getPlayerCurrCharacteristics(playerId)
			characteristics = PlayerCharacteristics(ability=float(request.POST["ability"]) - characteristics.ability, engagement=float(request.POST["engagement"]) - characteristics.engagement)
			playerBridge.setPlayerCharacteristics(playerId, characteristics)
			playerBridge.setAndSavePlayerStateToGrid(playerId, PlayerState(characteristics=characteristics, profile=playerBridge.getPlayerCurrProfile(playerId)))
			return Views.dash(request)


	# professor methods
	@csrf_protect
	def startAdaptation(request):
		# return Views.fetchServerState(request)
		# try:
		currAdaptationState = adaptation.iterate()
		# except ValueError:
		# 	return HttpResponseNotFound('something went wrong!')
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
		return render(request, 'taskRegistration.html')


	def isTaskRegistered(userId):
		returned = {}
		if(userId != None):
			try:
				returned['task'] = User.objects.get(taskId=taskId)
				returned['storedTasks'] = User.objects.filter(taskId__contains=taskId)
			except ObjectDoesNotExist as e:
				print("task does not exist!")
				returned = {"task": False, "storedTasks": User.objects.filter(taskId__contains=taskId)}
		return returned


	@csrf_protect	
	def updateTaskRegMode(request):
		request.session["isNewTaskRegRequest"] = request.POST["isNewTaskRegRequest"]
		return HttpResponse('ok')

	def saveTaskRegistration(request):
		if request.POST:
			requestInfo = request.POST
			isNewRegRequest = json.loads(request.session.get("isNewTaskRegRequest"))

			entry = User() 

			taskId = ''
			
			entry.creator = userId
			# requestInfo._mutable = True
			# requestInfo['taskId'] = taskId
			# requestInfo._mutable = False

			entry.creationTime = datetime.now()
			entry.title = requestInfo['title']

			if(isNewRegRequest):
				lenOfIsReg = 1
				while(lenOfIsReg > 0):
					taskId = requestInfo['title'].replace(" ", "")
					taskId = taskId + Views.getRandomString(10) #if userId exists in other regs, register userId1, userId2, etc.

					isReg = Views.isTaskRegistered(taskId)
					lenOfIsReg = len(isReg["storedTasks"])
			else:
				taskId = requestInfo['taskId']

			entry.description = requestInfo['description']
			entry.minReqAbility = requestInfo['minReqAbility']
			entry.profile = requestInfo['profile']
			entry.profileImportance = requestInfo['profileImportance']
			entry.difficultyImportance = requestInfo['difficultyImportance']

			entry.filePaths = ''

			# Adaptation stuff
			if(isNewRegRequest):
				try:
					entry.save()
				except IntegrityError as e:
					request.session['playerRegistrationError'] = e.__class__.__name__
					return HttpResponse('500')
			else:
				try:
					User.objects.filter(userId=userId).update(**entry.__dict__)
				except IntegrityError as e:
					request.session['playerRegistrationError'] = e.__class__.__name__
					return HttpResponse('500')

			return HttpResponse('200')



	# auxiliary methods
	@csrf_protect
	def fetchPlayerState(request):
		userId = request.session.get("userId")

		newSessionState = {}
		newSessionState["myStateGrid"] = playerBridge.getPlayerStateGrid(userId)
		newSessionState["myCharacteristics"] = playerBridge.getPlayerCurrCharacteristics(userId)
		newSessionState["myPersonality"] = playerBridge.getPlayerPersonalityEst(userId)

		newSession = json.dumps(newSessionState, default=lambda o: o.__dict__, sort_keys=True)
		return HttpResponse(newSession)

	@csrf_protect
	def fetchServerState(request):
		newSessionState = {}
		
		newSessionState["currSelectedPlayers"] = serverStateModelBridge.getCurrSelectedUsers()
		newSessionState["currFreePlayers"] = serverStateModelBridge.getCurrFreeUsers()

		newSessionState["currSelectedTasks"] = serverStateModelBridge.getCurrSelectedTasks()
		newSessionState["currFreeTasks"] = serverStateModelBridge.getCurrFreeTasks()

		newSessionState["readyForNewActivity"] = serverStateModelBridge.isReadyForNewActivity()

		if(request.session['role'] == 'professor'):
			newSessionState["currAdaptationState"] = serverStateModelBridge.getCurrAdaptationState()

		newSession = json.dumps(newSessionState, default=lambda o: o.__dict__, sort_keys=True)

		print(newSessionState)
		return HttpResponse(newSession)