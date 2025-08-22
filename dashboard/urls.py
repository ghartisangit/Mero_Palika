from django.urls import path
from . import views


urlpatterns = [
   path('municipality_dashboard/', views.municipality_dashboard, name='municipality_dashboard'),
   path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
   path('user_details/',views.user_details, name='user_details'),
   path('category/dashboard/',views.dashboard_my_search_complaints, name='dashboard_my_search_complaints'),
   path('complaints/<int:id>/update-status/', views.update_complaint_status, name='update_complaint_status'),
   path('admin/category/', views.admin_search_complaints, name='admin_search_complaints'),
   path('admin/complaint/<int:pk>/delete/', views.admin_delete_complaint, name='admin_delete_complaint'),
   path('admin/comment/<int:comment_id>/delete/', views.admin_delete_comment, name='admin_delete_comment'),
   path('delete-user/<int:user_id>/',views.delete_user, name='delete_user'),
]