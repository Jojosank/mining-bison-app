from dotenv import load_dotenv
import google.auth.transport.requests
from google.cloud import bigquery
import google.generativeai as genai
import os
import streamlit as st
import pandas as pd
from commonfunctions import * 


def main():
    username = get_username()

    credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

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
        st.write(df)

        client = bigquery.Client(credentials=credentials, project=project)


        # Initialize IDs
        table_id = f"josephsankahtechx2024.checklist_dataset.{username}_checklist_template"

        # enable schema auto-detection 
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
        )

        try:
            table = client.get_table(table_id)
        except Exception as e:
            table = bigquery.Table(table_id)

        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )  # Make an API request.
        job.result()  # Wait for the job to complete.

        table = client.get_table(table_id) # Make an API request


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
    if is_verified():
        log_in_message()
        generate_image("Generate an image of an academic advisor")
    else:
        main()