# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 22:26:10 2021

@author: lasin
"""

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import os
#import matplotlib.pyplot as plt

# print(os.getcwd())
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)





@st.cache
def NBA_Data (nrows):
    data=pd.read_csv(NBA_Table1.csv, nrows=nrows)
    data.sort_values('Name')
    return data
@st.cache
def NBA_Fig(nrows):
    Fig=pd.read_csv(NBAFigDisplay.csv, nrows=nrows)
    return Fig 

@st.cache
def NBA_Fig2(nrows):
    Fig2=pd.read_csv(NBAFigDisplay2.csv, nrows=nrows)
    return Fig2 
    
st.title("NBA Shooting")

st.header("Percentage of shots taken from various distances and the field goal percentage")
st.subheader("""Data""")


data_load_state = st.text('Loading data...')
data = NBA_Data(1000)
Figure1 = NBA_Fig(4000)
Figure2 = NBA_Fig2(4000)
data_load_state.text('Loading data...done!')



st.text('Table of NBA Players (sort by clicking on a column)')
st.write(data)

st.subheader('Visualized Player Shooting Stats')
PlayerName = st.selectbox('Please select player: ',
                          data['Name'].unique())

#Fig = data.plot.bar(rot=0)
# FGA_Distance = st.selectbox('Please select distance for % of shots taken: ',
#                             ('2PA', '0-3A', '3-10A', '10-16A', '16-3PA', '3PA'))
# 
# FG_Distance = st.selectbox('Please select distance for FG%: ',
#                             ('2P', '0-3', '3-10', '10-16', '16-3P', '3P'))
# 

if PlayerName:
    data = data[data['Name'] == PlayerName]
    st.write(data)
    st.write('\n')
    Figure1 = Figure1[Figure1['Name'] == PlayerName]
    Figure2 = Figure2[Figure2['Name'] == PlayerName]
    BarGraph1 = alt.Chart(Figure1).mark_bar().encode(
        x = alt.X('Shot Distance'),
        y = alt.Y('FG%',
              scale = alt.Scale(domain =[0, 1]))).properties(width=400,height=400)
    BarGraph2 = alt.Chart(Figure2).mark_bar().encode(
        x = alt.X('Shot Distance'),
        y = alt.Y('% of FG taken', 
              scale = alt.Scale(domain =[0, 1]))).properties(width=400, height=400)
    CombinedGraph = alt.vconcat(BarGraph1,BarGraph2)
    st.altair_chart(CombinedGraph)
    

# if PlayerName == 'Name':
#     st.success('Confirmed!')

