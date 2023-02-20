import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from pylab import *
import statistics as stat
raw_data=pd.read_csv(r'/Users/aarush/Downloads/pollution project/pollution_us_2000_2016.csv')
print(raw_data.dtypes)
print(raw_data.info())

# Removing all the unnecessary columns
data = raw_data.drop(['Unnamed: 0','State Code','County Code','Site Num','Address','NO2 Units','O3 Units','SO2 Units','CO Units'],axis=1)
print(data.head)
#checking for missing values (NAs)
print(data.isnull().sum())

#Droping missing values
data1 =  data.dropna(axis=0) 

#Removing Duplicates
data_no_dupl = data1.drop_duplicates()
data_no_duplindex_col=0

#Checking for outliers
#Viewing the values of each NO2 AQI, O3 AQI,SO2 AQI and CO AQI to spot potential outliers
# Show all distribution plots simultaneously in four subplots 

sb.set(rc={"figure.figsize": (15, 10)})

subplot(2,2,1)
ax = sb.kdeplot(data_no_dupl['CO AQI'],fill=True, color= "red")

subplot(2,2,2)
ax = sb.kdeplot(data_no_dupl['SO2 AQI'], fill=True, color= "red")

subplot(2,2,3)
ax = sb.kdeplot(data_no_dupl['NO2 AQI'], fill=True, color= "red")

subplot(2,2,4)
ax = sb.kdeplot(data_no_dupl['O3 AQI'], fill=True, color= "red")

plt.show() 

#checking for mistakes in individual variables

# 1.State
print(data_no_dupl['State'].unique())

#Removing all rows containg string 'Country of Mexico' in coloumn 'state'
data_clean1 = data_no_dupl[~data_no_dupl.State.str.contains("Country Of Mexico")]

# 2.City
print(data_clean1['City'].unique())

# 3. Date Local 
# Convert Date Local to date format and extract year and month
import datetime as dt

# making copy of the data first to avoid error
data_clean1 = data_clean1[data_clean1['Date Local'].notnull()].copy()
data_clean1['Year_Month'] = pd.to_datetime(data_clean1['Date Local']).dt.strftime('%Y-%m') #Year-Month
data_clean1['Year'] = pd.to_datetime(data_clean1['Date Local']).dt.strftime('%Y') #Year
data_clean1['Month'] = pd.to_datetime(data_clean1['Date Local']).dt.strftime('%m') #Year

# Focusing on California, Since California is the most Polluted State
# Analysis : Air Quality (AQI) development over time in California

# Taking the AQI index of all four air pollution categories

# create sub data set with relevant variables only
pollution_df = data_clean1[['Year_Month','Year','Month','State','City','NO2 AQI','O3 AQI','SO2 AQI','CO AQI']]

#Selecting California entries only 
pollution_CA = pollution_df [pollution_df['State'] == 'California'].reset_index(drop=True)
print(pollution_CA.head())

# For better handling and to prevent data size exceeding plotly data limit, select only 10% of the California data.

CA_10per = pollution_CA.sample(frac=0.5)
CA_10per = CA_10per.sort_values('Year_Month').reset_index(drop=True)

#import chart_studio.tools as tls
import chart_studio.plotly as pl
import plotly.graph_objects as go


#Distribution of AQI values per AQI category in California

# Create two new pd data frames
AQI_time= CA_10per[['Year_Month','NO2 AQI','O3 AQI','SO2 AQI','CO AQI']] # all four AQIs incl. date
AQI = AQI_time.iloc[:,1:]  # all four AQIs only

#Subplots for each AQI category over time
fig, (ax1, ax2,ax3,ax4) = plt.subplots(4,1, figsize = (25,25)) 
fig.subplots_adjust(left=0.0, bottom=0.2)
for ax in ax1, ax2,ax3,ax4:
    ax.set(xlabel='Date')
    ax.set(ylabel='Value')

ax1.bar(AQI_time['Year_Month'],AQI_time['CO AQI'], color = 'yellow')
ax1.set_title('CO AQI')
ax1.set_xticks(['2000-06','2001-06','2002-06','2003-06','2004-06','2005-06','2006-06','2007-06','2008-06','2009-06','2010-06','2011-06', '2012-06','2013-06','2014-06','2015-06','2016-06']) 

ax2.bar(AQI_time['Year_Month'], AQI_time['SO2 AQI'], color = 'green')
ax2.set_title('SO2 AQI')
ax2.set_xticks(['2000-06','2001-06','2002-06','2003-06','2004-06','2005-06','2006-06','2007-06','2008-06','2009-06','2010-06','2011-06', '2012-06','2013-06','2014-06','2015-06','2016-06']) 

ax3.bar(AQI_time['Year_Month'],AQI_time['NO2 AQI'], color = 'red')
ax3.set_title('NO2 AQI')
ax3.set_xticks(['2000-06','2001-06','2002-06','2003-06','2004-06','2005-06','2006-06','2007-06','2008-06','2009-06','2010-06','2011-06', '2012-06','2013-06','2014-06','2015-06','2016-06']) 

ax4.bar(AQI_time['Year_Month'],AQI_time['O3 AQI'], color = 'blue')
ax4.set_title('O3 AQI')
ax4.set_xticks(['2000-06','2001-06','2002-06','2003-06','2004-06','2005-06','2006-06','2007-06','2008-06','2009-06','2010-06','2011-06', '2012-06','2013-06','2014-06','2015-06','2016-06']) 

plt.show() 

# working with the monthly average AQI values

# 1.Basic line chart with monthly mean values for each AQI category

AQI_time_grouped =AQI_time.groupby(['Year_Month']).mean().plot()

# 2. Interactive scatter plot with several monthly records for each AQI category
fig = go.Figure()
fig.add_trace(go.Scatter(x=CA_10per['Year_Month'], y=CA_10per['NO2 AQI'],
                    mode='lines', name='NO2 AQI', opacity=0.7))
fig.add_trace(go.Scatter(x=CA_10per['Year_Month'], y=CA_10per['O3 AQI'],
                    mode='lines', name='O3 AQI', opacity=0.7))
fig.add_trace(go.Scatter(x=CA_10per['Year_Month'], y=CA_10per['SO2 AQI'],
                    mode='lines', name='SO2 AQI', opacity=1.0))
fig.add_trace(go.Scatter(x=CA_10per['Year_Month'], y=CA_10per['CO AQI'],
                    mode='markers', name='CO AQI', opacity=0.6))
fig.update_layout(legend_title_text = "AQI categories",
                  title='AQI categories 2000-2010')
fig.update_yaxes(title_text="Value (in PPM/PPB)")
fig.update_xaxes(title_text="Time")
fig.show()