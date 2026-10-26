import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Finance Tracker")
st.write("Manage your money smartly!")

if "transactions" not in st.session_state:
    st.session_state.transactions = []

st.subheader("➕ Add Transaction")

with st.form("transaction_form"):
    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=1.0,
        step=100.0
    )

    category = st.selectbox(
        "Category",
        ["Pocket Money", "Food", "Travel",
         "Shopping", "Education", "Other"]
    )

    description = st.text_input("Description")

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        st.session_state.transactions.append({
            "Type": transaction_type,
            "Amount": amount,
            "Category": category,
            "Description": description
        })
        st.success("Transaction added!")

df = pd.DataFrame(st.session_state.transactions)

if not df.empty:
    income = df.loc[df["Type"] == "Income", "Amount"].sum()
    expenses = df.loc[df["Type"] == "Expense", "Amount"].sum()
else:
    income = 0
    expenses = 0

balance = income - expenses

st.subheader("📊 Financial Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("💵 Total Income", f"₹{income:,.2f}")
col2.metric("💸 Total Expenses", f"₹{expenses:,.2f}")
col3.metric("💰 Balance", f"₹{balance:,.2f}")

st.subheader("📋 Transaction History")

if not df.empty:
    st.dataframe(df, use_container_width=True)

    expense_df = df[df["Type"] == "Expense"]

    if not expense_df.empty:
        st.subheader("📈 Expense Breakdown")
        st.bar_chart(
            expense_df.groupby("Category")["Amount"].sum()
        )
else:
    st.info("Add your first transaction to get started!")