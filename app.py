# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

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

refresh_data = st.button(label="Refresh Raw Data", type='primary')
if refresh_data:
    st.session_state.input += 1

df = get_data(st.session_state.input)

df.to_pickle("./data/sample_data.pkl")

st.dataframe(df)
# st.dataframe(df.dtypes)

# Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")