import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import util as ut
import osmnx as ox

uploaded_file = st.file_uploader("Choose a Strava Route GPX",type=['gpx'])

col1, col2, col3 , col4 ,col5= st.columns(5)

with col1:
   colorBackground   = st.color_picker('Background Color', "#415DC0")

with col2:
   colorLines   = st.color_picker('Lines Color', "#9DA5D9")

with col3:
   colorRoute  = st.color_picker('Route Color', "#E64E25")

with col4:
   colorText   = st.color_picker('Text Color', '#00f900')

with col5:
   title  = st.text_input('Title of Figure', 'title')

button = st.button("Update Map", type="primary")



# Crea una figura sin ejes

route_df = None

def read_route(file):
    global route_df
    route_df = ut.read_gpx_file(file)
    c        = ut.find_centroid(route_df)
    d        =  ut.get_dist_graph(route_df ,  c)
    elevation = route_df.elevation
    x_plot    = range(len(elevation))
    min_elev  = min(elevation) - 25
    G = ox.graph_from_point(c, dist=d, retain_all=True, simplify = True, network_type='bike')
    global global_variable
    global_variable = G




if uploaded_file is not None:
    # To read file as bytes:
   read_route(uploaded_file)

if button:
    fig, ax = ox.plot_graph(global_variable, node_size=0,
                        figsize        = (27, 40), 
                        dpi            = 300,
                        save           = False,
                        bgcolor        = colorBackground,
                        edge_color     = colorLines,
                        edge_alpha     = 1 ,
                        show           = False)
    
## Plot  activity in graph 
    ax.plot( route_df['longitude'] , route_df['latitude'] ,
               color     = colorRoute , 
               linewidth = 4.0)
      #bbox={'facecolor': '#415DC0', 'edgecolor': '#415DC0', 'pad': 5}
    ax.text(0.5, 0.95, title, horizontalalignment='center',color = colorText,
         verticalalignment='top', transform=ax.transAxes, fontsize=150)
    st.pyplot(fig)
