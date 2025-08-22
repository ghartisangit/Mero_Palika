from django.shortcuts import render, redirect
from complaints.models import Ward


def home(request):
    event_images = [f'images/items/IG{i}.jpg' for i in range(1, 10)]
    return render(request, 'home.html', {'event_images': event_images}) 

def welcome(request):
    return render(request, 'home.html') 