from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Complaint, Ward, Category, Status ,Like, Comment
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q

User = get_user_model()

@login_required(login_url='login')
def post_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category_name = request.POST.get('category', '').strip()
        image = request.FILES.get('image')

  
        if not all([title, description, category_name]):
            messages.error(request, "Please fill all required fields.")
            return redirect('post_complaint')

     
        ward = request.user.ward 
        if not ward:
            messages.error(request, "Your profile does not have a ward assigned.")
            return redirect('post_complaint')

        try:
            category = Category.objects.get(category_name=category_name)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect('post_complaint')

        status = Status.objects.filter(name='Pending').first()
        if not status:
            messages.error(request, "Default status not set in database.")
            return redirect('post_complaint')

        Complaint.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            ward=ward, 
            status=status,
            image=image
        )

        messages.success(request, "Complaint submitted successfully.")
        return redirect('my_complaints')

    categories = Category.objects.all()
    return render(request, 'complaints/create_complaint.html', {'categories': categories})



@login_required(login_url='login')
def all_complaint(request):
    user = request.user
    if user.is_authenticated :
        complaints_list = Complaint.objects.filter(ward=user.ward, ).order_by('-created_at')
    else:
        complaints_list = Complaint.objects.none()  
    

    paginator = Paginator(complaints_list, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = paginator.count  

    context = {
        'complaints': page_obj, 
        'wards': Ward.objects.all(),  
        'statuses': Status.objects.all(),
        'links': Category.objects.all(),
        'post_count': post_count
    }

    return render(request, 'complaints/all_complaints.html', context)

@login_required(login_url='login')
def post_detail(request, id):
    user = request.user
    
    if user.is_authenticated and user.user_type == 'admin':
        
        complaint = get_object_or_404(Complaint, id=id)
    else:
        complaint = get_object_or_404(Complaint, id=id, is_hidden=False)

    statuses = Status.objects.all()   
    return render(request, 'complaints/post_detail.html', {'complaint': complaint, 'statuses': statuses})


@login_required(login_url='login')
def my_profile(request):
    user = request.user
    post_count = Complaint.objects.filter(user=user).count()
    total_count = Complaint.objects.filter(ward=user.ward ,is_hidden=False).count()
     
    
    context = {
        'profile': user,
        'post_count': post_count,
        'total_count':total_count
    }
    return render(request, 'accounts/my_profile.html', context)


@login_required(login_url='login')
def my_complaints(request):
    complaints_list = Complaint.objects.filter(user=request.user).order_by('-created_at') 
    paginator = Paginator(complaints_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count= paginator.count 
    
    context = {
        'complaints': page_obj, 
        'wards': Ward.objects.all(),
        'statuses': Status.objects.all(),
        'links': Category.objects.all(),
        'post_count': post_count
    }
    return render(request, 'complaints/my_complaints.html', context)



@login_required(login_url='login')
def like_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    if request.user == complaint.user:
        messages.error(request, "You cannot like your own post.")
    else:
        like_obj = Like.objects.filter(user=request.user, complaint=complaint).first()
        if like_obj:
            like_obj.delete()
            messages.success(request, "You unliked the post.")
        else:
            Like.objects.create(user=request.user, complaint=complaint)
            messages.success(request, "You liked the post.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def comment_complaint(request, pk):
    
    complaint = get_object_or_404(Complaint, pk=pk)

    if request.user == complaint.user:
        messages.error(request, "You cannot comment on your own post.")
        return redirect('post_detail', id=pk)

    if Comment.objects.filter(user=request.user, complaint=complaint).exists():
        messages.info(request, "You have already commented on this post.")
        return redirect('post_detail', id=pk)  # Important: redirect here to avoid adding duplicate comment

    if request.method == "POST":
        content = request.POST.get('comment', '').strip()
        if content:
            Comment.objects.create(user=request.user, complaint=complaint, content=content)
            messages.success(request, "You commented on the post.")
        else:
            messages.warning(request, "Comment cannot be empty.")

    return redirect('post_detail', id=pk)


@login_required(login_url='login')
def search_complaints(request):
    keyword = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    status = request.GET.get('status')
    complaints = Complaint.objects.filter(
        ward=request.user.ward,
        is_hidden=False
    ).order_by('-created_at')

    # Apply filters
    if keyword:
        complaints = complaints.filter(
            Q(title__icontains=keyword) | Q(description__icontains=keyword)
        )

    if category:
        complaints = complaints.filter(category__id=category)

    if status:
        complaints = complaints.filter(status=status)

    post_count = complaints.count()

    context = {
        'complaints': complaints,
        'post_count': post_count,
        'links': Category.objects.all(),
        'wards': Ward.objects.filter(id=request.user.ward.id),
        'statuses': Status.objects.all(),
    }

    return render(request, 'complaints/all_complaints.html', context)



@login_required(login_url='login')
def my_search_complaints(request):

    keyword = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    municipality = request.GET.get('municipality')
    status = request.GET.get('status')
    ward_number = request.GET.get('ward_number')

    complaints=Complaint.objects.filter(user=request.user).order_by('-created_at') 
    

    if keyword:
        complaints = complaints.filter(title__icontains=keyword)

    if category:
        complaints = complaints.filter(category__id=category)
        
    if municipality and ward_number:
        complaints = complaints.filter(ward__ward_number=ward_number, ward__municipality_id=municipality)

    if status:
        complaints = complaints.filter(status=status)

    post_count = complaints.count()

    context = {
        'complaints': complaints,
        'post_count': post_count,
        'links': Category.objects.all(),
        'wards': Ward.objects.all(),
        'statuses': Status.objects.all(),
    }

    return render(request, 'complaints/my_complaints.html', context)

@login_required
def delete_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    if complaint.user != request.user:
        messages.error(request, "You are not allowed to delete this complaint.")
        return redirect(request.META.get('HTTP_REFERER', 'my_complaints'))  

    complaint.delete()
    messages.success(request, "Complaint deleted successfully.")
    return redirect('my_complaints') 


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    complaint = comment.complaint

    if request.user == comment.user or request.user == complaint.user:
        if request.method == 'POST':
            comment.delete()
            messages.success(request, "Comment deleted successfully.")
            return redirect('post_detail', complaint.id)
    else:
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('post_detail', complaint.id)

    return redirect('post_detail', complaint.id)


@login_required
def edit_complaint(request, complaint_id):
   
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    
    
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category_id = request.POST.get('category')
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')

        if not title or not description or not category_id:
            messages.error(request, "Please fill all required fields.")
            return redirect('edit_complaint', complaint_id=complaint.id)

        
        complaint.title = title
        complaint.description = description
        complaint.category = Category.objects.get(id=category_id)

        ward = request.user.ward 
        if not ward:
            messages.error(request, "Your complaint does not have a ward assigned.")
            return redirect('my_complaint')


        complaint.ward = ward
        complaint.municipality = ward.municipality

       
        if image:
            complaint.image = image

        complaint.save()
        messages.success(request, "Complaint updated successfully.")
        return redirect('my_complaints')

    context = {
        'complaint': complaint,
        'categories': categories,
        
    }
    return render(request, 'complaints/edit_complaint.html', context)

@login_required(login_url='login')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect('post_detail', id=comment.complaint.id)

    if request.method == 'POST':
        content = request.POST.get('comment', '').strip()
        if content:
            comment.content = content
            comment.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('post_detail', id=comment.complaint.id)

    return render(request, 'complaints/edit_comment.html', {'comment': comment, 'complaint': comment.complaint})
