import streamlit as st
import streamlit_authenticator as stauth

def authenticate():
    names = ["Avesh Nagauri", "Harshada Menewar", "Sangram Birje"]
    usernames = ["avesh", "harshada", "sangram"]
    passwords = ["123", "456", "789"]

    hashed_passwords = stauth.Hasher(passwords).generate()

    authenticator = stauth.Authenticate(
        names, 
        usernames, 
        hashed_passwords, 
        "some_cookie_name", 
        "some_signature_key",
        cookie_expiry_days=30  # Adjust this as needed
    )

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        st.success(f"Welcome {name}")
        return True
    elif authentication_status == False:
        st.error("Username/password is incorrect")
        return False
    elif authentication_status == None:
        st.warning("Please enter your username and password")
        return False

    return False
