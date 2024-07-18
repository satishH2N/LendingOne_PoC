import streamlit as st
import snowflake.connector
import pandas as pd
from datetime import date
import toml

# Load configuration
config = toml.load("config.toml")

def connect_to_snowflake():
    conn = snowflake.connector.connect(
        user=config['snowflake']['user'],
        password=config['snowflake']['password'],
        account=config['snowflake']['account'],
        warehouse=config['snowflake']['warehouse'],
        database=config['snowflake']['database'],
        schema=config['snowflake']['schema']
    )
    return conn

def insert_data_to_snowflake(account_type, account_code, date_of_entry, transaction_amount, entered_by):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    insert_query = f"""
    INSERT INTO FINANCE_METADATA (ACCOUNT_TYPE, ACCOUNT_CODE, DATE_OF_ENTRY, TRANSACTION_AMOUNT, ENTERED_BY)
    VALUES ('{account_type}', '{account_code}', '{date_of_entry}', {transaction_amount}, '{entered_by}');
    """
    cursor.execute(insert_query)
    conn.commit()
    cursor.close()
    conn.close()

def authenticate(username, password):
    return username == config['auth']['username'] and password == config['auth']['password']

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        st.sidebar.title("Menu")
        menu = ["Finance Metadata"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Finance Metadata":
            st.title("Finance Metadata Entry")

            account_type = st.selectbox("Account Type", ["Credit", "Debit"])
            account_code = st.text_input("Account Code")
            date_of_entry = st.date_input("Date of Entry", date.today())
            transaction_amount = st.number_input("Transaction Amount", min_value=0.0, format="%.2f")
            entered_by = st.text_input("Entered By")

            if st.button("Submit"):
                if account_code and date_of_entry and transaction_amount and entered_by:
                    insert_data_to_snowflake(account_type, account_code, date_of_entry, transaction_amount, entered_by)
                    st.success("Data submitted successfully")
                else:
                    st.error("Please fill all mandatory fields")

            if st.button("Clear All"):
                st.experimental_rerun()

            if st.button("Logout"):
                st.session_state.authenticated = False
                st.experimental_rerun()
    else:
        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Logged in as {}".format(username))
                st.experimental_rerun()
            else:
                st.error("Invalid Username/Password")

if __name__ == '__main__':
    main()
