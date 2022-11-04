from django.shortcuts import render
from .models import Choice, Question
import statistics
import psycopg2
import config 

def question(request):
    question = Question.objects.get(pk=1)
    context = {'question':  question}
    return render(request, 'graph/question.html', context)

def question2(request):
    question = Question.objects.get(pk=1)
    context = {'question':  question}
    return render(request, 'graph/question2.html', context)

def question3(request):
    question = Question.objects.get(pk=1)
    context = {'question':  question}
    return render(request, 'graph/question3.html', context)

def get_id(selected_choice):
        login = config.postgres["login"]
        connection = psycopg2.connect(login)
        cursor = connection.cursor()
        cursor.execute('''SELECT city_id FROM aq_meta WHERE city = (%s)''', (selected_choice,))
        records = cursor.fetchall()
        return records

def get_pm25(cityid):
        login = config.postgres["login"]
        connection = psycopg2.connect(login)
        cursor = connection.cursor()
        cursor.execute('''SELECT pm2_5, datetime FROM aq_data WHERE city_id = (%s) order by datetime''', (cityid,))
        records = cursor.fetchall()
        return records 

def results(request):
    question = Question.objects.get(pk=1)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    selected_choice = str(selected_choice)
    cityid = get_id(selected_choice)
    cityid = cityid[0]
    cityid = int(str(cityid).replace('(', '').replace(')','').replace(',',''))
    pm25_list = get_pm25(cityid)
    pm25_nums = [x[0] for x in pm25_list]
    datetime_nums = [x[1] for x in pm25_list]
    average = statistics.mean(pm25_nums)
    averagevar = [average] * len(pm25_nums)
    std = statistics.stdev(pm25_nums)
    stdv2 = [average + (2*std)] * len(pm25_nums)
    stdv_2 = [average - (2*std)] * len(pm25_nums)
    stdv3 = [average + (3*std)] * len(pm25_nums)
    stdv_3 = [average - (3*std)] * len(pm25_nums)
    minpm25 = min(pm25_nums)
    maxpm25 = max(pm25_nums)
    datetime_nums = [date_obj.strftime('%Y%m%d%H') for date_obj in datetime_nums]
    datetime_nums = [int(x) for x in datetime_nums]
    startvalue = datetime_nums[0]
    merge = [list(i) for i in zip(datetime_nums, pm25_nums)]
    context = {'pm25_list' : pm25_nums, 'datetime_list': datetime_nums, 'average': averagevar, 'std': std,
    'plusstdv2' : stdv2, 'minusstdv2' : stdv_2, 'plusstdv3' : stdv3, 'minusstdv3' : stdv_3, 
    'city': selected_choice, 'minpm25': minpm25, 'maxpm25': maxpm25, 'merge': merge, 'startvalue': startvalue}
    return render(request, 'graph/results.html', context)


