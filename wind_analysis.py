# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Kennedy, I'm going to comment a lot of the code here initially. Typically I wouldn't have this much
# description. As you get more confident, I'll do it less. 

# this imports the library called pandas, which has lots of useful functions for reading
# and writing data to files. I've also set it up so that throughout the script, whenever
# we need to refer to pandas (e.g., call a function from that library), the prefix is now
# 'pd' instead of 'pandas' (so, a little shorter for convenience)
import pandas as pd

# this imports the library called numpy, which has lots of useful mathematical and statistical 
# functions. I've also set it up with an abbreviated reference, 'np'. 
import numpy as np

# first I'll read in the hourly wind data from an excel file using a function from the 
# pandas library

# read_excel is the name of the function. I specify the file name, the sheetname, and what line 
# I want to be the column headers. I chose 14, which is technically the 15th row of the Excel file. 
# Remember, Python indexes starting with 0. So 0,1,2,...14 gives me the 15th row.
df_wind = pd.read_excel('SPP_wind data_20180309.xlsx', sheetname = 'Historical 8760s', header = 14)

# create some empty vectors 
output_years = []
output_months = []
output_days = []
output_hours = []
output_energy = []

# list the column headings that correspond to each year. This part is a little funny because of the
# way the Excel file was set up. There were 4 separate columns called 'Year', so pandas kind of
# renames them to keep track of which is which. You can see the data and column headings if you
# write 'df_wind' in the console (bottom left quadrant of your screen in Spyder)

years = ['Year','Year.1','Year.2','Year.3']

# similarly, I'm going to keep track of what pandas named other columns for categories we're interested in
months = ['Month','Month.1','Month.2','Month.3']
days = ['Day','Day.1','Day.2','Day.3']
hours = ['(CST)','(CST).1','(CST).2','(CST).3']
energy = ['Array (MWh)','Array (MWh).1','Array (MWh).2','Array (MWh).3']

# length of the variable 'years', gives us num_years = 4
num_years = len(years)

# 'for' loop to consider each year, one at a time
# i takes the value of a member of the list years (defined above); first i = 'Year', then 'Year.1', etc.
for i in years: # note the syntax; in python 'if' statements and 'for' loops are initiated with a colon

    # this keeps track of what # year we are on, by finding the location of 'i' within the list years
    # when i = 'Year', y_index = 0; when i = 'Year.1', y_index = 1; etc.
    y_index = years.index(i)

    
    # now we want to "nest" another for loop. can think about this like big and little hands of a clock. 
    # the inner loop is the minute hand, the outer loop is the hour hand. 
    
    # another python syntax rule: you need to indent the contents of an if statement/for loop
       
    # go through every hour in every year (i.e., iterate through the length of our dataframe table)   
    # here the value of j iterates through the set (0,1,...,8783). the 'range' function
    # is useful for creating sets of numbers. you specify the first number, and the last, and 
    # it creates a set of all numbers between them except for the last one.
    for j in range(0,len(df_wind)):
        
        # identify the corresponding year, month, day, hour and wind energy value 
        # associated with each row
        
        # note the .loc convention; you have to use this when identifying the element of a dataframe
        # if we were just pulling out an element of a 2D array, we would not need the .loc
        y = df_wind.loc[j,years[y_index]]
        m = df_wind.loc[j,months[y_index]]
        d = df_wind.loc[j,days[y_index]]
        h = df_wind.loc[j,hours[y_index]]
        e = df_wind.loc[j,energy[y_index]]

        # make sure there is real data there. if y < 0, it means that the year is <= 0
        # so we know not to proceed
        
        if y > 0:
            
            # if there is real data there, add each new data point to its respective vector
            # the .append function in the numpy (np) library allows you to add one data point
            # at a time to a vector. you specify the vector first, then the point to be added
            output_years = np.append(output_years,y)
            output_months = np.append(output_months,m)
            output_days = np.append(output_days,d)
            output_hours = np.append(output_hours,h)
            output_energy = np.append(output_energy,e)

# now we want to push those five vectors together to get one matrix. you can do this using the
# .column_stack function in numpy
D = np.column_stack((output_years,output_months,output_days,output_hours,output_energy))

# now let's add two more columns, all of zeros; these are just placeholders, we'll use them later
# the .zeros function in numpy creates an array of zeros of a specified shape
z = np.zeros((len(output_years),2))

D2 = np.column_stack((D,z))
            
# right now, the data matrix in a numerical array. let's turn it into a dataframe and add column headings
df_new = pd.DataFrame(D2)        
df_new.columns = ['Year','Month','Day','Hour','Energy','Target','Difference'] # note that .columns is a function of all data frames      

# at this point, we've extracted out all the wind power data we need, and it's organized in one
# long time series. I think that will make it easier to deal with. 

# next we want to find out if wind power production in each hour is above/below the target
# to do that, I would suggest creating another column in the dataframe that tells us what the target is for each hour

# let's start by uploading the target data. I'm going to cheat a little here, by using a different spreadsheet 
# than the one that currently stores that information

df_targets = pd.read_excel('hedge_targets.xlsx',sheetname='Sheet1',header=0)

# now let's go hour by hour through the historical wind data, and identify what the target is

# peak hours = 7 - 22
# offpeak hours = 0 - 6, 23

# create empty array for our results
targets = []

for i in range(0,len(df_new)):
    
    # what month is it?
    m = df_new.loc[i,'Month']
    
    # what hour is it?
    h = df_new.loc[i,'Hour']
    
    # if it's a peak hour
    if h > 6 and h < 23:
        
        # this assigns to the variable t, the peak value for month m (in row m-1 of df_targets)        
        t = df_targets.loc[m-1,'Peak']
    
    # if it's an offpeak hour
    else:
        
        # this assigns to the variable t, the offpeak value for month m (in row m-1 of df_targets)        
        t = df_targets.loc[m-1,'Offpeak']
    
    # assigns the identified target value to the 'Target' column
    df_new.loc[i,'Target'] = t
    
    # calculates the difference between actual generation and the target, and then stores
    # that value in the 'Difference' column
    df_new.loc[i,'Difference'] = df_new.loc[i,'Energy'] - df_new.loc[i,'Target']

# we can write the new dataframe to Excel to see what it looks like
df_new.to_excel('new_df.xlsx') # note that .to_excel is a function of all data frames



