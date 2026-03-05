from django.urls import path
from . import views

urlpatterns=[
    path('hello/',views.hello,name="hello"),
    path('greet/<str:name>/',views.greet,name="greet"),
        path('tasks/', views.tasks_list, name='tasks'),
]