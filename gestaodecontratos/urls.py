from django.contrib import admin
from django.urls import path, include
from .views import teste

urlpatterns = [
    path('gestaodecontratos/', teste, name='teste'),
]