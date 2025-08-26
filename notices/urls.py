from django.urls import path
from . import views

urlpatterns = [
    path('information/create/', views.create_information, name='create_information'),
    path('information/', views.list_information, name='list_information'),
    path('information/edit/<int:id>/', views.edit_information, name='edit_information'),
    path('information/delete/<int:id>/', views.delete_information, name='delete_information'),
    path('information/search/', views.my_search_information, name='my_search_information'),
    # Notices
    path('notice/create/', views.create_notice, name='create_notice'),
    path('notice/', views.list_notice, name='list_notice'),
    path('notice/edit/<int:id>/', views.edit_notice, name='edit_notice'),
    path('notice/delete/<int:id>/', views.delete_notice, name='delete_notice'),
    
    # Vacancy URLs
    path('vacancies/', views.list_vacancy, name='list_vacancy'),
    path('vacancy/create/', views.create_vacancy, name='create_vacancy'),
    path('vacancy/<int:id>/edit/', views.edit_vacancy, name='edit_vacancy'),
    path('vacancy/<int:id>/delete/', views.delete_vacancy, name='delete_vacancy'),
    path('vacancy/<int:id>/register/', views.register_vacancy, name='register_vacancy'),
    path('vacancy/<int:vacancy_id>/update-status/', views.update_vacancy_status, name='update_vacancy_status'),
    
    path('training/', views.list_training, name='list_training'),
    path('training/create/', views.create_training, name='create_training'),
    path('training/<int:id>/edit/', views.edit_training, name='edit_training'),
    path('training/<int:id>/delete/', views.delete_training, name='delete_training'),
    path('training/<int:id>/register/', views.register_training, name='register_training'),
    path('training/<int:id>/update_status/', views.update_training_status, name='update_training_status'),
]