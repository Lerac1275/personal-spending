"""
Helper file to be called in the main streamlit app. 

Contains functions for slicing data & graphing
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys

# Slices a dataframe according to the given dates (inclusive)
def get_dates(df:pd.DataFrame, start_date, end_date, date_column:str='Date')->pd.DataFrame:
    return df[(df[date_column]>=start_date)&(df[date_column]<=end_date)]