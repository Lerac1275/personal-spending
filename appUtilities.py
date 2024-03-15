"""
Helper file to be called in the main streamlit app. 

Contains functions for slicing data & graphing
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import sys, pytz

def get_endoff_day():
    """
    Returns the datetime of the end of the CURRENT day. Intended to be used in the form < so this returns the start of the next day (from today)
    """
   # Get Singapore's timezone
    sg_timezone = pytz.timezone('Asia/Singapore')

    # Get the current date and time in Singapore's timezone
    current_date_sg = datetime.datetime.now(sg_timezone)

    return pd.to_datetime(current_date_sg.date() + pd.DateOffset(days=1))

def get_current_month():
    """
    Returns the first day of the CURRENT month (without timezone)
    """
    # Get Singapore's timezone
    sg_timezone = pytz.timezone('Asia/Singapore')

    # Get the current date and time in Singapore's timezone
    current_date_sg = datetime.datetime.now(sg_timezone)

    # Subtract n months from the current date
    n_months_ago = current_date_sg - pd.DateOffset(months=0)
    # Set the day of the resulting date to 1 to get the first day of the month
    n_months_ago = n_months_ago.replace(day=1).date()
    # Return datetime timestamp type
    return pd.to_datetime(n_months_ago)
    
# @st.cache_data(show_spinner=True)This cannot be styled
def create_main_table(df:pd.DataFrame, n_months = 4, reverse=False):
    """
    Displays the main landing page table, which is the spending by type for the last 4 months

    Parameters
    ----------
    df:pd.DataFrame
        Pandas dataframecontaining individual purchase records. 
    n_months: int
        number of months back to go
    reverse: bool, False by default
        Whether months are in DESCENDING order (from left to right). reverse=False means columns will for example be Jan, Feb, Mar, Apr. reverse=True means they will be Apr, Mar, Feb, Jan. Handles color reformatting as well. 
        
    """

    n_months = n_months-1 #since zero-indexed

    # Get Singapore's timezone
    sg_timezone = pytz.timezone('Asia/Singapore')

    # Get the current date and time in Singapore's timezone
    current_date_sg = datetime.datetime.now(sg_timezone)

    # Subtract n months from the current date
    n_months_ago = current_date_sg - pd.DateOffset(months=n_months)
    # Set the day of the resulting date to 1 to get the first day of the month
    n_months_ago = n_months_ago.replace(day=1).date()

    # filter entries between the last n_months and today's date
    tdf = df.loc[(df['Date']>= pd.to_datetime(n_months_ago))
                 & (df['Date'] <= get_endoff_day())].copy()
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
    tdf = pd.concat([tdf, pd.DataFrame(column_sums).T]) #Add the column sums so they appear at the top
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
                styles.append('background-color: blue')  # Same value

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

def pie_chart_most_recent(df:pd.DataFrame):
    """
    Makes a pie chart of spending for the most recent month
    """
    tdf = df.loc[(df.month>= get_current_month())
            & (df.Date<get_endoff_day())]
    tdf = tdf.groupby('Type').agg(
        total=pd.NamedAgg(column='Amount', aggfunc='sum')
    ).reset_index().sort_values(by='Type')

    # Create a donut chart using Plotly Graph Objects
    fig = go.Figure()
    values = tdf.total.values
    labels = tdf.Type.values
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,  # Set the hole parameter to create a donut chart
        marker=dict(colors=['red', 'green', 'blue', 'orange'])  # You can customize colors if needed
    ))
    total_spending = sum(values)
    fig.update_layout(
        # title='Donut Chart Example',
        annotations=[dict(text=f'${total_spending:,.0f}', x=0.5, y=0.5, font_size=20, showarrow=False)]
        , legend= dict(x = 0.3, y=-0.1, orientation='h')
    )

    return fig