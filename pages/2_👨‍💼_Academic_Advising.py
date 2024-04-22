from commonfunctions import get_logged_in_username
from dotenv import load_dotenv
import google.auth.transport.requests
from google.cloud import bigquery
import google.generativeai as genai
import os
import streamlit as st
import pandas as pd
from commonfunctions import*

credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

def main():
    username = get_username()

    st.write(
        f"""
        # Welcome to the Academic Advising Portal, {username}👋!

        This resource streamlines and enhances the academic advising experience for students by 
        leveraging the power of generative AI with tailor-made guidance and advising based on 
        academic goals, history coupled with user interaction.
        """
    )

    st.write(
        """
        ## New to Academic Advising  🚀 ...

        - Submit checklist populated with registered classes for the given semester
        - Interact with chat bot to receive course recommendations and personalized guidance
        - Retrieve all chats from chat bot whenever you want to 😃!
        """
    )


    st.write(
        """
        ##### Upload Study Material Here
        """
    )

    uploaded_file = st.file_uploader("Study Material", type=None, accept_multiple_files=False, key=None, help="Make sure the file format is .csv", on_change=None, args=None, kwargs=None)

    if uploaded_file is not None:
        # Read the file into a Pandas DataFrame
        df = pd.read_csv(uploaded_file)


        # Create a BigQuery client
        client = bigquery.Client(credentials=credentials, project=project)

        # Initialize IDs
        dataset_id = "josephsankahtechx2024.checklist_dataset"
        table_id = "josephsankahtechx2024.checklist_dataset.checklist_template"


        # Get the Table object from the Dataset object
        table = client.get_table(table_id)

        errors = client.insert_rows_json(table_id, df.to_dict('records'))

        if errors == []:
            st.write("Data successfully uploaded to BigQuery.")


    input_text = st.text_input(label="Enter your genai query...")

    # Load environment variables from .env file
    load_dotenv()

    # Access the API key from the environment variables
    GENAI_API_KEY = os.getenv("GENAI_API_KEY")
    genai.configure(api_key=GENAI_API_KEY)

    model = genai.GenerativeModel('gemini-pro')

    if input_text:
        response = model.generate_content(input_text)

        st.write(
        """
        ##### Your output...
        """)
        st.write(response.text)

if __name__ == "__main__":
    if st.session_state.status != "verified":
        st.write("You need to log in first")
    else:
        main()