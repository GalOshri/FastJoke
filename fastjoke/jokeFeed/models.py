from django.db import models
from django.contrib.auth.models import User

class Joke(models.Model):
	owner = models.ForeignKey(User, related_name='owns')
	text = models.TextField(max_length=1000)
	
	#views = models.IntegerField()
	upVotes = models.IntegerField()
	downVotes = models.IntegerField()
	
	date = models.DateField()
	
	def __unicode__(self):
		return self.text

# Create your models here.
class UserProfile(models.Model):
	#associated with one user
	user = models.OneToOneField(User)
	
	numJokesPosted = models.IntegerField()
	favorites = models.ManyToManyField(Joke, related_name = "joke_favorites")
	votedUp = models.ManyToManyField(Joke, related_name = "joke_votedUp")
	votedDown = models.ManyToManyField(Joke, related_name = "joke_votedDown")
	
	def __unicode__(self):
		return self.user.username

		
