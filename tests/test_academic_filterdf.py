from pages._2_Academic_Advising import read_bigquery_table, filter_dataframe
import pandas as pd
from streamlit.testing.v1 import AppTest
import streamlit as st
import unittest
from unittest.mock import patch  

# Create a subclass of unittest.TestCase for testing
class TestAcademicAdvising(unittest.TestCase):

    # Test the filter_dataframe function
    def test_filter_dataframe(self):
        # Create a mock dataframe
        df = pd.DataFrame({'name': ['John', 'Jane'], 'age': [20, 25]})

        # Call the filter_dataframe function with the mock dataframe
        result = filter_dataframe(df)

        # Assert that the function returned the original dataframe (since no filters were applied)
        self.assertTrue(result.equals(df))



    # Test the read_bigquery_table function
    @patch('google.cloud.bigquery.Client')  # Patching the Client class
    def test_read_bigquery_table(self, mock_client):
        # Create a mock dataframe to return from the query job
        mock_dataframe = pd.DataFrame({'name': ['John', 'Jane'], 'age': [20, 25]})

        # Mock the query job to return the mock dataframe
        mock_query_job = mock_client.return_value.query.return_value
        mock_query_job.to_dataframe.return_value = mock_dataframe

        # Call the read_bigquery_table function with the mock project and table ID
        result = read_bigquery_table('my-project', 'my-table')

        # Assert that the function returned the mock dataframe
        self.assertTrue(result.equals(mock_dataframe))



def test_main():
    # Create an AppTest instance
    at = AppTest.from_file("pages/_2_Academic_Advising.py")

    # Set Session State to simulate a logged-in user
    at.session_state["status"] = "verified"
    at.session_state["edu_id"] = "joe"

    at.run()

    # # check if user gives in an input and receive's an output
    input_text, output_text = "What is the name of my college?", "Howard University"
    at.text_input[0].value == input_text
    at.text_input[0].set_value(output_text).run()
    assert at.text_input[0].value != input_text
    assert at.text_input[0].value == output_text


