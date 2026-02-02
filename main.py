import pandas as pd

data = [
    ["2026-01-01", "SKU1", "WarehouseA", "Inbound", 100],
    ["2026-01-03", "SKU1", "WarehouseA", "Consumption", -20],
    ["2026-01-05", "SKU1", "WarehouseB", "Inbound", 50]
]

df=pd.DataFrame(data, columns=["Date", "SKU", "Location", "Movement", "qty"])
df["Date"]=pd.to_datetime(df["Date"])

today = pd.Timestamp.today()
df["days_old"] = (today - df["Date"]).dt.days

def aging_bucket(days):
    if days <= 30:
        return "0-30"
    elif days <= 90:
        return "31-90"
    else:
        return "90+"

df["aging_bucket"] = df["days_old"].apply(aging_bucket)

import sqlite3

conn=sqlite3.connect("inventory.db")
df.to_sql("ledger", conn, if_exists="replace", index=False)
conn.close()

print("Database saved!")