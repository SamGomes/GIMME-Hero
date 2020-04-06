import json
import sys

from django.shortcuts import render, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from GIMMEWeb.core.models import User
from GIMMEWeb.core.models import Task
from GIMMEWeb.core.models import ServerState

from django.views.decorators.csrf import csrf_protect

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
		print(allPlayersIds)
		return allPlayersIds

	def getPlayerName(self, playerId):
		player = User.objects.get(username=playerId)
		return player.fullName

	
	def getPlayerCurrProfile(self,  playerId):
		player = User.objects.get(username=playerId)
		profile = json.loads(player.currState)["profile"]
		return InteractionsProfile(K_ea=float(profile["K_ea"]), K_mh=float(profile["K_mh"]), K_cp=float(profile["K_cp"]), K_i=float(profile["K_i"]))
	
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
				profile = InteractionsProfile(K_ea=float(profile["K_ea"]), K_mh=float(profile["K_mh"]), K_cp=float(profile["K_cp"]), K_i=float(profile["K_i"]))
	
				
				newCell.append(PlayerState(profile = profile, characteristics = characteristics, dist=state["dist"]))
			cells.append(newCell)
		return PlayerStateGrid(cells=cells, numCells=int(playerStateGrid["numCells"]), maxProfilesPerCell=int(playerStateGrid["maxProfilesPerCell"]))

	def getPlayerCurrCharacteristics(self, playerId):
		player = User.objects.get(username=playerId)
		characteristics = json.loads(player.currState)["characteristics"]
		return PlayerCharacteristics(ability= float(characteristics["ability"]), engagement= float(characteristics["engagement"]))
	
	def getPlayerPersonality(self, playerId):
		player = User.objects.get(username=playerId)
		personality = json.loads(player.personality)
		return InteractionsProfile(K_ea=float(personality["K_ea"]), K_mh=float(personality["K_mh"]), K_cp=float(personality["K_cp"]), K_i=float(personality["K_i"]))
	
	def getPlayerCurrState(self,  playerId):
		player = User.objects.get(username=playerId)
		return PlayerState(profile = self.getPlayerCurrProfile(playerId), characteristics = self.getPlayerCurrCharacteristics(playerId), dist = json.loads(player.currState)["dist"])


	def setPlayerPersonality(self, playerId, personality):
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
# serverStateModelBridge.setCurrFreePlayers([])

adaptation = Adaptation()
simpleConfigsAlg = SimpleConfigsGen(playerBridge, regAlg = KNNRegression(playerBridge, 5), numberOfConfigChoices=100, preferredNumberOfPlayersPerGroup = 5, qualityWeights = PlayerCharacteristics(ability=0.5, engagement=0.5))
adaptation.init(playerBridge, taskBridge, configsGenAlg = simpleConfigsAlg, name="GIMME")


class Views(): #acts as a namespace

	#global methods
	def home(request):
		if(Views.isLoggedIn(request)):
			return Views.dash(request)
		return render(request, 'home.html')

	def login(request):
		if(Views.isLoggedIn(request)):
			return Views.dash(request)
		return render(request, 'login.html')

	def loginCheck(request):
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')

		if(not Views.isRegistered(username, email)):
			return redirect('/home')

		storedUser = User.objects.get(username = username)

		# check if pass is right
		if storedUser.password != password:
			return redirect('/home')
		
		request.session.flush()
		userDict = storedUser.__dict__.copy()
		userDict.pop('_state')
		request.session.update(userDict)

		request.session.save()

		return redirect('/dash')

	def logout(request):
	    try:
	        request.session.flush()
	    except KeyError:
	        pass
	        return HttpResponse("You're already logged out.")
	    return render(request, 'home.html')

	def registerUser(request):
		return render(request, 'userRegistration.html')

	def isRegistered(username, email):
		if(username != None):
			try:
				storedUser = User.objects.get(username = username)
			except ObjectDoesNotExist as e:
				print("user does not exist!")
				return False
		elif(email != None):
			try:
				storedUser = User.objects.get(email = email)
			except ObjectDoesNotExist as e:
				print("user  does not exist!")
				return False
		else:
			return False
		return True

	def isLoggedIn(request):
		return (request.session.get('username')!=None)

	def dash(request):
		dashSwitch = {
	        'student': 'student/dash.html',
	        'professor': 'professor/dash.html',
	        'designer': 'designer/dash.html',
	        None: 'home.html'
	    }
		return render(request, dashSwitch.get(request.session.get("role")), request.session.__dict__)
       
		

	def saveUserRegistration(request):
		if request.POST:
			username = request.POST.get('username')
			email = request.POST.get('email')
			password = request.POST.get('password')
			if(Views.isRegistered(username, email)):
				return redirect('/home')
			
			entry = User() 

			requestInfo = request.POST

			entry.username = requestInfo["username"]
			# entry.isAuthenticated = requestInfo["isAuthenticated"]
			entry.email = requestInfo["email"]
			entry.password = requestInfo["password"]
			entry.role = requestInfo["role"]
			entry.age = requestInfo["age"]
			entry.gender = requestInfo["gender"]
			entry.preferences = requestInfo["preferences"]
			entry.fullName = requestInfo["fullName"]

			# Adaptation stuff
			entry.currState = json.dumps(PlayerState(), default=lambda o: o.__dict__, sort_keys=True)
			entry.pastModelIncreasesGrid = json.dumps(PlayerStateGrid(), default=lambda o: o.__dict__, sort_keys=True)
			entry.personality = json.dumps(InteractionsProfile(), default=lambda o: o.__dict__, sort_keys=True)
			entry.save()

			currFreePlayers = serverStateModelBridge.getCurrFreePlayers();
			currFreePlayers.append(username)
			serverStateModelBridge.setCurrFreePlayers(currFreePlayers)

			return Views.dash(request)

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
			characteristics = PlayerCharacteristics(ability=request.POST["ability"], engagement=request.POST["engagement"])
			playerBridge.setPlayerCharacteristics(playerId, characteristics)
			playerBridge.setAndSavePlayerStateToGrid(playerId, PlayerState(characteristics=characteristics, profile=playerBridge.getPlayerCurrProfile()))
			return Views.dash(request)


	# professor methods
	def startAdaptation(request):
		currAdaptationState = adaptation.iterate()
		print(currAdaptationState)
		serverStateModelBridge.setCurrAdaptationState(currAdaptationState)
		serverStateModelBridge.setReadyForNewActivity(True)
		return Views.fetchServerState(request)


	def registerTask(request):
		return Views.dash(request)

	def saveTaskRegistration(request):
		if request.POST:
			return Views.dash(request)


	# auxiliary methods
	@csrf_protect
	def fetchPlayerState(request):
		playerId = request.session.get("username")

		newSessionState = {}
		
		newSessionState["myStateGrid"] = playerBridge.getPlayerStateGrid(playerId)
		newSessionState["myCharacteristics"] = playerBridge.getPlayerCurrCharacteristics(playerId)
		newSessionState["myPersonality"] = playerBridge.getPlayerPersonality(playerId)

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