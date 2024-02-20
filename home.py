import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import util as ut
import osmnx as ox
import io
from PIL import Image

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title(' Beatifull Strava')

uploaded_file = st.file_uploader("Choose a Strava Route GPX",type=['gpx'],accept_multiple_files=False)

col1, col2, col3 , col4 ,col5= st.columns(5)

figure = st.pyplot()
fig = None

def on_color_change():
    if uploaded_file is not None:
      update_fig()

with col1:
   colorBackground   = st.color_picker('Background Color', "#06152A", on_change = on_color_change)
   #st.session_state.prev_color = colorBackground

with col2:
   colorLines   = st.color_picker('Lines Color', "#9DA5D9", on_change = on_color_change)

with col3:
   colorRoute  = st.color_picker('Route Color', "#E64E25", on_change = on_color_change)

with col4:
   colorText   = st.color_picker('Text Color', '#00f900', on_change = on_color_change)

with col5:
   title  = st.text_input('Title of Route', 'Title',on_change = on_color_change )

# Crea una figura 

route_df = None


def update_fig():
   global fig
   fig = ut.plot_figure(global_variable , route_df ,colorBackground , 
                         colorLines,colorRoute,title,colorText )
   figure.pyplot(fig)

def read_route(file):
    global route_df
    route_df  = ut.read_gpx_file(file)
    c         = ut.find_centroid(route_df)
    d         = ut.get_dist_graph(route_df ,  c)
    G         = ox.graph_from_point(c, dist=d, retain_all=True, simplify = True, network_type='bike')
    global global_variable
    global_variable = G
    update_fig()

if uploaded_file is not None:
    # To read file as bytes:
   read_route(uploaded_file)

name_file  = title+".png"
# Create the download button

# Convert the figure to different image formats
def fig_to_bytes(fig, format='png'):
    buf = io.BytesIO()
    fig.savefig(buf, format=format)
    buf.seek(0)
    return buf.getvalue()


if uploaded_file is not None:
   
   name_file  = title+".png"
# Assuming you have a figure 'fig' already defined
   png_data = fig_to_bytes(fig, format='png')

   btn = st.download_button(
      label="Download image",
      data=png_data,
      file_name=name_file,
      mime="image/png"
   )


