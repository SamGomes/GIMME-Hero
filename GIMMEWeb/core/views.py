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

sys.path.insert(1,'/home/samgomes/Documents/doutoramento/reps/GIMME/GIMME')
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
	
	def getCurrWaitingPlayers(self):
		serverState = ServerState.objects.first()
		currWaitingPlayers = json.loads(serverState.currWaitingPlayers)
		return currWaitingPlayers
	def getCurrFreePlayers(self):
		serverState = ServerState.objects.first()
		currFreePlayers = json.loads(serverState.currFreePlayers)
		return currFreePlayers

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

	def setCurrWaitingPlayers(self, currWaitingPlayers):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currWaitingPlayers = json.dumps(currWaitingPlayers, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currWaitingPlayers = currWaitingPlayers
		serverState.save()
	def setCurrFreePlayers(self, currFreePlayers):
		serverState = ServerState.objects.first()
		if serverState == None:
			serverState = ServerState()
		else:
			currFreePlayers = json.dumps(currFreePlayers, default=lambda o: o.__dict__, sort_keys=True)
			serverState.currFreePlayers = currFreePlayers
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
		player = User.objects.get(username = playerId)

		self.setPlayerCharacteristics(playerId, newState.characteristics)
		self.setPlayerProfile(playerId, newState.profile)

		playerStateGrid = self.getPlayerStateGrid(playerId)
		playerStateGrid.pushToGrid(newState)
		player.pastModelIncreasesGrid = json.dumps(playerStateGrid, default=lambda o: o.__dict__)
		player.save()

	def resetPlayer(self, playerId):
		return 0


	def getAllPlayerIds(self): #allPlayers for adaptation
		return serverStateModelBridge.getCurrWaitingPlayers()

	def getAllStoredPlayerIds(self):
		allPlayers = User.objects.all()
		allPlayersIds = []
		for player in allPlayers:
			if player.role=="student":
				allPlayersIds.append(player.username)
		return allPlayersIds

	def getPlayerName(self, playerId):
		player = User.objects.get(username=playerId)
		return player.fullName

	
	def getPlayerCurrProfile(self,  playerId):
		player = User.objects.get(username=playerId)
		# print(json.dumps(player, default= lambda o: o.__dict__, sort_keys=True))
		profile = json.loads(player.currState)["profile"]
		profile = InteractionsProfile(dimensions= profile["dimensions"])
		return profile
	
	def getPlayerStateGrid(self, playerId):
		player = User.objects.get(username=playerId)

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
		player = User.objects.get(username=playerId)
		characteristics = json.loads(player.currState)["characteristics"]
		return PlayerCharacteristics(ability= float(characteristics["ability"]), engagement= float(characteristics["engagement"]))
	
	def getPlayerPersonalityEst(self, playerId):
		player = User.objects.get(username=playerId)
		personality = json.loads(player.personality)
		personality = InteractionsProfile(dimensions= personality["dimensions"])
		return personality

	def getPlayerCurrState(self,  playerId):
		player = User.objects.get(username=playerId)
		return PlayerState(profile = self.getPlayerCurrProfile(playerId), characteristics = self.getPlayerCurrCharacteristics(playerId), dist = json.loads(player.currState)["dist"])


	def setPlayerPersonalityEst(self, playerId, personality):
		player = User.objects.get(username=playerId)
		player.personality = json.dumps(personality, default=lambda o: o.__dict__)
		player.save()


	def setPlayerCharacteristics(self, playerId, characteristics):
		player = User.objects.get(username=playerId)
		newState = self.getPlayerCurrState(playerId)
		newState.characteristics = characteristics
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()

	def setPlayerProfile(self, playerId, profile):
		player = User.objects.get(username=playerId)
		newState = self.getPlayerCurrState(playerId)
		newState.profile = profile
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()

playerBridge = CustomPlayerModelBridge()



# init server state
# serverStateModelBridge.setCurrAdaptationState([])
# serverStateModelBridge.setReadyForNewActivity(False)
# serverStateModelBridge.setCurrWaitingPlayers([])
# serverStateModelBridge.setCurrFreePlayers(["s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13","s14","s15","s16","s17","s18","s19","s20","s21","s22","s23","s24","s25","s26","s27","s28","s29","s30","s31","s32","s33","s34","s35","s36","s37","s38","s39","s40","s41","s42","s43","s44","s45","s46","s47","s48","s49","s50"])

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


	#global methods
	def home(request):
		return render(request, 'home.html')

	@csrf_protect
	def loginCheck(request):
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')

		print(username)
		print(email)
		print(password)

		if(not Views.isRegistered(username)["user"]):
			return HttpResponseNotFound("username not found")

		storedUser = User.objects.get(username = username)

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
		print("here")
		return render(request, 'userRegistration.html')

	def isRegistered(username):
		returned = {}
		if(username != None):
			try:
				returned["user"] = User.objects.get(username=username)
				returned["storedUsers"] = User.objects.filter(username__contains=username)
			except ObjectDoesNotExist as e:
				print("user does not exist!")
				returned = {"user": False, "storedUsers": User.objects.filter(username__contains=username)}
		return returned

	def isLoggedIn(request):
		if(request.session.get('username')!=None):
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
       
		
	def updateRegMode(request):
		request.session["isNewRegRequest"] = request.POST["isNewRegRequest"]
		return HttpResponse('ok')
	
	def getRandomString(length):
		letters = string.ascii_lowercase
		numbers = "0123456789"
		chars = letters + numbers
		result_str = random.choice(numbers) + ''.join(random.choice(chars) for i in range(length))
		return result_str

	def saveUserRegistration(request):
		if request.POST:
			requestInfo = request.POST

			isNewRegRequest = json.loads(request.session.get("isNewRegRequest"))

			entry = User() 


			username = ""
			if(isNewRegRequest):
				lenOfIsReg = 1
				while(lenOfIsReg > 0):
					username = requestInfo["fullName"].replace(" ", "")
					username = username + Views.getRandomString(10) #if username exists in other regs, register username1, username2, etc.

					isReg = Views.isRegistered(username)
					lenOfIsReg = len(isReg["storedUsers"])
			else:
				username = requestInfo["username"]

			entry.username = username
			# entry.isAuthenticated = requestInfo["isAuthenticated"]
			entry.email = requestInfo["email"]
			entry.password = requestInfo["password"]
			entry.role = requestInfo["role"]
			entry.age = requestInfo["age"]
			entry.gender = requestInfo["gender"]
			entry.preferences = requestInfo["preferences"]
			entry.fullName = requestInfo["fullName"]


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
					request.session["playerRegistrationError", e]
					return HttpResponse('500')

			else:
				breakpoint()
				try:
					User.objects.filter(username=username).update(**entry.__dict__)
				except IntegrityError as e:
					request.session["playerRegistrationError", e]
					return HttpResponse('500')



			currFreePlayers = serverStateModelBridge.getCurrFreePlayers();
			currFreePlayers.append(username)
			serverStateModelBridge.setCurrFreePlayers(currFreePlayers)

			return HttpResponse('200')

	@csrf_protect
	def addAllPlayersWaiting(request): #reads (player) from args
		serverStateModelBridge.setCurrWaitingPlayers(playerBridge.getAllStoredPlayerIds())
		serverStateModelBridge.setCurrFreePlayers([])
		return HttpResponse('ok')
	@csrf_protect
	def removeAllPlayersWaiting(request): #reads (player) from args
		serverStateModelBridge.setCurrWaitingPlayers([])
		serverStateModelBridge.setCurrFreePlayers(playerBridge.getAllStoredPlayerIds())
		return HttpResponse('ok')

	@csrf_protect
	def addWaitingPlayer(request): #reads (player) from args
		playerIdToAdd = request.POST.get("playerId")
		currWaitingPlayers = serverStateModelBridge.getCurrWaitingPlayers();
		currFreePlayers = serverStateModelBridge.getCurrFreePlayers();
		if not playerIdToAdd in currWaitingPlayers:
			currWaitingPlayers.append(playerIdToAdd)
			currFreePlayers.remove(playerIdToAdd)
		serverStateModelBridge.setCurrWaitingPlayers(currWaitingPlayers)
		serverStateModelBridge.setCurrFreePlayers(currFreePlayers)
		return HttpResponse('ok')

	@csrf_protect
	def removeWaitingPlayer(request): #reads (player) from args
		playerIdToRemove = request.POST.get("playerId")
		currWaitingPlayers = serverStateModelBridge.getCurrWaitingPlayers();
		currFreePlayers = serverStateModelBridge.getCurrFreePlayers();
		if playerIdToRemove in currWaitingPlayers:
			currWaitingPlayers.remove(playerIdToRemove)
			currFreePlayers.append(playerIdToRemove)
		serverStateModelBridge.setCurrWaitingPlayers(currWaitingPlayers)
		serverStateModelBridge.setCurrFreePlayers(currFreePlayers)
		return HttpResponse('ok')



	# student methods
	@csrf_protect
	def startActivity(request):
		# remove from waiting and move to occupied list
		currWaitingPlayers = serverStateModelBridge.getCurrWaitingPlayers();
		currFreePlayers = serverStateModelBridge.getCurrFreePlayers();

		currWaitingPlayers.remove(request.session.get("username"))
		currFreePlayers.append(request.session.get("username"))
		serverStateModelBridge.setCurrWaitingPlayers(currWaitingPlayers)
		serverStateModelBridge.setCurrFreePlayers(currFreePlayers)
		return render(request, 'student/activity.html')

	@csrf_protect
	def saveTaskResults(request):

		# remove from occupied list
		currFreePlayers = serverStateModelBridge.getCurrFreePlayers()
		currWaitingPlayers = serverStateModelBridge.getCurrWaitingPlayers();
		
		currFreePlayers.remove(request.session.get("username"))
		serverStateModelBridge.setCurrFreePlayers(currFreePlayers)
		
		if len(currWaitingPlayers) == 0 and len(currWaitingPlayers) == 0:
			serverStateModelBridge.setReadyForNewActivity(False)

		if request.POST:
			playerId = request.session.get("username")
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
		return Views.dash(request)

	def saveTaskRegistration(request):
		if request.POST:
			return Views.dash(request)


	# auxiliary methods
	@csrf_protect
	def fetchPlayerState(request):
		username = request.session.get("username")

		newSessionState = {}
		newSessionState["myStateGrid"] = playerBridge.getPlayerStateGrid(username)
		newSessionState["myCharacteristics"] = playerBridge.getPlayerCurrCharacteristics(username)
		newSessionState["myPersonality"] = playerBridge.getPlayerPersonalityEst(username)

		newSession = json.dumps(newSessionState, default=lambda o: o.__dict__, sort_keys=True)
		return HttpResponse(newSession)

	@csrf_protect
	def fetchServerState(request):
		newSessionState = {}
		
		newSessionState["currWaitingPlayers"] = serverStateModelBridge.getCurrWaitingPlayers()
		newSessionState["currFreePlayers"] = serverStateModelBridge.getCurrFreePlayers()

		newSessionState["readyForNewActivity"] = serverStateModelBridge.isReadyForNewActivity()

		if(request.session['role'] == 'professor'):
			newSessionState["currAdaptationState"] = serverStateModelBridge.getCurrAdaptationState()

		newSession = json.dumps(newSessionState, default=lambda o: o.__dict__, sort_keys=True)
		return HttpResponse(newSession)