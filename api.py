from flask import Flask, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return "API Running"

@app.route("/snapshot")
def snapshot():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql("SELECT * FROM ledger", conn)
    conn.close()

    result=df.groupby(["SKU", "Location"])["qty"].sum().reset_index()
    
    return result.to_json(orient="records")

app.run(debug=True)
