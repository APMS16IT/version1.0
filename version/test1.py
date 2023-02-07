import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import datetime
from dateutil.relativedelta import relativedelta # to add days or years
import re
import openpyxl
from openpyxl import Workbook
import plotly.graph_objects as go
import pandas as pd
import plotly.figure_factory as ff
import random
import dd


@st.cache(persist=True, allow_output_mutation=True)
def load_data(eq_name, cols_to_use):
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
    if eq_name == 'DG1':
        df = pd.read_csv(data_url+"\\"+raw_data['d5'], usecols=cols_to_use)
        return df


st.set_page_config(
    page_title = 'APMS DIESEL GENERATOR 1',
    page_icon = '🇮🇳',
    layout = 'wide'
)


st.title("AI BASED APMS/IPMS")

equip=st.sidebar.selectbox("Select the Equipment", dd.equipment_list, index=7)

st.sidebar.title("AI BASED APMS/IPMS")


equip=st.sidebar.selectbox("Select the Equipment", dd.equipment_list)

if equip=='DG'or equip=='PLANT':
    equipment=st.sidebar.selectbox("Select Diesel Generator", dd.dg)
elif equip=='PLANT':
    equipment=st.sidebar.selectbox("Select the Plant", dd.plant)
elif equip=='UPS':
    equipment=st.sidebar.selectbox("Select the UPS", dd.ups)
elif equip=='SYSTEM':
    equipment=st.sidebar.selectbox("Select the System", dd.system)
elif equip=='CPP':
    equipment=st.sidebar.selectbox("Select the CPP", dd.cpp)
elif equip=='GEARBOX':
    equipment=st.sidebar.selectbox("Select the Gearbox", dd.gearbox)
elif equip=='SHAFTING':
    equipment=st.sidebar.selectbox("Select the Shafting", dd.shafting)
else:
    equipment=equip


if equip=='DG'or equip=='PLANT':
    data_url=r'C:\Users\LENOVO\Desktop\LiveDataModelling\data\L&T_CH1001_1250.csv'
    if equipment=='DG1':
        chlist=dd.dg1
    elif equipment=='DG2':
        chlist=dd.dg2
    elif equipment=='DG3':
        chlist=dd.dg3
    else:
        chlist=dd.dg4
elif equip=='INTERNAL':
    data_url=r'C:\Users\LENOVO\Desktop\LiveDataModelling\data\L&T_CH1751_2000.csv'
    chlist=dd.internal
else:
    st.error("No data found.")





df = pd.read_csv(data_url)
st.title("Real-Time Data Visualisation")

start_date= df['Date'][0]
end_date= df['Date'][(len(df['Date'])-1)]
start_date_lis= re.split('-|/',start_date)
end_date_lis= re.split('-|/',end_date)


format = 'DD-MM-YY' #'YYYY-MM-DD'  # format output
start_date = datetime.date(year=int(start_date_lis[2]),month=int(start_date_lis[1]),day=int(start_date_lis[0]))-relativedelta(years=0)
end_date = datetime.date(year=int(end_date_lis[2]),month=int(end_date_lis[1]),day=int(end_date_lis[0]))-relativedelta(years=0)

max_days = end_date-start_date
slider = st.sidebar.slider('Select date', min_value=start_date, value=[start_date,end_date] ,max_value=end_date, format=format)
st.sidebar.write("Duration: ", slider[0].strftime('%Y/%m/%d')," - ", slider[1].strftime('%Y/%m/%d'))




split_date_start =pd.Series(slider[0].strftime('%d-%m-%Y'))
split_date_end = pd.Series(slider[1].strftime('%d-%m-%Y'))
df = df[(df['Date'] <= split_date_end[0]) | (df['Date'] >= split_date_start[0])]


# while True:
voltage=[]
current=[]
for i in range(len(chlist[0])):
    voltage.append('volt'+str(i))
    df['volt'+str(i)] = df[chlist[0][i]]
for j in range(len(chlist[1])):
    current.append('amp'+str(j))
    df['amp'+str(j)] = df[chlist[1][j]]
df['DateTime'] = df['Date']+' '+df['Time']
print(voltage,current)


df = df[(df['Date'] <= split_date_end[0]) | (df['Date'] >= split_date_start[0])]
df_amp = df[['Date', 'amp0','amp1','amp2']].set_index('Date')
df_volt = df[['Date','volt0','volt1','volt2']].set_index('Date')


# Calculating the mean of Voltage, Current 
df = df[(df['Date'] <= split_date_end[0]) | (df['Date'] >= split_date_start[0])]
ph_mean_volts, ph_mean_amp=df_volt.groupby('Date',sort=False).mean(),df_amp.groupby('Date',sort=False).mean()

st.markdown("### Phase wise mean volatge")
mean_fig = px.line(ph_mean_volts, y=voltage)
st.write(mean_fig)


st.markdown("### Phase wise mean Current")
mean_fig = px.line(ph_mean_amp, y=current)
st.write(mean_fig)



# Calculating the standard deviation of Voltage, Current 
df = df[(df['Date'] <= split_date_end[0]) | (df['Date'] >= split_date_start[0])]
ph_sd_volts, ph_sd_amp=df_volt.groupby('Date',sort=False).std(),df_amp.groupby('Date',sort=False).std()

st.markdown("### Phase wise standard deviation volatge")
mean_fig = px.line(ph_sd_volts, y=voltage)
st.write(mean_fig)


st.markdown("### Phase wise standard deviation current")
mean_fig = px.line(ph_sd_amp, y=current)
st.write(mean_fig)


        

df_volt = df[['Date', 'Ch 1195','Ch 1205','Ch 1215','Ch 1225']].set_index('Date')
ph_mean_volts=df_volt.groupby('Date',sort=False).mean()
ph_sd_volts=df_volt.groupby('Date',sort=False).std()
st.write(random.gauss(ph_mean_volts, ph_mean_volts))

st.markdown("### Phase wise mean volatge of Phase 1")
voltage=['Ch 1195','Ch 1205','Ch 1215','Ch 1225']
mean_fig = px.line(ph_mean_volts, y=voltage)
st.write(mean_fig)



df_volt = df[['Date','Ch 1197','Ch 1207','Ch 1217', 'Ch 1227']].set_index('Date')
ph_mean_volts=df_volt.groupby('Date',sort=False).mean()
st.markdown("### Phase wise mean volatge of Phase 2")
voltage=['Ch 1197','Ch 1207','Ch 1217', 'Ch 1227']
mean_fig = px.line(ph_mean_volts, y=voltage)
st.write(mean_fig)




df_volt = df[['Date','Ch 1199','Ch 1209', 'Ch 1219','Ch 1229']].set_index('Date')
ph_mean_volts=df_volt.groupby('Date',sort=False).mean()
st.markdown("### Phase wise mean volatge of Phase 3")
voltage=['Ch 1199','Ch 1209', 'Ch 1219','Ch 1229']
mean_fig = px.line(ph_mean_volts, y=voltage)
st.write(mean_fig)


# @st.cache
# def gaussian(x, mean, std):
#     return (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)

# df_volt = df[['Date','Ch 1199','Ch 1209', 'Ch 1219','Ch 1229']].set_index('Date')
# mean=df_volt.groupby('Date',sort=False).mean()
# std=df_volt.groupby('Date',sort=False).std()
# st.markdown("### Phase wise mean volatge of Phase 3")
# voltage=['Ch 1199','Ch 1209', 'Ch 1219','Ch 1229']
# x = df[(df['Date'] <= split_date_end[0]) | (df['Date'] >= split_date_start[0])]
# mean_fig = px.line(gaussian(x, mean, std), y=voltage)

# st.write(mean_fig)






