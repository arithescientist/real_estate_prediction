import pandas as pd
import json
import folium
from folium.plugins import MarkerCluster # for clustering the markers
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import scipy.stats as scs
import numpy as np



def create_map_Kc_County(df,col,legend ='Insert legend description'):
    """
    Generates a folium map of Seattle
    :param zipcode_data: zipcode dataset
    :param col: feature to display
    :param legend: Insert description for legend based on feature
    :return: mp
    """ 
    kc_geo = r'../data/cleaned_geodata.json'
    mp = folium.Map(location=[47.608013, -122.335167], default_zoom_start=11)

    folium.Choropleth(geo_data=kc_geo, 
                # my dataset                      
                 data=df, 
                # zip code is here for matching the geojson zipcode, col changes the color of zipcode areas
                 columns=['zipcode', col],
                # this path contains zipcodes in str type, this zipcodes should match with our ZIP CODE column
                 key_on='feature.properties.ZIPCODE', 
                 fill_color='Reds', legend_name=legend,fill_opacity=0.7, line_opacity=0.3).add_to(mp)
   
    mp.save(outfile = '../maps/'+ col + '.html')
    



