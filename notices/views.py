from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Information, Notice, Training, TrainingRegistration, TrainingStatus
from django.core.paginator import Paginator
from .models import Vacancy, VacancyRegistration
from django.db.models import Q

@login_required
def create_information(request):
    user = request.user
    if user.user_type not in ['municipality', 'admin']:
        messages.error(request, "You are not authorized to create information.")
        return redirect('list_information')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        ward = getattr(user, 'ward', None) 

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

   
    paginator = Paginator(informations, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'information/list_information.html', {
        'informations': page_obj
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

    informations = Information.objects.none()  

    if keyword:
       
        search_words = keyword.replace('_', ' ').split() 
        
        query = Q()
        for word in search_words:
            query |= Q(title__icontains=word)  

        if user.user_type == 'admin':
            informations = Information.objects.filter(query).order_by('-id')
        elif user.user_type == 'municipality':
            informations = Information.objects.filter(ward=user.ward).filter(query).order_by('-id')
        else:  # normal user
            informations = Information.objects.filter(ward=user.ward).filter(query).order_by('-id')
    else:
        # No category selected
        if user.user_type == 'admin':
            informations = Information.objects.all().order_by('-id')
        elif user.user_type == 'municipality':
            informations = Information.objects.filter(ward=user.ward).order_by('-id')
        else:
            informations = Information.objects.none()  
    
    paginator = Paginator(informations, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, 'information/list_information.html', { 'informations': page_obj})

@login_required
def create_notice(request):
    user = request.user
    if user.user_type not in ['municipality', 'admin']:
        messages.error(request, "You are not authorized to create notices.")
        return redirect('list_notice')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        ward = getattr(user, 'ward', None)

        if not title or not description:
            messages.error(request, "Please fill all fields.")
            return redirect('create_notice')

        Notice.objects.create(
            user=user,
            title=title,
            description=description,
            ward=ward
        )
        messages.success(request, "Notice uploaded successfully.")
        return redirect('list_notice')

    return render(request, 'notice/create_notice.html')


@login_required
def list_notice(request):
    user = request.user
    notices = Notice.objects.none()

    if user.user_type == 'admin':
        notices = Notice.objects.all().order_by('-id')
    elif user.user_type == 'municipality':
        notices = Notice.objects.filter(ward=user.ward).order_by('-id')
    else:
       
        notices = Notice.objects.filter(ward=user.ward).order_by('-id')

    
    paginator = Paginator(notices, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notice/list_notice.html', {
        'notices': page_obj
    })

# EDIT
@login_required
def edit_notice(request, id):
    notice = get_object_or_404(Notice, id=id)

 
    if request.user != notice.user and request.user.user_type != 'admin':
        messages.error(request, "You are not authorized to edit this notice.")
        return redirect('list_notice')

    if request.method == "POST":
        notice.title = request.POST.get('title', '').strip()
        notice.description = request.POST.get('description', '').strip()
        notice.save()
        messages.success(request, "Notice updated successfully.")
        return redirect('list_notice')

    return render(request, 'notice/edit_notice.html', {'notice': notice})

# DELETE
@login_required
def delete_notice(request, id):
    notice = get_object_or_404(Notice, id=id)

    if request.user.user_type not in ['municipality', 'admin']:
        messages.error(request, "You are not authorized to delete this notice.")
        return redirect('list_notice')

    notice.delete()
    messages.success(request, "Notice deleted successfully.")
    return redirect('list_notice')



@login_required
def create_vacancy(request):
    user = request.user
    if user.user_type != 'municipality':
        messages.error(request, "You are not authorized to create a vacancy.")
        return redirect('list_vacancy')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        ward = getattr(user, 'ward', None)

        if not title or not description:
            messages.error(request, "All fields are required.")
            return redirect('create_vacancy')

    
        available_status = TrainingStatus.objects.get(name='Available')
        vacancy = Vacancy.objects.create(
            user=user,
            title=title,
            description=description,
            ward=ward,
            vacancy_status=available_status
        )
        messages.success(request, "Vacancy created successfully.")
        return redirect('list_vacancy')

    return render(request, 'vacancy/create_vacancy.html')



@login_required
def edit_vacancy(request, id):
    vacancy = get_object_or_404(Vacancy, id=id)

    if request.user.user_type != 'municipality':
        messages.error(request, "You are not authorized to edit this vacancy.")
        return redirect('list_vacancy')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title and description:
            vacancy.title = title
            vacancy.description = description
            vacancy.save()
            messages.success(request, "Vacancy updated successfully.")
            return redirect('list_vacancy')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'vacancy/edit_vacancy.html', {'vacancy': vacancy})


@login_required
def delete_vacancy(request, id):
    vacancy = get_object_or_404(Vacancy, id=id)
    if request.user.user_type != 'municipality':
        messages.error(request, "You are not authorized to delete this vacancy.")
        return redirect('list_vacancy')

    if request.method == 'POST':
        vacancy.delete()
        messages.success(request, "Vacancy deleted successfully.")
        return redirect('list_vacancy')

    return redirect('list_vacancy')


@login_required
def list_vacancy(request):
    user = request.user
    vacancies = Vacancy.objects.filter(ward=user.ward).order_by('-created_at')

    
    for v in vacancies:
        if v.is_expired and v.vacancy_status != 'Expired':
            v.vacancy_status = 'Expired'
            v.save()

  
    paginator = Paginator(vacancies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Applicant count & user registration status
    for v in page_obj:
        v.applicant_count = v.vacancyregistrations.count()
        v.registered = v.vacancyregistrations.filter(user=request.user).exists()

    context = {
        'vacancies': page_obj,
        'statuses': TrainingStatus.objects.all(),
    }
    return render(request, 'vacancy/list_vacancy.html', context)



@login_required
def register_vacancy(request, id):
    vacancy = get_object_or_404(Vacancy, id=id)
    user = request.user

    if user.user_type != 'user':
        messages.error(request, "Only normal users can register for a vacancy.")
        return redirect('list_vacancy')

    if VacancyRegistration.objects.filter(user=user, Vacancy=vacancy).exists():
        messages.info(request, "You have already registered for this vacancy.")
    else:
        VacancyRegistration.objects.create(user=user, Vacancy=vacancy)
        messages.success(request, "Successfully registered for the vacancy. You will be contacted if selected.")

    return redirect('list_vacancy')

@login_required
def update_vacancy_status(request, vacancy_id):

    if request.user.user_type != 'municipality':
        messages.error(request, "You are not authorized to change status.")
        return redirect('list_vacancy')

    if request.method == 'POST':
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        status_id = request.POST.get('status')
        status = get_object_or_404(TrainingStatus, id=status_id)
        vacancy.vacancy_status = status
        vacancy.save()  
        messages.success(request, f"Vacancy status updated to {status.name}.")

    return redirect('list_vacancy')



@login_required
def list_training(request):
    user = request.user
    trainings = Training.objects.filter(ward=user.ward).order_by('-created_at')

    for t in trainings:
        if t.is_expired and t.training_status.name != 'Expired':
            expired_status = TrainingStatus.objects.get(name='Expired')
            t.training_status = expired_status
            t.save()

    # Pagination
    paginator = Paginator(trainings, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    for t in page_obj:
        t.applicant_count = t.trainingregistrations.count()  # You need TrainingRegistration model
        t.registered = t.trainingregistrations.filter(user=user).exists()

    context = {
        'trainings': page_obj,
        'statuses': TrainingStatus.objects.all() if user.user_type == 'municipality' else None,
    }
    return render(request, 'training/list_training.html', context)


@login_required
def create_training(request):
    user = request.user
    
    if user.user_type != 'municipality':
        messages.error(request, "You are not authorized to create a training.")
        return redirect('list_training')

   
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        expiry_date = request.POST.get('expiry_date')
        image = request.FILES.get('image')
        ward = getattr(user, 'ward', None)
        default_status = TrainingStatus.objects.get(name='Available')

        if not title or not description:
            messages.error(request, "Title and description are required.")
            return redirect('create_training')

        Training.objects.create(
            user=user,
            title=title,
            description=description,
            ward=ward,
            training_status=default_status,
            expiry_date=expiry_date or None,
            image=image
        )
        messages.success(request, "Training created successfully.")
        return redirect('list_training')

    return render(request, 'training/create_training.html')


@login_required
def edit_training(request, id):
    training = get_object_or_404(Training, id=id)

    if request.user.user_type != 'municipality':
        messages.error(request, "You are not authorized to edit this training.")
        return redirect('list_training')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        expiry_date = request.POST.get('expiry_date')
        image = request.FILES.get('image')

        if title and description:
            training.title = title
            training.description = description
            training.expiry_date = expiry_date
            if image:
                training.image = image
            training.save()
            messages.success(request, "Training updated successfully.")
            return redirect('list_training')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'training/edit_training.html', {'training': training})


@login_required
def delete_training(request, id):
    training = get_object_or_404(Training, id=id)

    if request.user.user_type != 'municipality':
        messages.error(request, "You are not authorized to delete this training.")
        return redirect('list_training')

    if request.method == 'POST':
        training.delete()
        messages.success(request, "Training deleted successfully.")
        return redirect('list_training')

    return render(request, 'list_training')

@login_required
def register_training(request, id):
    training = get_object_or_404(Training, id=id)
    user = request.user

    if user.user_type != 'user':
        messages.error(request, "Only normal users can register for a training.")
        return redirect('list_training')

    if training.training_status.name != 'Available':
        messages.error(request, "Registration closed for this training.")
        return redirect('list_training')

    if TrainingRegistration.objects.filter(user=user, training=training).exists():
        messages.info(request, "You have already registered for this training.")
    else:
        TrainingRegistration.objects.create(user=user, training=training)
        messages.success(request, "Successfully registered for the training.")

    return redirect('list_training')


@login_required
def update_training_status(request, id):
    training = get_object_or_404(Training, id=id)

    if request.user.user_type != 'municipality':
        messages.error(request, "You are not authorized to change status.")
        return redirect('list_training')

    if request.method == 'POST':
        status_id = request.POST.get('status')
        if status_id:
            training.training_status_id = status_id
            training.save()
            messages.success(request, "Training status updated successfully.")
        return redirect('list_training')