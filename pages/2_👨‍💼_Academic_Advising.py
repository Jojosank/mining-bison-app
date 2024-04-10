from dotenv import load_dotenv
import google.generativeai as genai
import os
import streamlit as st


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


input_type = st.selectbox("What kind of help do you need?",
                              ['Subject Help', 'Exam Preparation', 'Assignment Review', 'Study Techniques', 'Project Assistance', 'Career Guidance'],
                              help="""Can’t find your need in the list?""")

st.write(
    """
    ##### Upload Study Material Here
    """
)

st.file_uploader("Study Material", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)

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



