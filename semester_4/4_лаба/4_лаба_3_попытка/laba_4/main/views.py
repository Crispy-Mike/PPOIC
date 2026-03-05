# main/views.py
from django.shortcuts import render
from django.http import HttpResponse  # для простого ответа

def home(request):
    return render(request, 'templates/main/main.html')

def about(request):
    return render(request, 'main/about.html')  # если есть шаблон
    # или просто текст:
    # return HttpResponse("Страница О нас")

def services(request):
    return render(request, 'main/services.html')
    # или: return HttpResponse("Страница Услуги")

def contacts(request):
    return render(request, 'main/contacts.html')
    # или: return HttpResponse("Страница Контакты")