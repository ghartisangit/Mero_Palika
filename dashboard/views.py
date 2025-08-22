from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q

user=get_user_model()

# Create your views here.
@login_required(login_url = 'login')
def municipality_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 'municipality':
        return render(request, 'dashboard/municipality_dashboard.html')
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('login')
    
@login_required(login_url = 'login')  
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        return render(request, 'dashboard/admin_dashboard.html')
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('login')