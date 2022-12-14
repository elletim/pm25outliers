from django.shortcuts import render, redirect
from .models import Choice, Question
import statistics
import psycopg2
import config 
import pandas as pd
import json 
import numpy as np

def initial(request):
    context = {'a': 2}
    return render(request,'graph/initial.html', context)

def question(request):
    login = config.postgres["login"]
    connection = psycopg2.connect(login)
    cursor = connection.cursor()
    cursor.execute('''SELECT lat, long FROM aq_meta''')
    records = cursor.fetchall()
    records = [list(x) for x in records]
    question = Question.objects.get(pk=1)
    context = {'question':  question, 'records': records}
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
    return(records)

def get_pm25(cityid):
    login = config.postgres["login"]
    connection = psycopg2.connect(login)
    cursor = connection.cursor()
    cursor.execute('''SELECT pm2_5, datetime FROM aq_data WHERE city_id = (%s) order by datetime''', (cityid,))
    records = cursor.fetchall()
    return(records) 

def get_df(cityid):
    login = config.postgres["login"]
    connection = psycopg2.connect(login)
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM aq_data WHERE city_id = (%s)''', (cityid,))
    records = cursor.fetchall()
    datetime = [x[1] for x in records]
    pm25 = [x[2] for x in records]
    df1 = pd.DataFrame({'pm25': pm25, 'date': datetime})
    df1['date']= pd.to_datetime(df1['date'])
    df1 = df1.groupby([df1['date'].dt.year, df1['date'].dt.month]).agg({'pm25':'mean'})
    return(df1)

def get_fill(pm25, pm):
    diff = len(pm25)-len(pm)
    fill = [None] * diff
    pm = fill + pm
    return(pm)

def results(request):
    #hour
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
    datetime_nums = [date_obj.strftime('%Y/%m/%d/%H') for date_obj in datetime_nums]
    startvalue = datetime_nums[0]
    merge = [list(i) for i in zip(datetime_nums, pm25_nums)]

    #report data: hourly average
    pm25 = [x[0] for x in pm25_list]
    dates = [x[1] for x in pm25_list]
    df_dates = pd.DataFrame({'pm25': pm25, 'dates': dates})
    df_dates['dates']= pd.to_datetime(df_dates['dates'])
    df_dates = df_dates.groupby([ df_dates['dates'].dt.hour]).agg({'pm25':'mean'})
    pm25 = df_dates['pm25'].to_list()
    pm25 = [round(i,2) for i in pm25]
    avg_hour = statistics.mean(pm25)
    hours = list(range(24))
    

    context = {'pm25_list' : pm25_nums, 'datetime_list': json.dumps(datetime_nums), 'average': averagevar, 'std': std,
    'plusstdv2' : stdv2, 'minusstdv2' : stdv_2, 'plusstdv3' : stdv3, 'minusstdv3' : stdv_3, 
    'city': selected_choice, 'minpm25': minpm25, 'maxpm25': maxpm25, 'merge': json.dumps(merge), 'startvalue': json.dumps(startvalue),
    'pm25': pm25, 'hours': hours, 'avg_hour': avg_hour}
    return render(request, 'graph/results.html', context)

def results2(request):
    #month
    question = Question.objects.get(pk=1)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    selected_choice = str(selected_choice)
    cityid = get_id(selected_choice)
    cityid = cityid[0]
    cityid = int(str(cityid).replace('(', '').replace(')','').replace(',',''))
    pm25_list = get_pm25(cityid)
    pm25_nums = [x[0] for x in pm25_list]
    datetime_nums = [x[1] for x in pm25_list]
    df = pd.DataFrame({'pm25': pm25_nums, 'date': datetime_nums})
    df['date']= pd.to_datetime(df['date'])
    df = df.groupby([df['date'].dt.year, df['date'].dt.month]).agg({'pm25':'mean'})
    pm25_nums = df['pm25'].to_list()
    x = list(df.index.values)
    year = [i[0] for i in x]
    month = [i[1] for i in x]
    datetime_nums = [str(i) for i in zip(year, month)]
    datetime_nums = [i.replace(',','/').replace(' ','').replace('(','').replace(')','') for i in datetime_nums]   
    average = statistics.mean(pm25_nums)
    averagevar = [average] * len(pm25_nums)
    std = statistics.stdev(pm25_nums)
    stdv1 = [average + (std)] * len(pm25_nums)
    stdv_1 = [average - (std)] * len(pm25_nums)
    minpm25 = min(pm25_nums)
    maxpm25 = max(pm25_nums)
    startvalue = datetime_nums[0]

    #montly average
    pm25 = [x[0] for x in pm25_list]
    dates = [x[1] for x in pm25_list]
    df_dates = pd.DataFrame({'pm25': pm25, 'dates': dates})
    df_dates['dates']= pd.to_datetime(df_dates['dates'])
    df_dates = df_dates.groupby([df_dates['dates'].dt.month, df_dates['dates'].dt.month]).agg({'pm25':'mean'})
    pm25 = df_dates['pm25'].to_list()

    #report data: monthly average
    #print(pm25)

    context = {'pm25_list' : pm25_nums, 'datetime_list': json.dumps(datetime_nums), 'average': averagevar, 'std': std,
    'plusstdv1' : stdv1, 'minusstdv1' : stdv_1,  'city': selected_choice, 'minpm25': minpm25, 'maxpm25': maxpm25, 'startvalue': startvalue}
    return render(request, 'graph/results2.html', context)

def results3(request):
    #day
    question = Question.objects.get(pk=1)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    selected_choice = str(selected_choice)
    cityid = get_id(selected_choice)
    cityid = cityid[0]
    cityid = int(str(cityid).replace('(', '').replace(')','').replace(',',''))
    pm25_list = get_pm25(cityid)
    pm25_nums = [x[0] for x in pm25_list]
    datetime_nums = [x[1] for x in pm25_list]
    df = pd.DataFrame({'pm25': pm25_nums, 'date': datetime_nums})
    df['date']= pd.to_datetime(df['date'])
    df = df.groupby([df['date'].dt.year, df['date'].dt.month, df['date'].dt.day]).agg({'pm25':'mean'})
    pm25_nums = df['pm25'].to_list()
    x = list(df.index.values)
    year = [i[0] for i in x]
    month = [i[1] for i in x]
    day = [i[2] for i in x]
    datetime_nums = [str(i) for i in zip(year, month, day)]
    datetime_nums = [i.replace(',','/').replace(' ','').replace('(','').replace(')','') for i in datetime_nums]  
    average = statistics.mean(pm25_nums)
    averagevar = [average] * len(pm25_nums)
    std = statistics.stdev(pm25_nums)
    stdv1 = [average + (std)] * len(pm25_nums)
    stdv_1 = [average - (std)] * len(pm25_nums)
    minpm25 = min(pm25_nums)
    maxpm25 = max(pm25_nums)
    startvalue = datetime_nums[0]
    
    #graph 2
    days = pd.date_range('2015-01-01', '2015-12-31').strftime('%m/%d')
    days = [str(x) for x in days]
    pm25 = [x[0] for x in pm25_list]
    dates = [x[1] for x in pm25_list]
    df_dates = pd.DataFrame({'pm25': pm25, 'dates': dates})
    df_dates['dates']= pd.to_datetime(df_dates['dates'])
    df_dates = df_dates.groupby([df_dates['dates'].dt.month, df_dates['dates'].dt.day]).agg({'pm25':'mean'})
    pm25 = df_dates['pm25'].to_list()

    #report data: daily numbers
    max_avg = max(pm25)
    min_avg = min(pm25)
    mean_avg = statistics.mean(pm25)
    median_avg = statistics.median(pm25)
    percentile_25 = np.percentile(pm25, 25)
    percentile_75 = np.percentile(pm25, 75)
    #print(max_avg, min_avg, mean_avg, median_avg, percentile_25, percentile_75)

    context = {'pm25_list' : pm25_nums, 'datetime_list': json.dumps(datetime_nums), 'average': averagevar,
    'plusstdv1' : stdv1, 'minusstdv1' : stdv_1, 'pm25': pm25, 'city': selected_choice, 
    'minpm25': minpm25, 'maxpm25': maxpm25, 'startvalue': startvalue, 'days': json.dumps(days)}
    return render(request, 'graph/results3.html', context)


def allcities(request):
    login = config.postgres["login"]
    connection = psycopg2.connect(login)
    cursor = connection.cursor()
    cursor.execute('''SELECT city FROM aq_meta''')
    citynames = cursor.fetchall()
    citynames = [i[0] for i in citynames]
    df = get_df(0)
    pm25 = df['pm25'].to_list()
   
    x = list(df.index.values)
    year1 = [i[0] for i in x]
    month1 = [i[1] for i in x]
    datetime= [str(i) for i in zip(year1, month1)]
    datetime = [i.replace(',','/').replace(' ','').replace('(','').replace(')','') for i in datetime]

    dataArray = []
    for indx, val in enumerate(citynames):
        pm25_i = get_df(indx)['pm25'].to_list()
        pm25_i = get_fill(pm25, pm25_i)
        d = { 'name': val, 'type': 'line', 'data': pm25_i}
        dataArray.append(d)

    context = {'datetime' : json.dumps(datetime),'dataArray': json.dumps(dataArray)}
    return render(request, 'graph/allcities.html', context)



