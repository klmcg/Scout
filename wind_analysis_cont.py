#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 13:11:13 2018

@author: kmcg
"""
# import numpy and pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read the excel sheet using the sheetname and header at row 14
df_wind = pd.read_excel('SPP_wind data_20180309.xlsx', sheetname = 'Historical 8760s', header = 14)

# create empty vectors
output_years = []
output_months = []
output_days = []
output_hours = []
output_energy = []
output_price = []

# list the column headings that correspond to each column 
# (year, month, day, hour, hour, energy) and wether its 2015 (Year.2) or 2016 (Year.3)
years = ['Year.2','Year.3']
months = ['Month.2','Month.3']
days = ['Day.2','Day.3']
hours = ['(CST).2','(CST).3']
energy = ['Array (MWh).2','Array (MWh).3']

# create a for loop - still figuring out how this works
for i in years: 
    y_index = years.index(i)
    
    for j in range(0,len(df_wind)):
        y = df_wind.loc[j,years[y_index]]
        m = df_wind.loc[j,months[y_index]]
        d = df_wind.loc[j,days[y_index]]
        h = df_wind.loc[j,hours[y_index]]
        e = df_wind.loc[j,energy[y_index]]
        
        if y > 0:
            output_years = np.append(output_years,y)
            output_months = np.append(output_months,m)
            output_days = np.append(output_days,d)
            output_hours = np.append(output_hours,h)
            output_energy = np.append(output_energy,e)
                           
# stack the colums (put them next to each other)        
D = np.column_stack((output_years,output_months,output_days,output_hours,output_energy))

# create two colums of zeros
z = np.zeros((len(output_years),2))

# stack D and z
D2 = np.column_stack((D,z))

# create a new dataframe out of D2, with columns
df_new = pd.DataFrame(D2)        
df_new.columns = ['Year','Month','Day','Hour','Energy','Target','Difference'] 


# read the targets 
df_targets = pd.read_excel('hedge_targets.xlsx',sheetname='Sheet1',header=0)

# create empty vector
targets = []

# for loop determining which hours are onpeak/offpeak hours
for i in range(0,len(df_new)):
    m = df_new.loc[i,'Month']
    h = df_new.loc[i,'Hour']

    if h > 6 and h < 23:
        t = df_targets.loc[m-1,'Peak']
    
    else:
        t = df_targets.loc[m-1,'Offpeak']
    # identified target value to the 'Target' column
    df_new.loc[i,'Target'] = t
    # calculate the difference    
    df_new.loc[i,'Difference'] = df_new.loc[i,'Energy'] - df_new.loc[i,'Target']
    

# read data from excel, sheet 'Histroical LMP' and header 1
df_price = pd.read_excel('SPP_LMPs.xlsx', sheet_name = 'Historical LMP', header = 1)

# create empty vectors
output_hubreal = []
output_hubahead = []
output_nodereal = []
output_nodeahead = []

# pulls out and groups 2015 and 2016 data by type (hub/node, day-ahead/real)
# then converts this information from dataframe format to numerical 
# array using the .values command

hubreal = df_price[['SNL','SNL.4']].values
hubahead = df_price[['SNL.1','SNL.5']].values
nodereal = df_price[['SNL.2','SNL.6']].values
nodeahead = df_price[['SNL.3','SNL.7']].values
    
# create a for loop to fill the empty vectors with our price data 

# want to iterate through 2 columns (2015 and 2016) for each data type
for i in range(0,2):
    
    # go through every value in each year
    for j in range(0,len(hubreal)):
        
        # assigns value from hour j in column (year) i
        a = hubreal[j,i]
        b = hubahead[j,i]
        c = nodereal[j,i]
        d = nodeahead[j,i]
                      
        if np.isnan(a) == False:
            output_hubreal = np.append(output_hubreal,a)

        if np.isnan(b) == False:          
            output_hubahead = np.append(output_hubahead,b)
            
        if np.isnan(c) == False:          
            output_nodereal = np.append(output_nodereal,c)

        if np.isnan(d) == False:          
            output_nodeahead = np.append(output_nodeahead,d)
            
D3 = np.column_stack((output_hubreal,output_hubreal,output_nodereal,output_nodeahead))

df_new2 = pd.DataFrame(D3)

df_new2.columns = ['Hub Real Time Price','Hub Day Ahead Price','Node Real Time Price','Node Day Ahead Price']


energyprice = pd.concat([df_new, df_new2], axis=1, join_axes=[df_new.index])


for i in range(0,len(energyprice)):
    energyprice.loc[i,'Hub Real Time Profit'] = energyprice.loc[i,'Difference'] * energyprice.loc[i,'Hub Real Time Price']
    energyprice.loc[i,'Hub Day Ahead Profit'] = energyprice.loc[i,'Difference'] * energyprice.loc[i,'Hub Day Ahead Price']
    energyprice.loc[i,'Node Real Time Profit'] = energyprice.loc[i,'Difference'] * energyprice.loc[i,'Node Real Time Price']
    energyprice.loc[i,'Node Day Ahead Profit'] = energyprice.loc[i,'Difference'] * energyprice.loc[i,'Node Day Ahead Price']


set1 = energyprice[['Energy', 'Hub Real Time Profit']].copy()
ax1 = energyprice.plot.scatter(x='Energy',
                               y='Hub Real Time Profit',
                               c='DarkBlue')
hist1 = set1.hist(column='Hub Real Time Profit', bins=500)


set2 = energyprice[['Energy', 'Hub Day Ahead Profit']].copy()

set3 = energyprice[['Energy', 'Node Real Time Profit']].copy()

set4 = energyprice[['Energy', 'Node Day Ahead Profit']].copy()







#df_newnew.to_excel('new1516_df.xlsx')          