# coding: utf-8
from django.shortcuts import render,render_to_response
from django.views.generic import View
from djangoTest.core.models import User

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

	def saveRegistration(request):
		if request.POST:
			form = RegistryForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('/home/')
			return redirect('/login/')



	def home(request):
		# logout(request)
		username = password = ''
		if request.POST:
			print(str(request))
			username = request.POST.get('username')
			password = request.POST.get('password')

			role = "student";

			homeSwitch = {
		        'student': 'home/student.html',
		        'professor': 'homes/professor.html',
		        'designer': 'homes/designer.html',
		    };

			#case role is student then...
			return render(request, homeSwitch[role], { 
                'username': username, 
                'password': password
            })
