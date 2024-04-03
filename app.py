import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="superstore", page_icon= ':chart_with_upwards_trend:', layout= 'wide')
st.title(":chart_with_upwards_trend: Superstore EDA")
st.markdown("<style>div.block-container{padding-top-1rem;}</style>", unsafe_allow_html= True)

f1 = st.file_uploader(":file_folder: Upload a file", type = (['csv']))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename)
else:
    df = pd.read_csv(r'D:\Time_series_project\data_material.csv')


# ### PUBLIC PROPERTIES

# hello my name is akash

# * completed masters from IIT
# * learning Data scince and Quantitative finace

# 1. Enumerate 1
# 2. Enumerate 2
# 3. Enumerate 3
# """
# import pandas as pd

# df =pd.read_csv(r'D:\Time_series_project\Sample - Superstore.xls')
# #df

# st.write("A megical method of learning")

# # st.write(df)
# # st.table(df)

# df.set_index('Date')
# st.line_chart(df[['Adj Close']])

