import streamlit as st

def is_verified():
  return st.session_state.status != "verified"