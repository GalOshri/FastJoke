import csv
from django.contrib.auth.models import User
from jokeFeed.models import Joke,UserProfile
import unicodedata
import datetime

jokeList = []

reader=csv.reader(open("joke1.csv","r"), delimiter=",")

for joke in reader: 
	#jokeList.append(joke[0])
	print joke
	
	#modified code from views, submit_submit view
	new_joke = Joke(owner=User.objects.get(username='pg'), text=joke[0].encode('ascii','replace'), upVotes=0, downVotes=0, date=datetime.datetime.today())
	new_joke.save()
	curUser=UserProfile.objects.get(user=User.objects.get(username="pg"))
	curUser.numJokesPosted +=1
	curUser.save()