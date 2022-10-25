from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import requests as req
from io import StringIO
from .models import Choice, Question
from django.template import loader
import statistics

import psycopg2

def question(request):
    question = Question.objects.get(pk=1)
    context = {'question':  question}
    return render(request, 'graph/question.html', context)
    
def results(request):
    question = Question.objects.get(pk=1)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    connection = psycopg2.connect("dbname=aq user=postgres")
    cursor = connection.cursor()
    selected_choice = str(selected_choice)
    def get_id(selected_choice):
        cursor.execute('''SELECT city_id FROM aq_meta WHERE city = (%s)''', (selected_choice,))
        records = cursor.fetchall()
        return(records)
    cityid = get_id(selected_choice)
    cityid = cityid[0]
    cityid = int(str(cityid).replace('(', '').replace(')','').replace(',',''))
    def get_pm25(cityid):
        cursor.execute('''SELECT pm2_5 FROM aq_data WHERE city_id = (%s)''', (cityid,))
        records = cursor.fetchall()
        return(records)
    pm25_list = get_pm25(cityid)
    pm25_nums = [x[0] for x in pm25_list]
    average = statistics.mean(pm25_nums)
    std = statistics.stdev(pm25_nums)
    
    context = {'pm25_list' : pm25_nums, 'average': average, 'std': std}
    return render(request, 'graph/results.html', context)