# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from jokeFeed.models import UserProfile, Joke


#template of templates
def base(request):
	context = { }
	return render(request, 'base.html', context)
	
#home/index page. 
def index(request)
	#grab jokes from Joke database
	
	context = {}
	return render(request, 'jokeFeed/index.html', context)

	
#signing in and creating account	
def add_user(request):
	context = { }
	return render(request, 'registration/add_user.html', context)
	
def add_user_add(request):
	newUser = User.objects.create_user(request.POST['uname'],request.POST['email'], request.POST['pwd'])
	#newUser.last_name = request.POST['last_name']
	#newUser.first_name = request.POST['first_name']

	#add to UserProfiles
	newUser.save()
	addUserProf = newUser
	addUserProf.save()
	return HttpResponseRedirect('/')
	
	
#submitting jokes
def add_joke (request)
	context = {}
	return render(request, 'jokeFeed/index.html', context)

def add_joke_add
	context = {}
	return render(request, 'jokeFeed/index.html', context)

