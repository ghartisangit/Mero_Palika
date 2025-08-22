from django.shortcuts import render, redirect
from complaints.models import Complaint

def home(request):
    return render(request, 'login.html') 