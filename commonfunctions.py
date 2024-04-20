import streamlit as st
from google.cloud import bigquery

#check is user has logged in
def is_verified():
  return st.session_state.status != "verified"

#get the curr username
def get_username():
  return st.session_state.edu_id

#logout function
def log_out():
  st.session_state.status = "unverified"