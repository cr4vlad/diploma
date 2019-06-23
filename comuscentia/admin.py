from django.contrib import admin
from .models import Room, Participation, Keyword, Message, Verification

admin.site.register(Room)
admin.site.register(Participation)
admin.site.register(Keyword)
admin.site.register(Message)
admin.site.register(Verification)
