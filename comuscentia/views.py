from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string # check if really used
from .models import Room, Participation, Keyword
from .forms import RoomForm, SearchForm
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

def participants(room):
	return len(Participation.objects.filter(room=room))

def search(request):
	if request.method == 'POST' and request.is_ajax():
		print("ajax search view reached")
		query = request.POST.get('query')
		print(query)
		response_data = {}

		#search algorithm
		query = query.replace(",", "").replace(".", "").replace("?", "").replace("!", "").replace(";", "").replace(":", "").replace('"', "")
		query = query.lower()
		words = query.split()
		stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', "don't", 'should', 'now', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
		keywords = []
		for word in words:
			if word not in stop_words:
				if re.search(r"er$", word) or re.search(r"ed$", word):
					word = word[:-2]
				elif re.search(r"ing$", word):
					word = word[:-3]
				keywords.append(word)
		print(keywords)
		all_results = [] # может добавить сразу комнату по англ с значением совпадения = 1, заместо рекомендации
		for keyword in keywords:
			if len(keyword) < 3:
				keyword_rooms = Keyword.objects.filter(keyword=keyword)
			else:
				keyword_rooms = Keyword.objects.filter(keyword__icontains=keyword) # убрать 'i', когда сделаю, чтоб ключевые слова были в lowercase
			#if keyword_rooms:
				#keys = [keyword_room.keyword for keyword_room in keyword_rooms] # new keywords
				#for key in keys:

			if keyword_rooms:
				rooms = [keyword_room.room for keyword_room in keyword_rooms] # new rooms
				result_rooms = [result[0] for result in all_results] # rooms, that are already in result
				for room in rooms:
					# записывать в список (комната, значение совпадения)
					if room in result_rooms: # если комната уже есть в результатах
						# найти room в all_results, и добавить 1 к соответствующему значению
						index = result_rooms.index(room)
						print('all_results[index][1]: ' + str(all_results[index][1]))
						all_results[index][1] += 1
					else:
						all_results.append([room, 1])
		if all_results:
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
			response_data['pk'] = [result.pk for result in results]
			response_data['title'] = [result.title for result in results]
			response_data['description'] = [result.description for result in results]
			response_data['participants'] = [participants(result) for result in results]
			return JsonResponse(response_data)
		else:
			print('0 results')
	else:
		print("ajax view doesn't work")
	return JsonResponse(status=404)

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
			participant = Participation(user=request.user, room=room)
			participant.save()
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
