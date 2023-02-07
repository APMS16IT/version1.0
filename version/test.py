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
import altair as alt


equipment_list = [
    'PLANT', 'UPS', 'AFAS', 'AFDS', 'AVCAT', 'BILGE SYSTEM', 
    'SWITCHBOARD & APMS', 'DG', 'DOOR & HATCH MONITORING',
    'EDG', 'FIN STABILIZER', 'FIREMAIN SYSTEM', 'SYSTEM', 
    'HPAC', 'INTERNAL', 'NETWORK MONITORING', 'OWS', 'PME', 
    'POL STATUS', 'CPP', 'GEARBOX', 'SHAFTING', 'RECTIFIER', 
    'SME', 'STEERING GEAR', 'STP', 'VENTILATION'
]

plant=[
    'AC PLANT', 
    'REF PLANT', 
    'RO PLANT'
]

ups=[
    'AC UPS', 'DC UPS'
]

system=[
    'BILGE SYSTEM', 
    'FO SYSTEM', 
    'FW SYSTEM', 
    'LO SYSTEM', 
    'PROPULSION CONTROL SYSTEM'
]

cpp=[
    'PORT CPP', 'STBD CPP'
]

gearbox=[
    'PORT GEARBOX', 'STBD GEARBOX'
]

shafting=[
    'PORT SHAFTING', 'STBD SHAFTING'
]

dg=[
    'DG1', 'DG2', 'DG3', 'DG4'
]

dg1=[[
    'Ch 1195','Ch 1197','Ch 1199'
],[
    'Ch 1196', 'Ch 1198', 'Ch 1200'
]]

dg2=[[
    'Ch 1205', 'Ch 1207', 'Ch 1209'
],[
    'Ch 1206', 'Ch 1208', 'Ch 1210'
]]

dg3=[[
    'Ch 1215', 'Ch 1217', 'Ch 1219'
],[
    'Ch 1216', 'Ch 1218', 'Ch 1220'
]]

dg4=[[
    'Ch 1225', 'Ch 1227', 'Ch 1229'
],[
    'Ch 1226', 'Ch 1228', 'Ch 1230'
]]

internal=[[
    'Ch 1884', 'Ch 1886', 'Ch 1888',
    'Ch 1894', 'Ch 1896', 'Ch 1898',
    'Ch 1904', 'Ch 1906', 'Ch 1908',
    'Ch 1914', 'Ch 1916', 'Ch 1918'
],[
    'Ch 1885', 'Ch 1887', 'Ch 1889',
    'Ch 1895', 'Ch 1897', 'Ch 1899',
    'Ch 1905', 'Ch 1907', 'Ch 1909',
    'Ch 1915', 'Ch 1917', 'Ch 1919'
]]


st.set_page_config(
    page_title = 'APMS DIESEL GENERATOR',
    page_icon = '🇮🇳',
    layout = 'wide'
)

#maindata_url=('C:\\Users\\Administrator\\Desktop\\data\\RCS Signals with Equipment Name_INS Sunayna_Segregated.xlsx')

equip=st.sidebar.selectbox("Select the Equipment", equipment_list)

if equip=='DG' or equip=='PLANT':
    equipment=st.sidebar.selectbox("Select Diesel Generator", dg)
elif equip=='PLANT':
    equipment=st.sidebar.selectbox("Select the Plant", plant)
elif equip=='UPS':
    equipment=st.sidebar.selectbox("Select the UPS", ups)
elif equip=='SYSTEM':
    equipment=st.sidebar.selectbox("Select the System", system)
elif equip=='CPP':
    equipment=st.sidebar.selectbox("Select the CPP", cpp)
elif equip=='GEARBOX':
    equipment=st.sidebar.selectbox("Select the Gearbox", gearbox)
elif equip=='SHAFTING':
    equipment=st.sidebar.selectbox("Select the Shafting", shafting)
else:
    equipment=equip


if equip=='DG' or equip=='PLANT':
    data_url=r'C:\Users\LENOVO\Desktop\LiveDataModelling\data\L&T_CH1001_1250.csv'
    # data_url="C:\\Users\\Administrator\\Desktop\\data\\L&T_CH1001_1250.csv"
    if equipment=='DG1':
        chlist=dg1
    elif equipment=='DG2':
        chlist=dg2
    elif equipment=='DG3':
        chlist=dg3
    else:
        chlist=dg4
elif equip=='INTERNAL':
    data_url=r'C:\Users\LENOVO\Desktop\LiveDataModelling\data\L&T_CH1751_2000.csv'
    chlist=internal
else:
    st.error("No data found.")


@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(data_url,parse_dates=True)


#description=st.sidebar.selectbox("Select the channel: ", set(des_list))       

df = pd.read_csv(data_url)
st.title("Real-Time Data Visualisation")

start_date= df['Date'][0]
end_date= df['Date'][(len(df['Date'])-1)]
start_date_lis= re.split('-|/',start_date)
end_date_lis= re.split('-|/',end_date)



# Range selector
format = 'DD-MM-YY' #'YYYY-MM-DD'  # format output
start_date = datetime.date(year=int(start_date_lis[2]),month=int(start_date_lis[1]),day=int(start_date_lis[0]))-relativedelta(years=0)
end_date = datetime.date(year=int(end_date_lis[2]),month=int(end_date_lis[1]),day=int(end_date_lis[0]))-relativedelta(years=0)
max_days = end_date-start_date



slider = st.sidebar.slider('Select date', min_value=start_date, value=[start_date,end_date] ,max_value=end_date, format=format)
st.sidebar.write("Duration: ", slider[0].strftime('%Y/%m/%d')," - ", slider[1].strftime('%Y/%m/%d'))


placeholder = st.empty()
pd.to_datetime(df['Date'])



# df=df.fillna(0)
while True:
    date_list= df['Date']
    # import pdb; pdb.set_trace()
    voltage=[]
    current=[]
    for i in range(len(chlist[0])):
        voltage.append('volt'+str(i))
        df['volt'+str(i)] = df[chlist[0][i]]
    for j in range(len(chlist[1])):
        current.append('amp'+str(j))
        df['amp'+str(j)] = df[chlist[1][j]]
   
   
    df_volt = df[['Date','volt0','volt1','volt2']].set_index('Date')
    df_amp = df[['Date', 'amp0','amp1','amp2']].set_index('Date')
    with placeholder.container():

        fig_col1, fig_col2= st.columns(2)
       
        with fig_col1:
            st.markdown("### Voltage")
            st.line_chart(df_volt)
        
        with fig_col2:
            st.markdown("### Current")
            st.line_chart(df_amp)
             
        time.sleep(1)
   