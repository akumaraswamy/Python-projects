# -*- coding: utf-8 -*-
"""
Created on Tue May 30 23:40:29 2017

@author: aruna
"""

parse_dates = ['Dates']
print 'Loading timeData.csv - please wait'
time_data_df = pd.read_csv('../data/timeData2.csv', parse_dates=parse_dates)
time_data_df['Dates'] = pd.DatetimeIndex(time_data_df['Dates'])
print 'Loading completed'
time_data_df.set_index(keys='Dates', inplace=True)
print '\nIndex:', type(time_data_df.index)
start = datetime.time(22,00,0)
end = datetime.time(23,55,0)
filtered_df = time_data_df.between_time(start,end)
filtered_df['Category'].unique()
