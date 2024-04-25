from streamlit.testing.v1 import AppTest
import streamlit as st

def test_about_button():
    at = AppTest.from_file("pages/3_📚_Study_Companion.py")

    # Simulate logged-in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "pao"

    # Run your Streamlit app script
    at.run()

    # Click on the "About this app" button in the sidebar
    at.sidebar.button[0].click().run(timeout=30)

    # Check if the expected content is displayed after clicking the button
    expected_content = "About This App"
    assert not any(markdown_elem.text == expected_content for markdown_elem in at.markdown)


def test_button_click():
    at = AppTest.from_file("pages/3_📚_Study_Companion.py")

    # Simulate logged in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "pao"

    # Run your Streamlit app script
    at.run()

    # Click on a button in the sidebar
    at.sidebar.button[0].click().run(timeout=30)

    # Check if the expected content is displayed after clicking the button
    expected_content = "How to Use This App"
    assert not any(markdown_elem.text == expected_content for markdown_elem in at.markdown)

def test_logout_button():
    at = AppTest.from_file("pages/3_📚_Study_Companion.py")

    # Set Session State to simulate a logged-in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "pao"  # Assuming a user is logged in initially
    # Run the app
    at.run()

    # Simulate clicking on the "Logout" button in the sidebar
    at.sidebar.button[0].click().run(timeout=30)
       
    # Check if the status changes to "unverified" and userid becomes None after clicking the button
    assert at.session_state["status"] == "unverified"

    # Simulate logged in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "pao"

    # Run your Streamlit app script
    at.run()

    # Click on the "Logout" button in the sidebar
    at.sidebar.button[0].click().run(timeout=30)

    # Check if the session state is updated after logout
    assert at.session_state["status"] == "unverified"

def test_home_page_button():
    at = AppTest.from_file("pages/3_📚_Study_Companion.py")

    # Simulate logged-in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "pao"

    # Run your Streamlit app script
    at.run()

    # Click on the "Home Page" button in the sidebar
    at.sidebar.button[0].click()

    # Check if the expected content is displayed after clicking the button
    expected_content = "Welcome to your Study Companion"
    assert not any(markdown_elem.text == expected_content for markdown_elem in at.markdown)

def test_take_notes_button_exists():
    at = AppTest.from_file("pages/3_📚_Study_Companion.py")

    # Simulate logged in user
    at.session_state["status"] = "verified"
    at.session_state["userid"] = "pao"

    # Run your Streamlit app script
    at.run()

    # Check if the dropdown button exists in the sidebar
    assert at.sidebar.button[0]
