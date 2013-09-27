# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from jokeFeed.models import UserProfile, Joke
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
import datetime


# template of templates
def base(request):
	context = { }
	return render(request, 'base.html', context)
	
# home/index page. 
def index(request):
	# get top joke
	request.session['current_joke_num'] = 0
	next_joke = getNextJoke(request)
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(next_joke.id,)))

	
# signing in and creating account	
def add_user(request):
	context = { }
	return render(request, 'registration/add_user.html', context)
	
def add_user_add(request):
	newUser = User.objects.create_user(request.POST['uname'], password=request.POST['pwd'])
	# newUser.last_name = request.POST['last_name']
	# newUser.first_name = request.POST['first_name']

	# add to UserProfiles
	newUser.save()
	addUserProf = newUser
	addUserProf.save()
	return HttpResponseRedirect('/')
	
	
# submitting jokes
@login_required()
def submit(request):
	context = {}
	return render(request, 'jokeFeed/submit.html', context)
	
def submit_submit(request):
	new_joke = Joke(owner=request.user, text=request.POST['joke'], views=0, up=0, down=0, date=datetime.date.today())
	new_joke.save()
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(new_joke.id,)))
	
# viewing jokes
def detail(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	context = {'current_joke' : current_joke}
	return render(request, 'jokeFeed/detail.html', context)
	
def up(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	current_joke.up += 1
	current_joke.save()
	next_joke = getNextJoke(request)
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(next_joke.id,)))

def down(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	current_joke.down += 1
	current_joke.save()
	next_joke = getNextJoke(request)
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(next_joke.id,)))

def getNextJoke(request):
	request.session['current_joke_num'] += 1
	return get_object_or_404(Joke, pk=request.session['current_joke_num'])