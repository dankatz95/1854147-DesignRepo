import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
import os
import plotly
import plotly.express as ex
import plotly.graph_objs as go
import matplotlib.pyplot as plt

def plotVelocity(df, time="Date"):
    fig, ax = plt.subplots()
    ax.plot([getTimestamp(x.Date) for x in df.select(time).collect()], [x.velocity for x in df.select('velocity').collect()] )
    
def plotFigure(df, time="Date", velocity="velocity"):
    x = df.select(time).toPandas()[time]
    y = df.select(velocity).toPandas()[velocity]
    fig = go.Figure([go.Scatter(x=x, y=y)])
    fig.show()
    
def plotMap(dataframe):
    temp = dataframe.toPandas()
    
    fig = ex.scatter_mapbox(
        temp, lat=temp['Latitude'], 
        lon=temp['Longitude'], 
        zoom=10, 
        opacity=1, 
        size_max=20, 
        title="GeoTagging", 
        width=1200, 
        height =800, 
        template="plotly_dark", 
        hover_data=['Date'])
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show() 

def plotTimeSeries(x, y):
    fig = go.Figure([go.Scatter(x=x, y=y)])
    fig.show()