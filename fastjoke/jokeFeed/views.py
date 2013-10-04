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
	# get top joke, but if have viewed, go to the next one. 
	#set current_joke_num if session was not in place before. use try and except. 
	try:
		if request.session['current_joke_num']:
			pass
	except: request.session['current_joke_num'] = 0
	
	#create array of viewed jokes
	request.session['viewed']=[]
	
	next_joke = getNextJoke(request)
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(next_joke.id,)))

	
# signing in and creating account	
def add_user(request):
	context = { }
	return render(request, 'registration/add_user.html', context)
	
def add_user_add(request):
	if request.POST['uname'] not in User.objects.all():
		try:
			newUser = User.objects.create(username=request.POST['uname'], password=request.POST['pwd'])
			# newUser.last_name = request.POST['last_name']
			# newUser.first_name = request.POST['first_name']

			# add to UserProfiles
			newUser.save()
		
			#temp = User.objects.get(username=request.POST['uname'])
			addUserProf = UserProfile(user=newUser, numJokesPosted=0)
			addUserProf.save()
			return HttpResponseRedirect('/')
		except:
			error=1
			context = {'error':error}
			return render(request, 'registration/add_user.html', context)
			
	
	
@login_required()
def fav(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	curUser=UserProfile.objects.get(user=User.objects.get(id=request.user.id))
	if curUser.favorites.filter(id=current_joke.id).exists():
		curUser.favorites.remove(current_joke)
	else:
		curUser.favorites.add(current_joke)
	curUser.save()
	
	#next_joke = getNextJoke(request)
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(current_joke.id,)))

	
# submitting jokes
@login_required()
def submit(request):
	context = {}
	return render(request, 'jokeFeed/submit.html', context)
	
def submit_submit(request):
	new_joke = Joke(owner=request.user, text=request.POST['joke'], views=0, up=0, down=0, date=datetime.date.today())
	new_joke.save()
	curUser=UserProfile.objects.get(user=User.objects.get(id=request.user.id))	
	curUser.numJokesPosted +=1
	curUser.save()
	
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(new_joke.id,)))
	
# viewing jokes
def detail(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	if request.user.is_authenticated():
		curUser=UserProfile.objects.get(user=User.objects.get(id=request.user.id))
		# boolean if curUser has this joke favorited
		fav_bool = curUser.favorites.filter(id=joke_id).exists()
	else:
		fav_bool = 0
	
	context = {'current_joke' : current_joke, 'fav_bool' : fav_bool}
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
	
	#algorithm for next joke
	next_joke = getNextJoke(request)
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(next_joke.id,)))

def getNextJoke(request):
	#append viewed joke to list. 
	request.session['viewed'].append(request.session['current_joke_num'])
	
	next_joke_num=find_unviewed_joke(request,request.session['current_joke_num'])
	
	#set new current_joke_num for session. 
	request.session['current_joke_num']=next_joke_num
	return get_object_or_404(Joke, pk=request.session['current_joke_num'])

def find_unviewed_joke(request,joke_id):
	#checks array of viewed jokes. If not there, returns number of unviewed joke
	if joke_id + 1 not in request.session['viewed']:
		joke_id += 1
		return joke_id
	else:
		find_unviewed_joke(joke_id+1)