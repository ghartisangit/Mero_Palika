from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from django.contrib import messages
from complaints.models import Comment, Complaint, Ward, Category, Status, Municipality 
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q



User = get_user_model()

@login_required(login_url='login')
def municipality_dashboard(request):
    user = request.user
    if user.is_authenticated and user.user_type == 'municipality':
        
        complaints_list = Complaint.objects.filter(
            ward__municipality=user.ward.municipality, 
            is_hidden=False
        ).order_by('-created_at')
        
        total_count = complaints_list.count()
        
   
        pending_count = complaints_list.filter(status__name='Pending').count()
        in_progress_count = complaints_list.filter(status__name='In Progress').count()
        resolved_count = complaints_list.filter(status__name='Resolved').count()

        paginator = Paginator(complaints_list, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        post_count = paginator.count 
        
        context = {
            'complaints': page_obj, 
            'wards': Ward.objects.filter(municipality=user.ward.municipality),
            'statuses': Status.objects.all(),
            'links': Category.objects.all(),
            'total_count': total_count,
            'post_count': post_count,
            'pending_count': pending_count,
            'in_progress_count': in_progress_count,
            'resolved_count': resolved_count,
        }
        return render(request, 'dashboard/municipality_dashboard.html', context)
    
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('login')

@login_required(login_url='login')
def dashboard_my_search_complaints(request):
    keyword = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    status = request.GET.get('status')
    
    user = request.user
    if user.is_authenticated and user.user_type == 'municipality':
        complaints = Complaint.objects.filter(ward=request.user.ward).order_by('-created_at')
        
        total_count = complaints.count()
        

        pending_count = complaints.filter(status__name='Pending').count()
        in_progress_count = complaints.filter(status__name='In Progress').count()
        resolved_count = complaints.filter(status__name='Resolved').count()

        # Filters
        if keyword:
            complaints = complaints.filter(title__icontains=keyword)

        if category:
            complaints = complaints.filter(category_id=category)

        if status:
            complaints = complaints.filter(status_id=status)

        post_count = complaints.count()

        context = {
            'complaints': complaints,
            'total_count': total_count,
            'post_count': post_count,
            'links': Category.objects.all(),
            'statuses': Status.objects.all(),
            'pending_count': pending_count,
            'in_progress_count': in_progress_count,
            'resolved_count': resolved_count,
        }
        return render(request, 'dashboard/municipality_dashboard.html', context)

    messages.error(request, "You are not authorized.")
    return redirect('login')

@login_required
def update_complaint_status(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    
    if request.method == "POST":
        status_id = request.POST.get("status")
        if status_id:
            try:
                status_obj = Status.objects.get(id=status_id)
                complaint.status = status_obj
                complaint.save()
                messages.success(request, "Complaint status updated successfully.")
            except Status.DoesNotExist:
                messages.error(request, "Invalid status selected.")
        else:
            messages.error(request, "Please select a status.")

    return redirect('post_detail', id=id)




@login_required
def admin_delete_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    if not request.user.is_authenticated or request.user.user_type != 'admin':
        messages.error(request, "You are not allowed to delete this complaint.")
        return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))

    if request.method == 'POST':
        complaint.delete()
        messages.success(request, "Complaint deleted successfully.")
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')


@login_required
def admin_delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    complaint = comment.complaint

    if not request.user.is_authenticated or request.user.user_type != 'admin':
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('post_detail', complaint.id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('post_detail', complaint.id)

    return redirect('post_detail', complaint.id)



    



