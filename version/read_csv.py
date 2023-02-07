import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta # to add days or years
import re
import streamlit as st # web development
import plotly.express as px # interactive charts 




data_url=r'C:\Users\LENOVO\Desktop\LiveDataModelling\data\L&T_CH1001_1250.csv'
df = pd.read_csv(data_url)
fig = px.line(df, x="Date", y="Ch 1196", color='Ch 1037')
fig.show()

start_date= df['Date'][0]
end_date= df['Date'][(len(df['Date'])-1)]
start_date_lis= re.split('-|/',start_date)
end_date_lis= re.split('-|/',end_date)


format = 'DD-MM-YY' #'YYYY-MM-DD'  # format output
start_date = datetime.date(year=int(start_date_lis[2]),month=int(start_date_lis[1]),day=int(start_date_lis[0]))-relativedelta(years=0)
end_date = datetime.date(year=int(end_date_lis[2]),month=int(end_date_lis[1]),day=int(end_date_lis[0]))-relativedelta(years=0)


max_days = end_date-start_date
slider = st.sidebar.slider('Select date', min_value=start_date, value=[start_date,end_date] ,max_value=end_date, format=format)
st.sidebar.write("Duration: ", slider[0].strftime('%d-%m-%Y')," - ", slider[1].strftime('%d-%m-%Y'))



df_volt = df[['Date', 'Ch 1195','Ch 1205','Ch 1215','Ch 1225']].set_index('Date')
ph_mean_volts=df_volt.groupby('Date',sort=False).mean()
st.markdown("### Phase wise mean volatge")
voltage=['Ch 1195','Ch 1205','Ch 1215','Ch 1225']
mean_fig = px.line(ph_mean_volts, y=voltage)
st.write(mean_fig)

# split_date_start =pd.Series(slider[0].strftime('%d-%m-%Y'))
# split_date_end = pd.Series(slider[1].strftime('%d-%m-%Y'))
# df = df[(df['Date'] <= split_date_end[0]) | (df['Date'] >= split_date_start[0])]
# st.write(df)








