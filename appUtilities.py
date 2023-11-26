"""
Helper file to be called in the main streamlit app. 

Contains functions for slicing data & graphing
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import sys

# Generates today's date (returns string of YYYY-MM-DD by default)
def get_today(string=True):
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Slices a dataframe according to the given dates (inclusive)
def get_dates(df:pd.DataFrame, start_date:str, end_date:str, date_column:str='Date')->pd.DataFrame:
    return df[(df[date_column]>=start_date)&(df[date_column]<=end_date)]

# Get relevant data for that month
def get_month(df:pd.DataFrame, month):
    return df.loc[df.month==month]

# Get relevant data for that week
def get_week(df:pd.DataFrame, week:str):
    # Get the following week Monday's date. This will be a dt obj
    # week_end = datetime.datetime.strptime(week, '%Y-%m-%d') + datetime.timedelta(days=7)
    if datetime.datetime.strptime(week, '%Y-%m-%d').strftime("%a") != 'Mon':
        raise Exception(f"week of {week} was not a Monday")
    else:
        return df.loc[df.week_start==week]
