#!/usr/bin/python3
import pandas
import glob
import os
from datetime import datetime

def dateFunc(date_str, format=0):
    dateformats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%y %H:%M", "%m/%d/%Y %H:%M"]
    try:
        return datetime.strptime(date_str, dateformats[format])
    except:
        return dateFunc(date_str, format+1)

def toTimestamp(x):
    try:
        return datetime.timestamp(x)
    except TypeError:
        return 0

def getDataForContry(country):
    cwd = os.getcwd()
    all_files = glob.glob(cwd + "/csse_covid_19_data/csse_covid_19_daily_reports/*.csv")
    li = []

    for filename in all_files:
        df = pandas.read_csv(filename, index_col=None, header=0)
        df = df.rename(columns={'Country/Region': 'Country_Region', 'Last Update': 'Last_Update'})
        df = df.loc[df['Country_Region'] == country].filter(["Country_Region", "Last_Update", "Confirmed", "Deaths", "Recovered", "Active"])
        li.append(df)

    data = pandas.concat(li, axis=0, ignore_index=True, sort=False)

    return data

def addTimeStampAndSortIt(data):
    germany['Timestamps'] = germany['Last_Update']
    germany['Timestamps'] = germany['Timestamps'].apply(dateFunc).apply(toTimestamp)
    return germany.sort_values(by=['Timestamps'])

germany = getDataForContry('Germany')

germany = addTimeStampAndSortIt(germany)

germany.to_csv('germany.csv', sep='\t', encoding='utf-8')