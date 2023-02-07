import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.graph_objects as go
import numpy as np

pd.set_option('display.max_columns',None, 'display.max_rows', None)
dg1=[[
    'Ch 1195','Ch 1197','Ch 1199'
],[
    'Ch 1196', 'Ch 1198', 'Ch 1200'
]]
raw_data = {
        'd1':'L&T_CH1_250.csv',
        'd2':'L&T_CH251_500.csv',
        'd3':'L&T_CH501_750.csv',
        'd4':'L&T_CH751_1000.csv',
        'd5':'L&T_CH1001_1250.csv',
        'd6':'L&T_CH1251_1500.csv',
        'd7':'L&T_CH1501_1750.csv',
        'd8':'L&T_CH1751_2000.csv',
        'd9':'L&T_CH2001_2250.csv',
        'd10':'L&T_CH2251_2500.csv',
        'd11':'L&T_CH2501_2750.csv',
        'd12':'L&T_CH2751_3000.csv',
        'd13':'L&T_CH3001_2250.csv'
    }
data_url=r'C:\Users\LENOVO\Desktop\LiveDataModelling\data'
df_dg1_current = pd.read_csv(data_url+"\\"+raw_data['d5'], usecols=dg1[1])
df_dg1_current.head()
df_dg1_current.dropna(inplace=True)

fig = go.Figure()
current_1 = df_dg1_current[8000:9000]
fig.add_trace(go.Scatter( y=current_1['Ch 1196'],
                    mode='lines',
                    name='DG1_Current_Phase_1'))
fig.add_trace(go.Scatter(y=current_1['Ch 1198'],
                    mode='lines',
                    name='DG1_Current_Phase_2'))
fig.add_trace(go.Scatter(y=current_1['Ch 1200'],
                    mode='lines', name='DG1_Current_Phase_3'))

fig.show()

fig = go.Figure()
current_1 = df_dg1_current[8000:9000]

mu, sigma = np.mean(current_1['Ch 1196']), np.std(current_1['Ch 1196'])
s = np.random.normal(mu, sigma, 1000)
fig.add_trace(go.Scatter(x=s,y=norm.pdf(s, mu, sigma),
                    mode='markers',
                    marker_size=5,
                    name='DG1_Current_Phase_1'))
mu, sigma = np.mean(current_1['Ch 1198']), np.std(current_1['Ch 1198'])
s = np.random.normal(mu, sigma, 1000)
fig.add_trace(go.Scatter(x=s,y=norm.pdf(s, mu, sigma),
                    mode='markers',
                    marker_size=5,
                    name='DG1_Current_Phase_2'))
mu, sigma = np.mean(current_1['Ch 1200']), np.std(current_1['Ch 1200'])
s = np.random.normal(mu, sigma, 1000)
fig.add_trace(go.Scatter(x=s,y=norm.pdf(s, mu, sigma),
                    mode='markers',
                    marker_size=5,
                    name='DG1_Current_Phase_3'))
import streamlit as st # web development

st.write(fig.show())