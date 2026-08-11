import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

def create_connection():
    conn = sqlite3.connect('expenses.db', check_same_thread=False)
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()

conn = create_connection()
create_table(conn)

st.title("💰 Expense Tracker")

with st.form("expense_form"):
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Shopping", "Other"])
    description = st.text_input("Description (optional)")
    expense_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
            (amount, category, description, str(expense_date))
        )
        conn.commit()
        st.success("Expense added!")

df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
st.subheader("All Expenses")
st.dataframe(df)

if not df.empty:
    st.subheader("Spending by Category")
    st.bar_chart(df.groupby("category")["amount"].sum())
