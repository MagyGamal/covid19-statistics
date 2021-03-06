from flask import Flask, redirect, url_for, render_template, request
import json
import requests as req
import plotly.graph_objects as go
import math
import pandas as pd
import pylab
from sklearn.metrics import r2_score

# start app
app = Flask(__name__)

# request for all countries
response = req.get('https://api.covid19api.com/countries')
response = sorted(response.json(), key=lambda i: i['Country'])

@app.route("/", methods=["GET","POST"])
def home():
  # chosen values
  country = request.args.get('country')
  status = request.args.get('status')
  graph = request.args.get('graph')
  country_1 = request.args.get('country_1')
  country_2 = request.args.get('country_2')
  status_2 = request.args.get('status_2')
  chart = request.args.get('chart')
  country_chart = request.args.get('country_chart')
  date= request.args.get('date')
  # if user has chosen a value
  if status and country and graph:
    # request for the given data
    result = req.get('https://api.covid19api.com/total/country/' + country + '/status/' + status)
    # prepare the X,Y of the graph
    dates = []
    cases = []
    for inADay in result.json():
      dates.append(inADay['Date'])
      cases.append(inADay['Cases'])
    # show the graph
    if graph == 'Line':
      (go.Figure(data=[go.Line(x=dates, y=cases)])).show()
    elif graph == 'Bars':
      (go.Figure(data=[go.Bar(x=dates, y=cases)])).show()
 
  
  elif country_chart and chart == "R":
    if country_chart== "World":
        days=[]
        worlddays=[]
        result = req.get('https://pomber.github.io/covid19/timeseries.json')
        result = result.json()
#        dates= []
#        for date in result['Afghanistan']:
#            dates.append(result['Afghanistan']['date'])
        for day in range(1,len(result['Afghanistan'])):
            worldcases=0
            for country in result:
                daily=result[country][day]['confirmed']-result[country][day-1]['confirmed']
                worldcases+=daily
            worlddays.append(worldcases)    
            days.append(day)
        for i in range (len(worlddays)):
            worlddays[i]= math.log(worlddays[i],2)
        days = pylab.array(days)
        worlddays = pylab.array(worlddays)
        if date=="all":
            A,B= pylab.polyfit(days, worlddays, 1)
            worlddays_predicted=A*pylab.array(days)+B
            virusworldR=2**(A*6)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=days, y=worlddays, name='log(world cases)' ,mode='markers', marker_color='red'))
            fig.add_trace(go.Scatter(x=days, y=worlddays_predicted, name='log(world cases predicted)', mode='markers',marker_color='green'))
            fig.update_layout( title=virusworldR,xaxis_title="days",yaxis_title="log(cases)",
            font=dict(family="Courier New, monospace",size=18,color="#7f7f7f"))
            print(r2_score(worlddays_predicted, worlddays))
            fig.show()
        elif date=='daily':
            two_weeks_cases=worlddays[-14:len(worlddays)]
            two_weeks=days[-14:len(days)]
            A,B=pylab.polyfit(two_weeks,two_weeks_cases,1)
            two_weeks_cases_predicted=A*pylab.array(two_weeks)+B
            R_daily=2**(A*6)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=two_weeks, y=two_weeks_cases, name='log(world cases)' ,mode='markers', marker_color='red'))
            fig.add_trace(go.Scatter(x=two_weeks, y=two_weeks_cases_predicted, name='log(world cases predicted)', mode='markers',marker_color='green'))
            fig.update_layout( title=R_daily,xaxis_title="days",yaxis_title="log(cases)",
            font=dict(family="Courier New, monospace",size=18,color="#7f7f7f"))
#            print(r2_score(R_daily, two_weeks_cases))
            fig.show()
        
    else:
        payload = {'country': country_chart}
        URL = 'https://api.statworx.com/covid'
        result = req.request("POST", url=URL, data=json.dumps(payload))
        discrete_cases = result.json()['cases']
        logn_t = []
        days_array = []
        firstday=0
        for d in range (0,len(discrete_cases)):
            if discrete_cases[d]!=0:
                firstday=d
                break
        for i in range(firstday,len(discrete_cases)):
            if discrete_cases[i] == 0:
               logn_t.append(0)
            else:
                logn_t.append(int(math.log(float(discrete_cases[i]), 2)))
            days_array.append(i)
        dates = pylab.array(days_array)
        logn_t = pylab.array(logn_t)
        if date=="all":
            a,b= pylab.polyfit(dates, logn_t, 1)
            logn_t_predicted = a*pylab.array(dates)+b
               #slope
            virus_reproduction=2**(a*6)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=logn_t, name='log(cases)',mode='markers', marker_color='red'))
            fig.add_trace(go.Scatter(x=dates, y=logn_t_predicted, name='log(cases predictec)', mode='markers',marker_color='green'))
            fig.update_layout(
            title=virus_reproduction,
            xaxis_title="days",
            yaxis_title="log(cases)",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"))
            print(r2_score(logn_t_predicted, logn_t))
            fig.show()
        elif date=='daily':
            two_weeks_cases=logn_t[-14:len(logn_t)]
            two_weeks=dates[-14:len(dates)]
            A,B=pylab.polyfit(two_weeks,two_weeks_cases,1)
            two_weeks_cases_predicted=A*pylab.array(two_weeks)+B
            R_daily=2**(A*6)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=two_weeks, y=two_weeks_cases, name='log(world cases)' ,mode='markers', marker_color='red'))
            fig.add_trace(go.Scatter(x=two_weeks, y=two_weeks_cases_predicted, name='log(world cases predicted)', mode='markers',marker_color='green'))
            fig.update_layout( title=R_daily,xaxis_title="days",yaxis_title="log(cases)",
            font=dict(family="Courier New, monospace",size=18,color="#7f7f7f"))
#            print(r2_score(R_daily, two_weeks_cases))
            fig.show()
        
    
    
    
  elif country_1 and country_2 and status_2:
    result = req.get('https://api.covid19api.com/total/country/' + country_1 + '/status/' + status_2)
    # prepare the X,Y of the graph
    dates = []
    cases = []
    for inADay in result.json():
      dates.append(inADay['Date'])
      cases.append(inADay['Cases'])
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dates, y=cases, name=country_1, marker_color='red'))
    result = req.get('https://api.covid19api.com/total/country/' + country_2 + '/status/' + status_2)
    # prepare the X,Y of the graph
    dates = []
    cases = []
    for inADay in result.json():
      dates.append(inADay['Date'])
      cases.append(inADay['Cases'])

    fig.add_trace(go.Bar(x=dates, y=cases, name=country_2, marker_color='green'))
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.show()
  elif country == '' or status == '' or graph == '' or country_1 == '' or country_2 == '' or status_2 == '':
    error_message = {
        'country': country,
        'status': status,
        'graph': graph,
        'country_1': country_1,
        'country_2': country_2,
        'status_2': status_2,
    }
    return render_template("Index.html", countries=response, errorMessage=error_message)

  return render_template("Index.html", countries=response, errorMessage={})


if __name__ == '__main__':
  app.run(debug=True)
