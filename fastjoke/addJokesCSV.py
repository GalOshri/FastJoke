import csv
from jokeFeed.models import Joke,UserProfile

jokeList = []

reader=csv.reader(open("jokes.csv","r"), delimiter=",")

for joke in reader: 
	#jokeList.append(joke[0])
	print joke
	
	#modified code from views, submit_submit view
	new_joke = Joke(owner='pg', text=joke[0], upVotes=0, downVotes=0, date=datetime.date.today())
	new_joke.save()
	curUser=UserProfile.objects.get(user=User.objects.get(username="pg"))
	curUser.numJokesPosted +=1
	curUser.save()