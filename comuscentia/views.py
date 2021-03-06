from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from .models import Room, Participation, Keyword, Message, Verification
from .forms import RoomForm, SearchForm, MessageForm, MailingForm
from datetime import datetime
import re

def index(request):
	form = SearchForm()
	if request.user.is_authenticated:
		user_rooms = Participation.objects.filter(user=request.user)
		rooms = []
		for user_room in user_rooms:
			print(user_room)
			room = user_room.room
			print(room)
			rooms.append((room, participants(room)))
			print(rooms)
		return render(request, 'comuscentia/index.html', {'form': form, 'rooms': rooms})
	else:
		return render(request, 'comuscentia/index.html', {'form': form})

def search(request):
	if request.method == 'POST' and request.is_ajax():
		print("ajax search view reached")
		query = request.POST.get('query')
		print(query)

		#search algorithm
		keywords = get_keywords(query)
		all_results = [] # insert recommended rooms
		for keyword in keywords:
			keyword_rooms = Keyword.objects.filter(keyword__startswith=keyword)
			if keyword_rooms:
				rooms = [keyword_room.room for keyword_room in keyword_rooms] # new rooms
				for room in rooms:
					# write to list [room, match value]
					result_rooms = [result[0] for result in all_results] # rooms, that are already in result
					if room in result_rooms: # if room is already in results
						# find room in all_results and add 1 to the appropriate value
						index = result_rooms.index(room)
						print('all_results[index][1]: ' + str(all_results[index][1]))
						all_results[index][1] += 1 # может +1 только когда полное совпадение keyword, в других случаях чем слабее совпадение (чем меньше % слова совпадает), тем меньше добавлять. Но для этого нужна сортировка, а не просто max. Тогда можно будет удалить однобуквенные стоп-слова
					else:
						all_results.append([room, 1])
		if all_results:
			# some prints to console for debagging
			print('all_results: ' + str(all_results))
			result_nums = [result[1] for result in all_results] # all_results[1]
			print('result_nums: ' + str(result_nums))
			max_num = max(result_nums)
			print('Max: ' + str(max_num))
			indexes = []
			print('indexes1:')
			index = 0
			for num in result_nums:
				if num == max_num:
					print(index)
					indexes.append(index)
				index += 1
			if len(indexes) < 10 and max_num > 1:
				print('Looking for more indexes with max_num-1')
				index = 0
				for num in result_nums:
					if num == (max_num - 1):
						print(index)
						indexes.append(index)
					index += 1
				if index > 0:
					print('it worked')
				# потом найти максимальное значение, и выбрать все комнаты с этим значением. Если будет мало, взять комнаты со значением max - 1
				# всегда обрабатывать только лучшие n результатов (комнат). Если наибольших значений совпадений больше n, остальные не трогать
				# Если же меньше, брать значения совпадений поменьше, пока не будет n. Или нет.
			results = []
			print('indexes2:')
			for index in indexes:
				print(index)
				results.append(all_results[index][0])
			response_data = {}
			response_data['pk'] = [result.pk for result in results]
			response_data['title'] = [result.title for result in results]
			response_data['description'] = [result.description for result in results]
			response_data['participants'] = [participants(result) for result in results]
			response_data['verificated'] = [result.verificated for result in results]
			return JsonResponse(response_data)
		else:
			print('0 results')
	else:
		print("ajax view doesn't work")
	return JsonResponse(status=404) # no results

@login_required
def room(request, pk):
	room = get_object_or_404(Room, pk=pk)
	if request.method == "POST" and request.is_ajax():
		msg = Message.objects.create(author = request.user, time = timezone.now(), room = room)
		msg.message = request.POST.get('msg')
		msg.save()
		room.msgs += 1
		room.save()
		if msg:
			new_msg = {}
			new_msg['author'] = msg.author.username
			new_msg['msg'] = msg.message
			new_msg['time'] = msg.time.strftime("%B %d, %Y, %I:%M %p")
			print(new_msg)
			return JsonResponse(new_msg)
		else:
			print("send 404")
			return JsonResponse(status=404)
	elif request.method == "POST":
		mailForm = MailingForm(request.POST)
		if mailForm.is_valid():
			subject = request.POST.get('subject_field', room.title + 'Comuscentia') # potential error
			message = request.POST.get('mail_field', 'Looks like empty message was sent. Sorry about this mistake.')
			emails = []
			for participation in Participation.objects.filter(room=room):
				if participation.user != request.user:
					emails.append(participation.user.email)
			send_mail(subject, message + "\nSent from Comuscentia by " + request.user.username + ".", 'request.user.email', emails) #request.user.email OR my email
		return render(request, 'comuscentia/email_sent.html', {'room_pk': room.pk, 'subject': subject, 'message': message + "\nSent from Comuscentia by " + request.user.username + "."})
	else:
		participations = Participation.objects.filter(room=room)
		messages = Message.objects.filter(room=room)
		subscribers = [participation.user for participation in participations] # subscribers list
		count = participants(room)
		mesForm = MessageForm()
		mailForm = MailingForm()
		asked4verif = False
		if Verification.objects.filter(room=room):
			asked4verif = True
		return render(request, 'comuscentia/room.html', {'room': room, 'count': count, 'participants': subscribers, 'messages': messages, 'mesForm': mesForm, 'mailForm': mailForm, 'asked4verif': asked4verif})

def loop(request, pk):
	room = get_object_or_404(Room, pk=pk)
	result = {}
	result['msgs'] = room.msgs
	return JsonResponse(result)

def update(request, pk, new):
	room = get_object_or_404(Room, pk=pk)
	print('UPDATING')
	if request.method == "GET" and request.is_ajax():
		messages = list(Message.objects.filter(room=room))
		print(messages)
		msgs = {}
		msgs['author'] = []
		msgs['msg'] = []
		msgs['time'] = []
		for i in range(1, new+1):
			msg = messages[-i]
			msgs['author'].append(msg.author.username)
			msgs['msg'].append(msg.message)
			msgs['time'].append(msg.time.strftime("%B %d, %Y, %I:%M %p"))
		print(msgs)
		return JsonResponse(msgs)
	else:
		return JsonResponse(status=404)

def verificate(request, pk):
	room = get_object_or_404(Room, pk=pk)
	verif = Verification.objects.create(room = room, time = timezone.now())
	verif.save()
	return HttpResponse('')

@login_required
def new_room(request):
	if request.method == "POST":
		form = RoomForm(request.POST)
		if form.is_valid():
			room = form.save(commit=False)
			room.owner = request.user
			room.created_date = timezone.now()
			room.save()
			participant = Participation(user=request.user, room=room) # add new room + owner to participation table
			participant.save()
			keywords = get_keywords(request.POST['title'])
			for keyword in keywords: # add title-keywords to keywords table one by one
				kw = Keyword(room=room, keyword=keyword)
				kw.save()
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

@login_required
def subscribe(request, pk):
	room = get_object_or_404(Room, pk=pk)
	participant = Participation(user=request.user, room=room)
	participant.save()
	return redirect('room', pk=room.pk)

@login_required
def unsubscribe(request, pk):
	room = get_object_or_404(Room, pk=pk)
	Participation.objects.get(user=request.user, room=room).delete()
	return redirect('room', pk=room.pk)

@login_required
def delete(request, pk):
	Room.objects.get(pk=pk).delete()
	return redirect('index')

def participants(room):
	return len(Participation.objects.filter(room=room))

def get_keywords(title):
	title = title.replace(",", "").replace(".", "").replace("?", "").replace("!", "").replace(";", "").replace(":", "").replace('"', "")
	title = title.lower()
	words = title.split()
	stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', "don't", 'should', 'now', 'b', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	keywords = []
	for word in words:
		if word not in stop_words:
			if re.search(r"er$", word) or re.search(r"ed$", word):
				word = word[:-2]
			elif re.search(r"ing$", word):
				word = word[:-3]
			elif re.search(r"s$", word):
				word = word[:-1]
			keywords.append(word)
	print(keywords)
	return keywords