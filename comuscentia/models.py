from django.db import models
from django.conf import settings
from django.utils import timezone

class Room(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	created_date = models.DateTimeField(default=timezone.now)
	description = models.CharField(max_length=200)
	textblock = models.TextField(default="Text field for learning stuff. We advice to start with a link to the chat.")
	#close = models.BooleanField(default=False) # if room is closed for new participants, don't show in search

	def __str__(self):
		return '%s by %s' % (self.title, self.owner)

class Participation(models.Model): # 1 entry for each act of subscription
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users')
	room = models.ForeignKey(Room, on_delete=models.CASCADE)

	def __str__(self):
		return '%s in %s' % (self.user, self.room)

class Keyword(models.Model): # 1 entry for each keyword in each room
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	keyword = models.CharField(max_length=50)

	def __str__(self):
		return '(%s) : %s' % (self.room, self.keyword)