# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 22:26:10 2021

@author: lasin
"""

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

@st.cache
def NBA_Data (nrows):
    data=pd.read_csv('https://raw.githubusercontent.com/lasindua/NBA-Shooting-Web-App/main/NBA_Table1.csv', nrows=nrows)
    data.sort_values('Name')
    return data
@st.cache
def NBA_Fig(nrows):
    Fig=pd.read_csv('https://raw.githubusercontent.com/lasindua/NBA-Shooting-Web-App/main/NBAFigDisplay.csv', nrows=nrows)
    return Fig 

@st.cache
def NBA_Fig2(nrows):
    Fig2=pd.read_csv('https://raw.githubusercontent.com/lasindua/NBA-Shooting-Web-App/main/NBAFigDisplay2.csv', nrows=nrows)
    return Fig2 
    
st.title("NBA Shooting :basketball:")

st.header("Percentage of shots taken from various distances and the corresponding field goal percentage")
st.subheader("""Data from the 2020-2021 Season""")


data_load_state = st.text('Loading data...')
data = NBA_Data(1000)
Figure1 = NBA_Fig(4000)
Figure2 = NBA_Fig2(4000)
data_load_state.text('Data loaded')


#Cleaned up Dataframe
st.text('Table of NBA Players (sort by clicking on a column)')
st.markdown('_*Data source: Basketball-Reference.com*_')
st.write(data)

st.header("""Visualized Player Shooting Stats""")
PlayerName = st.selectbox('Please select player: ',
                          data['Name'].unique())

#Chart Display
if PlayerName:
    data = data[data['Name'] == PlayerName]
    st.write(data)
    st.write('\n')
    Figure1 = Figure1[Figure1['Name'] == PlayerName]
    Figure2 = Figure2[Figure2['Name'] == PlayerName]
    st.subheader(PlayerName)
    BarGraph1 = alt.Chart(Figure1).mark_bar().encode(
        x = alt.X('Shot Distance', sort=('2P', '0-3', '3-10', '10-16', '16-3P', '3P')),
        y = alt.Y('FG%',
              scale = alt.Scale(domain =[0, 1])),color=alt.Color('FG%', scale=alt.Scale(scheme='inferno'))).properties(width=400,height=400)
    BarGraph2 = alt.Chart(Figure2).mark_bar().encode(
        x = alt.X('Shot Distance',sort=('2P', '0-3', '3-10', '10-16', '16-3P', '3P')),
        y = alt.Y('% of FG taken', 
              scale = alt.Scale(domain =[0, 1])), color=alt.Color('% of FG taken', scale=alt.Scale(scheme='inferno'))).properties(width=400, height=400)
    CombinedGraph = alt.vconcat(BarGraph1,BarGraph2)
    st.altair_chart(CombinedGraph)
st.markdown('*****2P is the average of all shooting distances until the 3P line')
st.markdown('*****2PA is the total of all shooting distances until the 3P line')
    

# if PlayerName == 'Name':
#     st.success('Confirmed!')

