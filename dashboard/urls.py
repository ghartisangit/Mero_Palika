from django.urls import path
from . import views


urlpatterns = [
   path('municipality_dashboard/', views.municipality_dashboard, name='municipality_dashboard'),
   path('category/dashboard/',views.dashboard_my_search_complaints, name='dashboard_my_search_complaints'),
   path('complaints/<int:id>/update-status/', views.update_complaint_status, name='update_complaint_status'),
   path('admin/complaint/<int:pk>/delete/', views.admin_delete_complaint, name='admin_delete_complaint'),
   path('admin/comment/<int:comment_id>/delete/', views.admin_delete_comment, name='admin_delete_comment'),
]