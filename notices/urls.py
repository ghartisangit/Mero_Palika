from django.urls import path
from . import views

urlpatterns = [
    path('information/create/', views.create_information, name='create_information'),
    path('information/', views.list_information, name='list_information'),
    path('information/edit/<int:id>/', views.edit_information, name='edit_information'),
    path('information/delete/<int:id>/', views.delete_information, name='delete_information'),
    path('information/search/', views.my_search_information, name='my_search_information'),
    path('vacancy/create/', views.create_vacancy, name='create_vacancy'),
    path('notice/create/', views.create_notice, name='notice_creation'),
    path('noticess_create/',views.create_noticeyes, name='noticess_create'),
    path('vacancies/', views.vacancy_list, name='vacancy_list'),
]