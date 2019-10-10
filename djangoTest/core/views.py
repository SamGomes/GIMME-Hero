# coding: utf-8
from django.shortcuts import render,render_to_response, redirect
from django.views.generic import View
from djangoTest.core.models import User
from djangoTest.core.forms import RegistryForm

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

	def home(request):
		username = password = ''
		if request.POST:
			print(str(request))
			username = request.POST.get('username')
			password = request.POST.get('password')

			role = "student";

			homeSwitch = {
		        'student': 'home/student.html',
		        'professor': 'home/professor.html',
		        'designer': 'home/designer.html',
		    };

			#case role is student then...
			return render(request, homeSwitch[role], { 
                'username': username, 
                'password': password
            })

	def saveRegistration(request):
		if request.POST:
			form = RegistryForm(request.POST)
			print(request.POST)
			if form.is_valid():
				# form.save()
				return Views.home(request)
			return redirect('/login')



