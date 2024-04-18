import streamlit as st
from google.cloud import bigquery

def is_verified():
  return st.session_state.status != "verified"

#grab user name
def get_logged_in_username():
    client = bigquery.Client('joemotatechx2024')

    # Query user_login table to find the logged-in user
    query = """
    SELECT username
    FROM joemotatechx2024.user_data.user_login
    WHERE logged_in = 'YES'
    """

    # Execute the query
    query_job = client.query(query)

    # Fetch the result
    result = query_job.result()

    # Extract the username
    for row in result:
        username = row.username
        return username

    return None  # Return None if no logged-in user is found