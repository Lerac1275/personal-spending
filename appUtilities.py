"""
Helper file to be called in the main streamlit app. 

Contains functions for slicing data & graphing
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import sys, pytz

# Generates today's date (returns string of YYYY-MM-DD by default)
def get_today(string=True):
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Slices a dataframe according to the given dates (inclusive)
def get_dates(df:pd.DataFrame, start_date:str, end_date:str, date_column:str='Date')->pd.DataFrame:
    return df[(df[date_column]>=start_date)&(df[date_column]<=end_date)]

# Get relevant data for that week
def get_week(df:pd.DataFrame, week:str):
    # Get the following week Monday's date. This will be a dt obj
    # week_end = datetime.datetime.strptime(week, '%Y-%m-%d') + datetime.timedelta(days=7)
    if datetime.datetime.strptime(week, '%Y-%m-%d').strftime("%a") != 'Mon':
        raise Exception(f"week of {week} was not a Monday")
    else:
        return df.loc[df.week_start==week]
    

def create_main_table(df:pd.DataFrame, n_months = 4, reverse=False):
    """
    Displays the main landing page table, which is the spending by type for the last 4 months
    """
    # Get Singapore's timezone
    sg_timezone = pytz.timezone('Asia/Singapore')

    # Get the current date and time in Singapore's timezone
    current_date_sg = datetime.datetime.now(sg_timezone)

    # Subtract n months from the current date
    n_months_ago = current_date_sg - pd.DateOffset(months=n_months)
    # Set the day of the resulting date to 1 to get the first day of the month
    n_months_ago = n_months_ago.replace(day=1).date()

    # filter entries
    tdf = df.loc[df['Date']>= pd.to_datetime(n_months_ago)].copy()
    # Group by month & type
    tdf = tdf.groupby(['month', 'Type']).Amount.sum()
    # Pivot long to wide
    tdf = tdf.unstack(level=0)
    # Reset the name
    # tdf.columns.name = None
    # Sum values for each column
    column_sums = tdf.sum()
    column_sums.name = "Total" # Set the name of the series
    # Append sums as a new row to the DataFrame
    tdf = pd.concat([pd.DataFrame(column_sums).T, tdf]) #Add the column sums so they appear at the top
    # Set the index name
    tdf.index.name = "Type"
    # Change the date columns
    tdf.columns =  [pd.to_datetime(col).strftime("%b'%y") for col in tdf.columns.values]
    # Fill in missing values
    tdf = tdf.fillna(0)
    # Reverse the columns
    if reverse:
        tdf = tdf[tdf.columns[::-1]]

    # Define custom styling function
    def highlight_left(s):
        styles = []
        for i in range(1, len(s)):
            # print(s)
            if s[i] > s[i - 1]: # More than the previous cell
                styles.append(f'background-color: {"red" if not reverse else "green"}')
            elif s[i] < s[i - 1]:
                styles.append(f'background-color: {"green" if not reverse else "red"}')
            else:
                styles.append('background-color: blue, ')  # Same value

        if reverse:
            styles.append('background-color: grey')
        else:
        # First column should be grey
            styles.insert(0, 'background-color: grey')
        return styles

    # Apply custom styling function to DataFrame. axis=1 indicates to feed in the data row-wise 
    styled_df = tdf.style.format("${:,.2f}").apply(highlight_left, axis = 1)
    # Display styled DataFrame
    return styled_df