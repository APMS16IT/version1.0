import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import datetime
from dateutil.relativedelta import relativedelta # to add days or years
import re
import plotly.graph_objects as go
import pandas as pd
import plotly.figure_factory as ff
from scipy.stats import norm
import dd # Data Definitions

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
    page_title = 'AI Based APMS/ IPMS',
    page_icon = '🇮🇳',
    layout = 'wide'
)
df = pd.read_csv(r'C:\Users\LENOVO\Desktop\LiveDataModelling\data\L&T_CH1001_1250.csv')

st.title("AI BASED APMS/IPMS")
start_date= df['Date'][0]
end_date= df['Date'][(len(df['Date'])-1)]
start_date_lis= re.split('-|/',start_date)
end_date_lis= re.split('-|/',end_date)

# format = 'DD-MM-YY' #'YYYY-MM-DD'  # format output
start_date = datetime.date(year=int(start_date_lis[2]),month=int(start_date_lis[1]),day=int(start_date_lis[0]))
end_date = datetime.date(year=int(end_date_lis[2]),month=int(end_date_lis[1]),day=int(end_date_lis[0]))

equip=st.sidebar.selectbox("Select the Equipment", dd.equipment_list, index=7)

if equip=='DG':
    equipment=st.sidebar.selectbox("Select Diesel Generator", dd.dg)
    if equipment=='DG1':
        df_dg1_current = load_data('DG1', cols_to_use = dd.dg1[1])
        df_dg1_current.dropna(inplace=True)
    
    with st.sidebar.container():
        col1, col2 = st.sidebar.columns(2)
        with col1: 
            start_date = st.date_input('Start Date:',value=start_date, min_value=start_date, max_value=end_date) # omit "sidebar"
        with col2: 
            end_date = st.date_input('End Date:',value=end_date, min_value=start_date,max_value=end_date) # omit "sidebar"

    st.write("Dates are in between ",start_date, "and", end_date)
    

    if st.sidebar.checkbox('Analyse Current values'):

        fig = go.Figure()
        current_1 = df_dg1_current[8000:9000]
        st.write(current_1)
        fig.add_trace(go.Scatter( y=current_1['Ch 1196'],mode='lines',name='DG1_Current_Phase_1'))
        fig.add_trace(go.Scatter(y=current_1['Ch 1198'],mode='lines',name='DG1_Current_Phase_2'))
        fig.add_trace(go.Scatter(y=current_1['Ch 1200'],mode='lines', name='DG1_Current_Phase_3'))

        st.plotly_chart(fig, use_container_width=True)

    if st.sidebar.checkbox('Compare the current data distribution'):
        
        fig = go.Figure()
        current_1 = df_dg1_current[8000:9000]

        mu, sigma = np.mean(current_1['Ch 1196']), np.std(current_1['Ch 1196'])
        s = np.random.normal(mu, sigma, 1000)
        fig.add_trace(go.Scatter(x=s,y=norm.pdf(s, mu, sigma),mode='markers',marker_size=5,name='DG1_Current_Phase_1'))
        mu, sigma = np.mean(current_1['Ch 1198']), np.std(current_1['Ch 1198'])
        s = np.random.normal(mu, sigma, 1000)
        fig.add_trace(go.Scatter(x=s,y=norm.pdf(s, mu, sigma),mode='markers',marker_size=5,name='DG1_Current_Phase_2'))
        mu, sigma = np.mean(current_1['Ch 1200']), np.std(current_1['Ch 1200'])
        s = np.random.normal(mu, sigma, 1000)
        fig.add_trace(go.Scatter(x=s,y=norm.pdf(s, mu, sigma),mode='markers',marker_size=5,name='DG1_Current_Phase_3'))

        st.plotly_chart(fig, use_container_width=True)
    
    else:
        df = pd.read_csv(r'C:\Users\LENOVO\Desktop\LiveDataModelling\data\L&T_CH1001_1250.csv')

        split_date_start =pd.Series(start_date.strftime('%d-%m-%Y'))
        split_date_end = pd.Series(end_date.strftime('%d-%m-%Y'))
        df = df[(df['Date'] <= split_date_end[0]) | (df['Date'] >= split_date_start[0])]
        
        df_volt = df[['Date', 'Ch 1195','Ch 1197','Ch 1199']].set_index('Date')
        st.markdown("### Voltage ")
        voltage=['Ch 1195','Ch 1197','Ch 1199']
        mean_fig = px.line(df_volt, y=voltage)
        st.write(mean_fig)

        df_current = df[['Date', 'Ch 1196', 'Ch 1198', 'Ch 1200']].set_index('Date')
        st.markdown("### Current ")
        current=['Ch 1196', 'Ch 1198', 'Ch 1200']
        mean_fig = px.line(df_current, y=current)
        st.write(mean_fig)


        df_volt = df[['Date','Ch 1195','Ch 1205', 'Ch 1215','Ch 1225']].set_index('Date')
        ph_mean_volts=df_volt.groupby('Date',sort=False).mean()
        st.markdown("### Phase wise mean voltage of Phase 1")
        voltage=['Ch 1195','Ch 1205', 'Ch 1215','Ch 1225']
        mean_fig = px.line(ph_mean_volts, y=voltage)
        st.write(mean_fig)

        df_volt = df[['Date','Ch 1196','Ch 1206', 'Ch 1216','Ch 1226']].set_index('Date')
        ph_mean_volts=df_volt.groupby('Date',sort=False).mean()
        st.markdown("### Phase wise mean current of Phase 1")
        voltage=['Ch 1196','Ch 1206', 'Ch 1216','Ch 1226']
        mean_fig = px.line(ph_mean_volts, y=voltage)
        st.write(mean_fig)



