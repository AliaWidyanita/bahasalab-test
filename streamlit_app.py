import streamlit as st
from query_processor import process_query

st.title("Travel Agency Chatbot")

query = st.text_input("Enter your question:")
if st.button("Submit"):
    response = process_query(query)
    st.write(response)