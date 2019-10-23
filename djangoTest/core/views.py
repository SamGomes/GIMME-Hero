import json
import sys
sys.path.append('../../GIMME/GIMME/GIMMECore/')

from django.shortcuts import render,render_to_response, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from djangoTest.core.models import User

from GIMMECore import *



# view models?
currAdaptationState = []
readyForNewActivity = False
currSelectedPlayers = ['Daniel', 'Nick', 'ssa']


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


class CustomPlayerModelBridge(PlayerModelBridge):
	
	def savePlayerState(self, playerId, newState):
		player = User.objects.get(username = playerId)
		player.currState = newState
		player.save(update_fields=["active"])

	def resetPlayer(self, playerId):
		return 0


	def getSelectedPlayerIds(self):
		return currSelectedPlayers

	def getPlayerName(self, playerId):
		player = User.objects.get(username=playerId)
		return player.fullName

	
	def getPlayerCurrProfile(self,  playerId):
		player = User.objects.get(username=playerId)
		profile = json.loads(player.currState)["profile"]
		return InteractionsProfile(K_cl= profile["K_cl"], K_cp= profile["K_cp"], K_i= profile["K_i"])

	def getPlayerPastModelIncreases(self, playerId):
		player = User.objects.get(username=playerId)
		return json.loads(player.pastModelIncreasesGrid)["cells"]

	def getPlayerCurrCharacteristics(self, playerId):
		player = User.objects.get(username=playerId)
		characteristics = json.loads(player.currState)["characteristics"]
		return PlayerCharacteristics(ability= characteristics["ability"], engagement= characteristics["engagement"])
	
	def getPlayerPersonality(self, playerId):
		player = User.objects.get(username=playerId)
		personality = json.loads(player.personality)
		return InteractionsProfile(K_cl=personality["K_cl"], K_cp=personality["K_cp"], K_i=personality["K_i"])
	
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
taskBridge = CustomTaskModelBridge()


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
		request.session.modified = True
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

	# functioning methods
	def newAvailablePlayer(request):
		username = request.session.get('username')
		print("globals: "+str(currSelectedPlayers))
		if not username in currSelectedPlayers:
			currSelectedPlayers.append(username)
		return render(request, 'student/waiting.html')


	def startAdaptation(request):
		currAdaptationState = adaptation.iterate()
		request.session["currAdaptationState"] = json.dumps(currAdaptationState, default=lambda o: o.__dict__, sort_keys=True)
		readyForNewActivity = True
		request.session.modified = True
		return Views.dash(request)



	def registerTask(request):
		return Views.dash(request)

	def saveTaskRegistration(request):
		if request.POST:
			
			# playerBridge.registerNewPlayer(playerId, name, currState, pastModelIncreasesGrid, currModelIncreases, personality)
			return Views.dash(request)


	def displayTask(request):
		return render(request, 'student/activity.html')

	def saveTaskResults(request):
		if request.POST:
			playerId = request.session.get('username')
			playerBridge.setPlayerCharacteristics(playerId, "{ 'ability': '"+request.POST["ability"]+"', 'engagement': '"+request.POST["engagement"]+"'}")
			playerBridge.setPlayerCurrProfile(playerId, "{ 'K_i': '0.3', 'K_cp': '0.1', 'K_cl': '0.5'}")
			return Views.dash(request)