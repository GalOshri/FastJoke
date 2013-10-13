from django.contrib import admin
from jokeFeed.models import Joke, UserProfile, UserFeedback

admin.site.register(Joke)
admin.site.register(UserProfile)
admin.site.register(UserFeedback)