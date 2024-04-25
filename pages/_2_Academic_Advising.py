from dotenv import load_dotenv
import google.auth.transport.requests
from google.cloud import bigquery
import google.generativeai as genai
import os
import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from commonfunctions import * 

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of the checklist dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

def read_bigquery_table(project, table_id):
    client = bigquery.Client(project=project)
    query_job = client.query(f"SELECT * FROM `{table_id}`")
    return query_job.to_dataframe()
 

def main():
    username = get_username()

    st.write(
        f"""
        # Welcome to the Academic Advising Portal, {username}👋!

        This resource streamlines and enhances the academic advising experience for students by 
        leveraging the power of generative AI and a user-friendly filter providing tailor-made guidance and advising based on 
        academic goals, history coupled with user interaction.
        """
    )

    st.write(
        """
        ## New to Academic Advising  🚀 ...
        - Enter in your college name.
        - Submit checklist populated with registered classes for the given semester.
        - Interact with chat bot to receive course recommendations and personalized guidance 😃!
        """
    )


    school_name = st.text_input(label="What college do you attend?")

    DATA_SET_ID = 'joemotatechx2024.checklist_dataset'
    uploaded_file = st.file_uploader("Cummulative checklist", type=None, accept_multiple_files=False, key=None, help="Make sure the file format is .csv", on_change=None, args=None, kwargs=None)

    if uploaded_file is not None:
        # Read the file into a Pandas DataFrame
        df = pd.read_csv(uploaded_file)
        #st.write(df)
        project = DATA_SET_ID.split('.')[0]
        client = bigquery.Client(project=project)


        # Initialize IDs
        table_id = f"{DATA_SET_ID}.{username}_checklist_template"

        # enable schema auto-detection 
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
        )

        #table = client.get_table(table_id)
        try:
            table = client.get_table(table_id)
        except Exception as e:
            table = bigquery.Table(table_id)

        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )  # Make an API request.
        job.result()  # Wait for the job to complete.

        table = client.get_table(table_id) # Make an API request
        try:
            df_from_bigquery = read_bigquery_table(project, table_id)
        except Exception as e:
            st.write("Read request from bigquery was not successful")
        else:
            st.write(df_from_bigquery)
            st.success('Read request to bigquery was successful!', icon="✅")

        st.write(
        """
        ##### Filter your checklist here:
        """
        )

        st.dataframe(filter_dataframe(df))

    input_text = st.text_input("Got any question on your checklist?")

    context = f"You are a helpful academic advisor for a student at {school_name}."

    if input_text:
        full_prompt = context + "\n\n" + input_text  # Combine context and input prompt
        response = generate_text_output(full_prompt)

        st.write(
        """
        ##### Your output...
        """)
        st.write(response)

if __name__ == "__main__":
    if is_verified():
        log_in_message()
        generate_image("Generate an image of an academic advisor")
    else:
        main()