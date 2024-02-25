# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import appUtilities as au

@st.cache_data()
def dummy_data(): # A helper function for prototyping, reads in a dummy dataframe to avoid having to re-pull data during prototyping
    return pd.read_pickle('./data/dummy_data.pkl')

@st.cache_data #input is a placeholder to be used when we want to re-pull data
def get_data(input):
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.read(
        worksheet="Combined",
        ttl="0m", # Cache will expire in o minutes
        usecols=[0, 2, 3, 4, 5, 6, 7, 8, 9],
        # nrows=3,
    )
    # Remove NA rows
    df = df.loc[~df.Date.isna()]
    # Convert to date type
    df.Date=pd.to_datetime(df.Date)
    # Add the month
    df['month']=df['Date'].to_numpy().astype('datetime64[M]')
    # Add the week (start of the week is every monday)
    df['week_start'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
    return df

if "input" not in st.session_state:
    st.session_state['input']=1
# Ensures that data is only pulled from google API when the button is clicked (aside from when the app is first run. )
refresh_data = st.button(label="Refresh Raw Data", type='primary')
if refresh_data:
    st.session_state.input += 1

# df = get_data(st.session_state.input) #Uncomment this to pull the real data from google sheet
df = dummy_data()

# df.to_pickle("./data/dummy_data.pkl")

st.dataframe(df)
st.dataframe(df.dtypes)

styled_df = au.create_main_table(df=df, reverse=False)
st.dataframe(styled_df)

# Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")