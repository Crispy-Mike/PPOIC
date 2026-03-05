# laba_4/urls.py
from django.contrib import admin
from django.urls import path, include  # добавьте include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # добавляем все URL из приложения main
]