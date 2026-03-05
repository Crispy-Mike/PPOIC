# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    # если нужны другие страницы:
    path('about/', views.about, name='about'),      # создайте потом
    path('services/', views.services, name='services'),
    path('contacts/', views.contacts, name='contacts'),
]