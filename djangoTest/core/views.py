# coding: utf-8
from django.shortcuts import render,render_to_response, redirect
from django.views.generic import View
from djangoTest.core.models import User
from djangoTest.core.forms import RegistryForm

from django.core.exceptions import ObjectDoesNotExist

class Views(): #acts as a namespace

	def login(request):
		return render(request, 'login.html')

	def registration(request):
		return render(request, 'registration/student.html')
		# return render(request, 'registration/student.html', { 
  #               'email': username, 
  #               'password': username, 
  #               'username': username, 
  #               'name': name, 
  #               'age': age,
  #               'gender': gender,
  #               'preferences': preferences,
  #           })

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

	def home(request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		if request.POST:
			if(not Views.isRegistered(request)):
				return redirect('/login')

			storedUser = User.objects.get(username = username)
			
			# check if pass is right
			if not storedUser.password == password:
				return redirect('/login')

			homeSwitch = {
		        'student': 'home/student.html',
		        'professor': 'home/professor.html',
		        'designer': 'home/designer.html',
		    }

			#case role is student then...
			return render(request, homeSwitch[storedUser.role], storedUser)
            

	def saveRegistration(request):
		if request.POST:
			if(Views.isRegistered(request)):
				return redirect('/login')
			form = RegistryForm(request.POST)
			print(request.POST)
			if form.is_valid():
				form.save()
				return Views.home(request)
			return redirect('/login')



