# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from jokeFeed.models import UserProfile, Joke, UserFeedback
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth import authenticate, login
	
# home/index page. 
def index(request):
	# get top joke, but if have viewed, go to the next one. 
	#set current_joke_num if session was not in place before. use try and except. 
	#try:
	#	if request.session['current_joke_num']:
	#		pass
	#except: request.session['current_joke_num'] = 0
	
	#create array of viewed jokes
	#request.session['viewed']=[]
	if request.user.is_authenticated():
		request.session['current_joke_num'] = 1
		curUser=UserProfile.objects.get(user=User.objects.get(id=request.user.id))
		next_joke = getNextJoke(request, curUser)
		return HttpResponseRedirect(reverse('jokeFeed:detail', args=(next_joke.id,)))
		
	else:

		top_five = []
		for i in range(3, 8):
			top_five.append(getRankJoke(i))
		context = { 'top_five' : top_five}
		return render(request, 'jokeFeed/index.html', context)

	
# signing in and creating account	
def add_user(request):
	context = { }
	return render(request, 'registration/add_user.html', context)
	
def add_user_add(request):
	try:
		newUser = User.objects.create(username=request.POST['uname'])
		newUser.set_password(request.POST['pwd'])
		# newUser.last_name = request.POST['last_name']
		# newUser.first_name = request.POST['first_name']

		# add to UserProfiles
		newUser.save()

		#temp = User.objects.get(username=request.POST['uname'])
		addUserProf = UserProfile(user=newUser, numJokesPosted=0)
		addUserProf.save()
		
		#add user to session
		auth = authenticate(username=request.POST['uname'], password=request.POST['pwd'])
		login(request, auth)
		return HttpResponseRedirect('/')
	
	except:
		error=1
		context = {'error':error}
		return render(request, 'registration/add_user.html', context)
	
	
	
@login_required()
def fav(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	curUser=UserProfile.objects.get(user=User.objects.get(username=request.user.username))
	if curUser.favorites.filter(id=current_joke.id).exists():
		curUser.favorites.remove(current_joke)
	else:
		curUser.favorites.add(current_joke)
	curUser.save()
	
	#next_joke = getNextJoke(request)
	if request.GET['next']:
		return HttpResponseRedirect(request.GET['next'])
	else:
		return HttpResponseRedirect(reverse('jokeFeed:detail', args=(current_joke.id,)))

	
# submitting jokes
@login_required()
def submit(request):
	context = {}
	return render(request, 'jokeFeed/submit.html', context)
	
@login_required()
def submit_submit(request):
	new_joke = Joke(owner=request.user, text=request.POST['joke'], upVotes=0, downVotes=0, date=datetime.date.today())
	new_joke.save()
	curUser=UserProfile.objects.get(user=User.objects.get(id=request.user.id))	
	curUser.numJokesPosted +=1
	curUser.save()
	
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(new_joke.id,)))
	
# viewing jokes
@login_required()
def detail(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	curUser=UserProfile.objects.get(user=User.objects.get(id=request.user.id))
	# boolean if curUser has this joke favorited
	fav_bool = curUser.favorites.filter(id=joke_id).exists()
	
	context = {'current_joke' : current_joke, 'fav_bool' : fav_bool}
	return render(request, 'jokeFeed/detail.html', context)
	
@login_required()
def up(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	curUser=UserProfile.objects.get(user=User.objects.get(id=request.user.id))
	
	if not curUser.votedUp.filter(id=current_joke.id).exists():
		curUser.votedUp.add(current_joke)
		current_joke.upVotes += 1
		current_joke.save()
		curUser.save()
		
	next_joke = getNextJoke(request, curUser)
	if next_joke == 0:
		context = {}
		return render(request, 'jokeFeed/no_life.html', context)
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(next_joke.id,)))

@login_required()
def down(request, joke_id):
	current_joke = get_object_or_404(Joke, pk=joke_id)
	curUser=UserProfile.objects.get(user=User.objects.get(id=request.user.id))

	if not curUser.votedDown.filter(id=current_joke.id).exists():	
		curUser.votedDown.add(current_joke)
		current_joke.downVotes += 1
		current_joke.save()
		curUser.save()
	
	#algorithm for next joke
	next_joke = getNextJoke(request, curUser)
	if next_joke == 0:
		context = {}
		return render(request, 'jokeFeed/no_life.html', context)
	return HttpResponseRedirect(reverse('jokeFeed:detail', args=(next_joke.id,)))

def getNextJoke(request, curUser):
	#append viewed joke to list. 
	#request.session['viewed'].append(request.session['current_joke_num'])
	
	num_jokes = len(Joke.objects.all())
	
	next_joke_num = request.session['current_joke_num']
	
	while next_joke_num <= num_jokes:
		
		request.session['current_joke_num'] = next_joke_num
		if Joke.objects.filter(pk=next_joke_num).exists():
			next_joke = getRankJoke(next_joke_num)
			if not (curUser.votedDown.filter(id=next_joke.id).exists() or curUser.votedUp.filter(id=next_joke.id).exists()):
				return next_joke
		next_joke_num = request.session['current_joke_num'] + 1
	
	return 0
	
def getRankJoke(rank):
	rank = rank
	new_joke = Joke.objects.get(pk=rank)
	return get_object_or_404(Joke, pk=new_joke.id)

@login_required()		
def view_profile(request, username):
	if not username:
		curUser = UserProfile.objects.get(user=User.objects.get(id=request.user.id))
	else:
		try:
			curUser = UserProfile.objects.get(user=User.objects.get(username=username))
		except:
			return HttpResponseRedirect(reverse('jokeFeed:index'))
	joke_list = curUser.user.owns.all()
	context = { 'joke_list' : joke_list }
	return render(request, 'jokeFeed/profile.html', context)
	
@login_required()		
def view_fav(request):
	curUser = UserProfile.objects.get(user=User.objects.get(id=request.user.id))
	context = { 'profile' : curUser }
	return render(request, 'jokeFeed/fav.html', context)
	
# feedback
def feedback(request):
	context = {}
	return render(request, 'jokeFeed/feedback.html', context)
	
def feedback_submit(request):
	new_feedback = UserFeedback(feedback=request.POST['feedback'], date=datetime.date.today())
	new_feedback.save()
	
	return HttpResponseRedirect(reverse('jokeFeed:index'))
	
