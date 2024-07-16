import streamlit as st
from auth import authenticate
from database import insert_finance_metadata

# Authenticate the user
if authenticate():
    st.sidebar.title("Menu")
    menu = ["Finance Metadata"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Finance Metadata":
        st.title("Finance Metadata Entry")

        with st.form(key='finance_metadata_form'):
            account_type = st.selectbox("Account Type", ["Credit", "Debit"], key="account_type")
            account_code = st.text_input("Account Code", key="account_code")
            date_of_entry = st.date_input("Date of Entry", key="date_of_entry")
            transaction_amount = st.number_input("Transaction Amount", format="%.2f", key="transaction_amount")
            entered_by = st.text_input("Entered By", key="entered_by")

            submit_button = st.form_submit_button(label="Submit")
            clear_button = st.form_submit_button(label="Clear All")

            if submit_button:
                if account_code and date_of_entry and transaction_amount and entered_by:
                    insert_finance_metadata(account_type, account_code, date_of_entry, transaction_amount, entered_by)
                    st.success("Data submitted successfully!")
                else:
                    st.error("Please fill all the mandatory fields.")
            elif clear_button:
                st.session_state["account_type"] = "Credit"
                st.session_state["account_code"] = ""
                st.session_state["date_of_entry"] = None
                st.session_state["transaction_amount"] = 0.0
                st.session_state["entered_by"] = ""
