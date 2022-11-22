from django.shortcuts import render
from .models import Choice, Question
import statistics
import psycopg2
import config 
import pandas as pd
import json 
import numpy as np


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
    context = {'pm25_list' : pm25_nums, 'datetime_list': json.dumps(datetime_nums), 'average': averagevar, 'std': std,
    'plusstdv2' : stdv2, 'minusstdv2' : stdv_2, 'plusstdv3' : stdv3, 'minusstdv3' : stdv_3, 
    'city': selected_choice, 'minpm25': minpm25, 'maxpm25': maxpm25, 'merge': json.dumps(merge), 'startvalue': json.dumps(startvalue)}
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
    
    #graph 2
    login = config.postgres["login"]
    connection = psycopg2.connect(login)
    cursor = connection.cursor()
    cursor.execute('''SELECT city FROM aq_meta''')
    citynames = cursor.fetchall()
    citynames = [i[0] for i in citynames]
    print(citynames[1])
    df = get_df(0)
    pm25 = df['pm25'].to_list()
    df1= get_df(1)
    pm25_1 = df1['pm25'].to_list()
    pm25_1 = get_fill(pm25, pm25_1)
    df2= get_df(2)
    pm25_2 = df2['pm25'].to_list()
    pm25_2 = get_fill(pm25, pm25_2)
    df3= get_df(3)
    pm25_3 = df3['pm25'].to_list()
    pm25_3 = get_fill(pm25, pm25_3)
    df4= get_df(4)
    pm25_4 = df4['pm25'].to_list()
    pm25_4 = get_fill(pm25, pm25_4)
    df5= get_df(5)
    pm25_5 = df5['pm25'].to_list()
    pm25_5 = get_fill(pm25, pm25_5)
    df6= get_df(1)
    pm25_6 = df6['pm25'].to_list()
    pm25_6 = get_fill(pm25, pm25_6)
    df7= get_df(7)
    pm25_7 = df7['pm25'].to_list()
    pm25_7 = get_fill(pm25, pm25_7)
    df8= get_df(8)
    pm25_8 = df8['pm25'].to_list()
    pm25_8 = get_fill(pm25, pm25_8)
    df9= get_df(9)
    pm25_9 = df9['pm25'].to_list()
    pm25_9 = get_fill(pm25, pm25_9)
    df10= get_df(10)
    pm25_10 = df10['pm25'].to_list()
    pm25_10 = get_fill(pm25, pm25_10)
    df11= get_df(11)
    pm25_11 = df11['pm25'].to_list()
    pm25_11 = get_fill(pm25, pm25_11)
    df12= get_df(12)
    pm25_12 = df12['pm25'].to_list()
    pm25_12 = get_fill(pm25, pm25_12)
    df13= get_df(13)
    pm25_13 = df13['pm25'].to_list()
    pm25_13 = get_fill(pm25, pm25_13)
    x = list(df.index.values)
    year1 = [i[0] for i in x]
    month1 = [i[1] for i in x]
    datetime= [str(i) for i in zip(year1, month1)]
    datetime = [i.replace(',','/').replace(' ','').replace('(','').replace(')','') for i in datetime]

    context = {'pm25_list' : pm25_nums, 'datetime_list': json.dumps(datetime_nums), 'average': averagevar, 'std': std,
    'plusstdv1' : stdv1, 'minusstdv1' : stdv_1, 'pm25' : pm25, 
    'pm25_1': json.dumps(pm25_1), 'pm25_2': json.dumps(pm25_2), 'pm25_3': json.dumps(pm25_3), 'pm25_4': json.dumps(pm25_4), 
    'pm25_5': json.dumps(pm25_5), 'pm25_6': json.dumps(pm25_6), 'pm25_7': json.dumps(pm25_7), 'pm25_8': json.dumps(pm25_8),
    'pm25_9': json.dumps(pm25_9), 'pm25_10': json.dumps(pm25_10), 'pm25_11': json.dumps(pm25_11), 'pm25_12': json.dumps(pm25_12),
    'pm25_12': json.dumps(pm25_12), 'pm25_13': json.dumps(pm25_13), 'datetime' : json.dumps(datetime), 'citynames': json.dumps(citynames),
    'city': selected_choice, 'minpm25': minpm25, 'maxpm25': maxpm25, 'startvalue': startvalue}
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

    context = {'pm25_list' : pm25_nums, 'datetime_list': json.dumps(datetime_nums), 'average': averagevar,
    'plusstdv1' : stdv1, 'minusstdv1' : stdv_1, 'pm25': pm25, 'city': selected_choice, 
    'minpm25': minpm25, 'maxpm25': maxpm25, 'startvalue': startvalue, 'days': json.dumps(days)}
    return render(request, 'graph/results3.html', context)


