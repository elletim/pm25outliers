from django.urls import path
from . import views

urlpatterns = [
    path('', views.initial, name='initial'),
    path('hour/', views.question, name='question'),
    path('hour/results/', views.results, name='results'),
    path('month/', views.question2, name='question2'),
    path('month/results/', views.results2, name='results2'),
    path('day/', views.question3, name='question3'),
    path('day/results/', views.results3, name='results3'),  
]