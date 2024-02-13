import streamlit as st
import pandas as pd
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np

uploaded_file = st.file_uploader("Choose a Strava Route GPX")

col1, col2, col3 , col4= st.columns(4)

with col1:
   colorBackground   = st.color_picker('Background Color', '#00f900')

with col2:
   colorLines   = st.color_picker('Lines Color', '#00f900')

with col3:
   colorRoute  = st.color_picker('Route Color', '#00f900')

with col4:
   colorText   = st.color_picker('Text Color', '#00f900')

# Crea una figura sin ejes
fig = plt.figure(facecolor=colorBackground)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()


st.pyplot(fig)


if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)