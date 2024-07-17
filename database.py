import snowflake.connector
import streamlit as st

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user='anagauri',
        password='Beskos3421@',
        account='dlb82371.us-east-1',
        warehouse='EDH_QUERY',
        database='ODS',
        schema='ODS_STREAMLIT'
    )
    return conn

def insert_finance_metadata(account_type, account_code, date_of_entry, transaction_amount, entered_by):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO ODS_STREAMLIT.FINANCE_METADATA (account_type, account_code, date_of_entry, transaction_amount, entered_by)
        VALUES (%s, %s, %s, %s, %s)
    """, (account_type, account_code, date_of_entry, transaction_amount, entered_by))
    conn.commit()
    cursor.close()
    conn.close()
