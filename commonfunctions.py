import streamlit as st
from google.cloud import bigquery

def is_verified():
  return st.session_state.status != "verified"

#grab user name thats logged in
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

#update logout info
def update_logout_status(username):
    """
    Updates the login status to 'NO' for the given username.

    Args:
    - username (str): The username for which the login status should be updated.
    """
    client = bigquery.Client('joemotatechx2024')

    update_query = f"""
        UPDATE `joemotatechx2024.user_data.user_login`
        SET logged_in = 'NO'
        WHERE username = @username
    """
    update_job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username)
        ]
    )
    client.query(update_query, job_config=update_job_config)

    query_job = client.query(update_query)