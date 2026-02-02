import streamlit as st
import pandas as pd
import sqlite3

st.title("Inventory Dashboard")

conn = sqlite3.connect("inventory.db")
df = pd.read_sql("SELECT * FROM ledger", conn)
conn.close()

st.dataframe(df)

st.metric("Total Records", len(df))
st.metric("Total Quantity", df["qty"].sum())
st.bar_chart(df.groupby("SKU")["qty"].sum())
st.subheader("Aging Data")
st.dataframe(df[["SKU","days_old","aging_bucket"]])