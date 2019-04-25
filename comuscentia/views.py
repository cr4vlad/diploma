from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Participation

def index(request):
	if request.user.is_authenticated:
		user_rooms = Participation.objects.filter(user=request.user) #.order_by('room.title')
		return render(request, 'comuscentia/index.html', {'user_rooms': user_rooms})
	else:
		return render(request, 'comuscentia/index.html', {})

@login_required
def room(request, pk):
	room = get_object_or_404(Room, pk=pk)
	return render(request, 'comuscentia/room.html', {'room': room})
