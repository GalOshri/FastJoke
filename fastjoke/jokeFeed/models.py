from django.db import models
from django.contrib.auth.models import User

class Joke(models.Model):
	owner = models.ForeignKey(User, related_name='owns')
	text = models.TextField(max_length=1000)
	
	#views = models.IntegerField()
	upVotes = models.IntegerField()
	downVotes = models.IntegerField()
	
	date = models.DateTimeField()
	
	def __unicode__(self):
		return self.text
		
	def _get_score(self):
		return self.upVotes - self.downVotes
		
	score = property(_get_score)

	
# Create your models here.
class UserProfile(models.Model):
	#associated with one user
	user = models.OneToOneField(User)
	
	numJokesPosted = models.IntegerField()
	favorites = models.ManyToManyField(Joke, related_name = "favorited_by")
	votedUp = models.ManyToManyField(Joke, related_name = "voted_up_by")
	votedDown = models.ManyToManyField(Joke, related_name = "voted_down_by")
	
	def __unicode__(self):
		return self.user.username

class UserFeedback(models.Model):
	feedback = models.TextField(max_length=2000)
	
	date = models.DateTimeField()
	
	def __unicode__(self):
		return self.feedback

		
