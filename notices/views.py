from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Information

@login_required
def create_information(request):
    user = request.user
    if user.user_type not in ['municipality', 'admin']:
        messages.error(request, "You are not authorized to create information.")
        return redirect('list_information')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        ward = getattr(user, 'ward', None)  # Get user's ward

        if not title or not description:
            messages.error(request, "Please fill all fields.")
            return redirect('create_information')

        Information.objects.create(
            user=user,
            title=title,
            description=description,
            ward=ward
        )
        messages.success(request, "Information uploaded successfully.")
        return redirect('list_information')

    return render(request, 'information/create_information.html')


@login_required
def list_information(request):
    user = request.user
    informations = Information.objects.none() 

   
    if user.user_type == 'admin':
        informations = Information.objects.all().order_by('-id')
        
    elif user.user_type == 'municipality':
        informations = Information.objects.filter(ward=user.ward).order_by('-id')

    else:
        informations = Information.objects.none()

    return render(request, 'information/list_information.html', {
        'informations': informations
    })


@login_required
def edit_information(request, id):
    info = get_object_or_404(Information, id=id)

    if request.user.user_type not in ['municipality', 'admin']:
        messages.error(request, "You are not authorized to edit this information.")
        return redirect('list_information')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title and description:
            info.title = title
            info.description = description
            info.save()
            messages.success(request, "Information updated successfully.")
            return redirect('list_information')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'information/edit_information.html', {'info': info})


@login_required
def delete_information(request, id):
    info = get_object_or_404(Information, id=id)

    if request.user.user_type not in ['municipality', 'admin']:
        messages.error(request, "You are not authorized to delete this information.")
        return redirect('list_information')

    info.delete()
    messages.success(request, "Information deleted successfully.")
    return redirect('list_information')

@login_required
def my_search_information(request):
    keyword = request.GET.get('category', '').strip()
    user = request.user

    if keyword: 
        if user.user_type == 'admin':
            informations = Information.objects.filter(title__icontains=keyword).order_by('-id')
        elif user.user_type == 'municipality':
            informations = Information.objects.filter(ward=user.ward, title__icontains=keyword).order_by('-id')
        else:  
            informations = Information.objects.filter(title__icontains=keyword).order_by('-id')
    else:
        if user.user_type == 'admin':
            informations = Information.objects.all().order_by('-id')
        elif user.user_type == 'municipality':
            informations = Information.objects.filter(ward=user.ward).order_by('-id')
        else: 
            informations = Information.objects.none()

    return render(request, 'information/list_information.html', {'informations': informations})



from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse


def send_email(subject, msg, recipent_list):
    send_mail(
        subject,
        msg,
        settings.EMAIL_HOST_USER,
        recipent_list,
        fail_silently = False
        )
    
def is_admin(user):
    return user.is_staff or user.is_superuser

def create_notice(request):
    return render(request, 'notices/create_notice.html')


# @login_required
@csrf_exempt
@user_passes_test(is_admin)
def create_noticeyes(request):
    print("Request method:", request.method)
    print("POST data:", request.POST)
    print("User:", request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        print(title, description)
        if not title or not description:
            messages.error(request, "Title and description are required.")
            return redirect("create_notice")

        
        ward = getattr(request.user, "ward", None)

        Notice.objects.create(
            user=request.user,
            title=title,
            description=description,
           
            ward=ward,
        )
       
        messages.success(request, "Notice created successfully!")
        notices = Notice.objects.all().order_by('-created_at')
        return render(request, "notices/notice_display.html", {"notices": notices})

    return render(request, "notice_display.html", {"notices":notices})

def create_vacancy(request):
    return render(request, 'notices/create_vacancy.html')


@login_required
@user_passes_test(is_admin)
def create_vacancy(request):
    
    statuses = TrainingStatus.objects.all()
    # vacancies = Vacancy.objects.order_by('-created_at')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        status_id = request.POST.get('vacancy_status')
        image = request.FILES.get('image')

        user_ward = getattr(request.user, 'ward', None)

        if not all([title, description, deadline, status_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('create_vacancy')

        try:
            vacancy_status = TrainingStatus.objects.get(pk=status_id)

            Vacancy.objects.create(
                user=request.user,
                title=title,
                description=description,
                deadline=deadline,
                ward=user_ward,
                vacancy_status=vacancy_status,
                image=image
            )

            messages.success(request, 'Vacancy created successfully!')
            return redirect('create_vacancy')

        except TrainingStatus.DoesNotExist:
            messages.error(request, 'Invalid status selected. Please try again.')
            return redirect('create_vacancy')
    return render(request, 'notices/create_vacancy.html', {'statuses': statuses})

def vacancy_list(request):
    vacancies = Vacancy.objects.order_by('-created_at')  # latest first
    return render(request, 'notices/vacancy_list.html', {'vacancies': vacancies})




