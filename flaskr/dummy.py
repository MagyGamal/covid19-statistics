from flask import Flask, redirect, url_for, render_template, request
import json
import requests as req
import plotly.graph_objects as go
import math
import pylab
from sklearn.metrics import r2_score

days=[]
worlddays=[]
result = req.get('https://pomber.github.io/covid19/timeseries.json')
result = result.json()
print(result)
for day in range(1,len(result['Afghanistan'])):
    worldcases=0
    for country in result:
        daily=result[country][day]['confirmed']-result[country][day-1]['confirmed']
        print("daily",daily)
        worldcases+=daily
    worlddays.append(worldcases)
    print(worlddays)
    days.append(day)
print(worlddays)
for i in range (len(worlddays)):
    worlddays[i]= math.log(worlddays[i],2)
days = pylab.array(days)
worlddays = pylab.array(worlddays)
A,B= pylab.polyfit(days, worlddays, 1)
worlddays_predicted=A*pylab.array(days)+B
virusworldR=2**(A*6)
print("worldR",virusworldR)
fig = go.Figure()
fig.add_trace(go.Scatter(x=days, y=worlddays, name='log(world cases)' ,mode='markers', marker_color='red'))
fig.add_trace(go.Scatter(x=days, y=worlddays_predicted, name='log(world cases predicted)', mode='markers',marker_color='green'))
fig.update_layout( title=virusworldR,xaxis_title="days",yaxis_title="log(cases)",
font=dict(family="Courier New, monospace",size=18,color="#7f7f7f"))
print(r2_score(worlddays_predicted, worlddays))
fig.show()
