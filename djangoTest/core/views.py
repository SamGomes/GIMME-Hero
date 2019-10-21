import sys
sys.path.append('../../GIMME/GIMME/GIMMECore/')

# coding: utf-8
from django.shortcuts import render,render_to_response, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist

from GIMMECore import *
from djangoTest.core.GIMMEModelBridges import *

from django.http import HttpResponse

playerBridge = CustomPlayerModelBridge()
taskBridge = CustomTaskModelBridge()

adaptation = Adaptation()
adaptation.init(KNNRegression(5), RandomConfigsGen(), WeightedFitness(PlayerCharacteristics(ability=0.5, engagement=0.5)), playerBridge, taskBridge, name="", numberOfConfigChoices=50, maxNumberOfPlayersPerGroup = 5, difficultyWeight = 0.5, profileWeight=0.5)
# adaptation.iterate()

currSelectedPlayers = []

class Views(): #acts as a namespace

	def home(request):
		if(Views.isLoggedIn(request)):
			return Views.dash(request)
		return render(request, 'home.html')

	def login(request):
		print(request.session.modified)
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

	def registration(request):
		return render(request, 'student/registration.html')

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
            
	def saveRegistration(request):
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
		currSelectedPlayers.append(request.session.get('username'))
		return render(request, 'student/waiting.html')



