from google.cloud import bigquery
from dotenv import load_dotenv
import google.generativeai as genai
import os
import streamlit as st
import pandas as pd

st.write(
    """
    # Welcome to the Academic Advising Portal👨‍🔧!

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

uploaded_file = st.file_uploader("Study Material", type=None, accept_multiple_files=False, key=None, help="Make the file format is .csv", on_change=None, args=None, kwargs=None)

if uploaded_file is not None:
    # Read the file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)


    # Create a BigQuery client
    client = bigquery.Client()

    # Create a new dataset (if it doesn't already exist)
    dataset_id = "josephsankahtechx2024.checklist_dataset"
    dataset = bigquery.Dataset(dataset_id)
    #dataset = client.create_dataset(dataset)  # API request

    # Create a new table (if it doesn't already exist)
    table_id = "josephsankahtechx2024.checklist_dataset.checklist-template"
    table = bigquery.Table(dataset.table(table_id))
    # table = client.create_table(table)  # API request

    # Load the data from the DataFrame into the table
    job_config = bigquery.LoadJobConfig(schema=[
        bigquery.SchemaField("Number", "STRING"),
        bigquery.SchemaField("Course Title", "STRING"),
        bigquery.SchemaField("Grade", "STRING")
    ])
    job = client.load_table_from_dataframe(
        df, table, job_config=job_config
    )  # API request

    # Wait for the job to complete
    job.result()  # Waits for table load to complete.

    # Print a success message
    st.write("Data successfully uploaded to BigQuery.")

st.write(
    """
    ##### Enter your command...
    """
)

input_text = st.text_input("Input Text")

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



