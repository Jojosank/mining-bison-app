
from streamlit.testing.v1 import AppTest
import streamlit as st
import random

def test_no_bookname():
    # Initialize app
    at = AppTest.from_file("pages/1_👨‍🏫_Storybook.py")

    # Set Session State to simulate a logged-in user
    at.session_state["status"] = "verified"
    at.session_state["edu_id"] = "joe"

    # Run the app
    at.run()

    #test if warning appears
    assert len(at.warning) != 0

def test_generate_story_button():
    # Initialize app
    at = AppTest.from_file("pages/1_👨‍🏫_Storybook.py")

    # Set Session State to simulate a logged-in user
    at.session_state["status"] = "verified"
    at.session_state["edu_id"] = "joe"

    at.run()

    #generate random due to not being allowed duplicates if it fails its due to this make a duplicate
    name = str(random.randint(1, 100))

    #generate random due to not being allowed duplicates
    at.text_input[0].input(name).run()

    at.selectbox[0].select("Social Studies/History").run()

    at.selectbox[1].select("2nd Grade").run()

    at.text_area[0].input("Make sure to make the story about the history of trucks in the United States.").run()

    at.button[0].click().run(timeout=30)

    assert at.success[0].value == "Storybook generated successfully!"

def test_logout_button():
    at = AppTest.from_file("pages/1_👨‍🏫_Storybook.py")

    # Set Session State to simulate a logged-in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "joe"  # Assuming a user is logged in initially
    # Run the app
    at.run()

    # Simulate clicking on the "Logout" button in the sidebar
    at.sidebar.button[0].click().run(timeout=30)
       
    # Check if the status changes to "unverified" and userid becomes None after clicking the button
    assert at.session_state["status"] == "unverified"
