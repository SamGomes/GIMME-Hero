import json
import sys
sys.path.append('../../GIMME/GIMMECore/')

from django.shortcuts import render,render_to_response, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from djangoTest.core.models import User
from djangoTest.core.models import Task
from djangoTest.core.models import ServerState

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
	def getCurrSelectedPlayers(self):
		serverState = ServerState.objects.first()
		currSelectedPlayers = json.loads(serverState.currSelectedPlayers)
		return currSelectedPlayers

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

serverStateModelBridge = ServerStateModelBridge()




class CustomTaskModelBridge(TaskModelBridge):
	
	def getSelectedTaskIds(self):
		return []

	def getTaskInteractionsProfile(self, taskId):
		return InteractionsProfile()

	def getTaskMinRequiredAbility(self, taskId):
		return 0

	def getTaskDifficultyWeight(self, taskId):
		return 0

	def getTaskProfileWeight(self, taskId):
		return 0

taskBridge = CustomTaskModelBridge()



class CustomPlayerModelBridge(PlayerModelBridge):
	
	def savePlayerState(self, playerId, newState):
		player = User.objects.get(username = playerId)
		playerStateGrid = self.getPlayerPastModelIncreases(playerId)
		print(playerStateGrid)
		playerStateGrid.pushToGrid(newState)
		player.pastModelIncreasesGrid = json.dumps(playerStateGrid, default=lambda o: o.__dict__)
		player.save()

	def resetPlayer(self, playerId):
		return 0


	def getSelectedPlayerIds(self):
		return serverStateModelBridge.getCurrSelectedPlayers()

	def getPlayerName(self, playerId):
		player = User.objects.get(username=playerId)
		return player.fullName

	
	def getPlayerCurrProfile(self,  playerId):
		player = User.objects.get(username=playerId)
		profile = json.loads(player.currState)["profile"]
		return InteractionsProfile(K_cl=float(profile["K_cl"]), K_cp=float(profile["K_cp"]), K_i=float(profile["K_i"]))

	def getPlayerPastModelIncreases(self, playerId):
		player = User.objects.get(username=playerId)
		playerStateGrid = json.loads(player.pastModelIncreasesGrid)
		cells = []
		for state in playerStateGrid["cells"]:
			characteristics = state["characteristics"]
			characteristics = PlayerCharacteristics(ability= float(characteristics["ability"]), engagement= float(characteristics["engagement"]))

			profile = state["profile"]
			profile = InteractionsProfile(K_cl=float(profile["K_cl"]), K_cp=float(profile["K_cp"]), K_i=float(profile["K_i"]))
			
			cells.append(PlayerState(profile = profile, characteristics = characteristics, dist=state["dist"]))
		return PlayerStateGrid(cells=cells, numCells=int(playerStateGrid["numCells"]), maxAmountOfStoredProfilesPerCell=int(playerStateGrid["maxAmountOfStoredProfilesPerCell"]))

	def getPlayerCurrCharacteristics(self, playerId):
		player = User.objects.get(username=playerId)
		characteristics = json.loads(player.currState)["characteristics"]
		return PlayerCharacteristics(ability= float(characteristics["ability"]), engagement= float(characteristics["engagement"]))
	
	def getPlayerPersonality(self, playerId):
		player = User.objects.get(username=playerId)
		personality = json.loads(player.personality)
		return InteractionsProfile(K_cl=float(personality["K_cl"]), K_cp=float(personality["K_cp"]), K_i=float(personality["K_i"]))
	
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

	def setPlayerCurrProfile(self, playerId, profile):
		player = User.objects.get(username=playerId)
		newState = self.getPlayerCurrState(playerId)
		newState.profile = profile
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()

playerBridge = CustomPlayerModelBridge()




# init server state
serverStateModelBridge.setCurrAdaptationState([])
serverStateModelBridge.setReadyForNewActivity(False)
serverStateModelBridge.setCurrSelectedPlayers([])


adaptation = Adaptation()
adaptation.init(KNNRegression(5), RandomConfigsGen(), WeightedFitness(PlayerCharacteristics(ability=0.5, engagement=0.5)), playerBridge, taskBridge, name="", numberOfConfigChoices=50, maxNumberOfPlayersPerGroup = 5, difficultyWeight = 0.5, profileWeight=0.5)



class Views(): #acts as a namespace

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

		#case role is student then...
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
			
			# playerBridge.registerNewPlayer(playerId, name, currState, pastModelIncreasesGrid, currModelIncreases, personality)
			return Views.dash(request)


	@csrf_protect
	def newAvailablePlayer(request):
		username = request.session.get('username')
		# print("globals: "+str(currSelectedPlayers))
		currSelectedPlayers = serverStateModelBridge.getCurrSelectedPlayers();
		if not username in currSelectedPlayers:
			currSelectedPlayers.append(username)
		serverStateModelBridge.setCurrSelectedPlayers(currSelectedPlayers)
		return HttpResponse('ok')




	# student methods
	def displayTask(request):
		return render(request, 'student/activity.html')

	def saveTaskResults(request):
		if request.POST:
			playerId = request.session.get('username')
			playerBridge.setPlayerCharacteristics(playerId, PlayerCharacteristics(ability=request.POST["ability"], engagement=request.POST["engagement"]))
			playerBridge.setPlayerCurrProfile(playerId, InteractionsProfile(K_i=0.3, K_cp=0.1, K_cl=0.5))
			playerBridge.savePlayerState(playerId, playerBridge.getPlayerCurrState(playerId))
			return Views.dash(request)




	# professor methods
	def startAdaptation(request):
		currAdaptationState = adaptation.iterate()
		request.session["currAdaptationState"] = json.dumps(currAdaptationState, default=lambda o: o.__dict__, sort_keys=True)
		serverStateModelBridge.setCurrAdaptationState(currAdaptationState)
		serverStateModelBridge.setReadyForNewActivity(True)
		request.session.save()
		return Views.dash(request)



	def registerTask(request):
		return Views.dash(request)

	def saveTaskRegistration(request):
		if request.POST:
			# playerBridge.registerNewPlayer(playerId, name, currState, pastModelIncreasesGrid, currModelIncreases, personality)
			return Views.dash(request)


	@csrf_protect
	def fetchServerState(request):
		newSessionState = {}
		
		request.session["currSelectedPlayers"] = serverStateModelBridge.getCurrSelectedPlayers()
		newSessionState["currSelectedPlayers"] = request.session["currSelectedPlayers"]

		request.session["readyForNewActivity"] = serverStateModelBridge.isReadyForNewActivity()
		newSessionState["readyForNewActivity"] = request.session["readyForNewActivity"]

		if(request.session['role'] == 'professor'):
			request.session["currAdaptationState"] = serverStateModelBridge.getCurrAdaptationState()
			newSessionState["currAdaptationState"] = request.session["currAdaptationState"]

		request.session.save()
		newSession = json.dumps(newSessionState, default=lambda o: o.__dict__, sort_keys=True)
		return HttpResponse(newSession)