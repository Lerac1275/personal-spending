# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="Combined",
    ttl="10m", # Cache will expire in 10 minutes
    usecols=[0, 2, 3, 4, 5, 6, 7, 8, 9],
    # nrows=3,
)

df.to_pickle("./data/sample_data.pkl")

st.dataframe(df)
# st.dataframe(df.dtypes)

# Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")