import sys
print(sys.path)
sys.path.append('/home/samgomes/Documents/doutoramento/reps/GIMME-rep/GIMME/GIMMECore/')

# coding: utf-8
from django.shortcuts import render,render_to_response, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist

from GIMMECore import *
from djangoTest.core.GIMMEModelBridges import *

playerBridge = CustomPlayerModelBridge()
taskBridge = CustomTaskModelBridge()

adaptation = Adaptation()
adaptation.init(KNNRegression(5), RandomConfigsGen(), WeightedFitness(PlayerCharacteristics(ability=0.5, engagement=0.5)), playerBridge, taskBridge, name="", numberOfConfigChoices=50, maxNumberOfPlayersPerGroup = 5, difficultyWeight = 0.5, profileWeight=0.5)

class Views(): #acts as a namespace

	def home(request):
		return render(request, 'home.html')

	def login(request):
		return render(request, 'login.html')

	def registration(request):
		return render(request, 'registration/student.html')

	def isRegistered(userLogin):
		username = userLogin.POST.get('username')
		if(not username == None):
			try:
				storedUser = User.objects.get(username = username)
			except ObjectDoesNotExist as e:
				print("one")
				return False
		email = userLogin.POST.get('email')
		if(not email == None):
			try:
				storedUser = User.objects.get(email = email)
			except ObjectDoesNotExist as e:
				print("two")
				return False
		return True

	def dash(request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		if request.POST:
			if(not Views.isRegistered(request)):
				return redirect('/home')

			storedUser = User.objects.get(username = username)

			# check if pass is right
			if not storedUser.password == password:
				return redirect('/home')

			dashSwitch = {
		        'student': 'dash/student.html',
		        'professor': 'dash/professor.html',
		        'designer': 'dash/designer.html',
		    }

			#case role is student then...
			return render(request, dashSwitch[storedUser.role], storedUser.__dict__)
            

	def saveRegistration(request):
		if request.POST:
			if(Views.isRegistered(request)):
				return redirect('/home')
			print(request.POST)
			
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

			# Adaptation stuff
			entry.currState = json.dumps(PlayerState())
			entry.pastModelIncreasesGrid = json.dumps(PlayerStateGrid())
			entry.personality = json.dumps(InteractionProfile())
			entry.currIncreases = json.dumps(InteractionProfile())
			print(requestInfo)
			entry.save()
			
			# playerBridge.registerNewPlayer(playerId, name, currState, pastModelIncreasesGrid, currModelIncreases, personality)
			return Views.dash(request)

	def newTask(request):
		iteration = adaptation.iterate()
		for i in range(len(iteration.groups)):
			currGroup = iteration.groups[i]
			print(currGroup.__dict__)



