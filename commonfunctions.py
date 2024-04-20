import streamlit as st
from google.cloud import bigquery

def is_verified():
  return st.session_state.status != "verified"