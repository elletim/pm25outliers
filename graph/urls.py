from django.urls import path
from . import views

urlpatterns = [
    path('hour/', views.question, name='question'),
    path('results/', views.results, name='results'),
    path('month/', views.question2, name='question2'),
     path('day/', views.question3, name='question3')

    
]