from streamlit.testing.v1 import AppTest
import streamlit as st


def test_read_bigquery_table():
    at = AppTest.from_file("pages/2_👨‍💼_Academic_Advising.py")

    # Set Session State to simulate a logged-in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "joseph"  # Assuming a user is logged in initially

    # check if table is read into a dataframe
    expected_df = pd.DataFrame([1, 2, 3])
    assert at.dataframe[0].value.equals(expected_df)






def test_upload_button(): 
    at = AppTest.from_file("pages/2_👨‍💼_Academic_Advising.py")

    # Set Session State to simulate a logged-in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "joseph"

    # Run the app
    at.run()

    # check if upload button is clicked
    assert at.button[0].value == False
    at.button[0].click().run()
    assert at.button[0].value == True


def test_logout_button():
    at = AppTest.from_file("pages/2_👨‍💼_Academic_Advising.py")

    at.session_state["status"] = "verified"
    at.session_state["userid"] = "joseph"  # Assuming a user is logged in initially
    
    at.run()

    # Simulate clicking on the "Logout" button in the sidebar
    at.sidebar.button[0].click().run(timeout=20)
       
    # Check if the status changes to "unverified" and userid becomes None after clicking the button
    assert at.session_state["status"] == "unverified"


def test_input_output_text_from_genai():

    at = AppTest.from_file("pages/2_👨‍💼_Academic_Advising.py")

    at.session_state["status"] = "verified"
    at.session_state["userid"] = "joseph" 

    at.run()

    # check if user give in an input and receive's an output
    assert at.text_input[0].value == "What is the name of my college"
    at.text_input[0].set_value("Howard University").run()
