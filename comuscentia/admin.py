from django.contrib import admin
from .models import Room, Participation, Keyword, Message

admin.site.register(Room)
admin.site.register(Participation)
admin.site.register(Keyword)
admin.site.register(Message)
