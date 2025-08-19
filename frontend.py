import streamlit as st
import requests

st.title("💪 SmartFit")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        response = requests.post("http://localhost:8000/auth/login", 
                               json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Logged in!")
            st.session_state['user_id'] = response.json()["user_id"]
        else:
            st.error("Login failed")
    except:
        st.error("Can't connect to server")

if 'user_id' in st.session_state:
    st.write("Ask your fitness question:")
    question = st.text_input("Question")
    
    if st.button("Ask"):
        try:
            chat_response = requests.post("http://localhost:8000/chat/ask",
                                        json={"user_id": st.session_state['user_id'], 
                                             "message": question})
            if chat_response.status_code == 200:
                st.write(chat_response.json()["response"])
        except:
            st.error("Error getting response")
