from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Room, Participation
from .forms import RoomForm

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

@login_required
def new_room(request):
	if request.method == "POST":
		form = RoomForm(request.POST)
		if form.is_valid():
			room = form.save(commit=False)
			room.owner = request.user
			room.created_date = timezone.now()
			room.save()
			return redirect('room', pk=room.pk)
	else:
		form = RoomForm()
	return render(request, 'comuscentia/edit_room.html', {'form': form})

@login_required
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.created_date = timezone.now()
            room.save()
            return redirect('room', pk=room.pk)
    else:
        form = RoomForm(instance=room)
    return render(request, 'comuscentia/edit_room.html', {'form': form})
