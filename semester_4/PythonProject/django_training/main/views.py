from django.http import HttpResponse
from django.shortcuts import render
from .models import Task

def hello(request):
    return HttpResponse("Hello ,world")

def greet(request, name):
    context={
        'name':name
    }
    return render(request,'greet.html',context)

def tasks_list(request):
    tasks = Task.objects.all()  # получаем ВСЕ задачи из БД
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks_list.html', context)