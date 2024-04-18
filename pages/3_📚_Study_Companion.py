import streamlit as st
from google.cloud import bigquery
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import pdfplumber
import io
import calendar
from datetime import datetime

client = bigquery.Client(project='paolaalvaradotechx2024')

# Define your dataset ID and table ID
dataset_id = 'notes_from_student'
table_id = 'notes'

def save_notes_to_bigquery(course_name, notes_content):
    # Get the current date
    current_date = datetime.now().date()

    # Create a dictionary to store the note data
    note_data = {
        "course_name": course_name,
        "notes_taken": notes_content,
        "date_created": current_date,
    }

    # Insert the note data into the BigQuery table
    try:
        table_ref = client.dataset(dataset_id).table(table_id)
        table = client.get_table(table_ref)

        rows_to_insert = [note_data]
        errors = client.insert_rows(table, rows_to_insert)

        if errors == []:
            st.success("Notes saved successfully to BigQuery.")
        else:
            st.error(f"Failed to save notes: {errors}")
    except Exception as e:
        st.error(f"Error saving notes to BigQuery: {str(e)}")

def take_notes():

    # Input fields for course name and notes
    course_name = st.text_input("Enter your course name")
    notes_content = st.text_area("Enter your notes here")

    # Button to save notes
    if st.button("Save Notes"):
        # Validate inputs
        if not course_name or not notes_content:
            st.error("Please fill in all fields.")
            return

        # Save notes to BigQuery
        save_notes_to_bigquery(course_name, notes_content)

    st.sidebar.caption("Notes will be saved to BigQuery for future access.")

    genai.configure(api_key='AIzaSyCK-rU375-vmt4Th9hvfBhFXthGFNeuCUk')
    model = genai.GenerativeModel('gemini-pro')

        # Input field for user's question or input
    input_text = st.text_input("What is your question? ")

    if st.button("General Question"):
        # Call the AI function for general questions
        response = model.generate_content(input_text)
        st.markdown("## Response")
        st.write(response.text)

    if st.button("Summarize"):
        # Call the AI function to summarize input text
        summary = model.generate_content(input_text)
        st.markdown("## Summary")
        st.write(summary)

    if st.button("Make Quiz"):
        # Call the AI function to generate a quiz based on user input
        quiz_prompt = f"generate quiz for {input_text}"
        quiz = model.generate_content(quiz_prompt)
        st.markdown("## Quiz")
        st.write(quiz)

    if st.button("Make Notes"):
        # Call the AI function to generate notes
        notes = model.generate_content(input_text)
        st.markdown("## Notes")
        st.write(notes)


def main_page():
    
    # Input field for student's name
    student_name = st.sidebar.text_input("Enter your name", key="student_name_input")

    if student_name:
        st.session_state['student_name'] = student_name
        st.sidebar.success("Welcome!")

    image_url1 = "https://i.pinimg.com/474x/f5/48/5d/f5485d686f3913957ad6a3c3084b7db3.jpg"
        # Display the image using st.image
    st.sidebar.image(image_url1,)

    # Display the image using st.image
    image_url = "https://i.pinimg.com/564x/42/c0/2a/42c02af84fac1f5a1f4b36b46de807fd.jpg"
    st.image(image_url,)

    st.markdown("# Studio Ghibli Companion")
    st.sidebar.markdown(" ")

    # Button for "How to use this app?"
    how_to_button = st.button("How to use this app?", key="how_to_button")

    # Show "How to use this app?" content when the button is clicked
    if how_to_button:
        st.markdown("""
        Welcome to the Studio Ghibli Companion! This app is designed to help you manage your courses, homework, notes, and more in a user-friendly way. Here's how to get started:

        - **Home Page:** Start from the home page, where you'll find an overview of the app's features and a guide on how to use it effectively.
        - **Courses Page:** Click on the 'Courses' button to access your courses. Here, you can create new courses, upload syllabuses, and manage your course schedule.
        - **Creating a New Course:** Navigate to the 'Create Course' page. Enter the course name and description. Upload the course syllabus (PDF format). Click 'Create Course' to add it to your list of courses.
        - **Homework & Notes Page:** Use this page to upload and manage your homework assignments, notes, and other study materials.
        - **Calendar Integration:** Access your calendar to set important dates for your courses and assignments. This helps you stay organized and on track.
        - **AI-Powered Assistance:** Ask questions using the AI-powered content generator to get quick responses and assistance with your studies.
        - **Customize Your Experience:** Explore the sidebar for additional features and options tailored to your needs.
        """)
        # Button for "About this app"
    about_button = st.button("About this app", key="about_button")

    # Show "About this app" content when the button is clicked
    if about_button:
        st.markdown("""
        This notebook application’s purpose is to help the student by keeping them organized with their note-taking. They will be able to set their courses in these sections and in them will hold their notebook for that specific class.
        """)
    # selected_date = st.date_input("Select a date")

    # if selected_date:
    #     st.write(f"You selected: {selected_date}")

    # Display the calendar on the home page
   # display_calendar()

    # topics = ["", "Math", "Science", "History", "English", "Computer Science", "Art"]

    # if topics:
    # # Display the select box for choosing topics
    #     selected_topic = st.selectbox("Select a topic you need help with", topics)

    # # Display the selected topic
    # if selected_topic:
    #     st.write(f"You selected: {selected_topic}")

dataset_id = 'courses_created'
table_id = 'new_course'

if 'courses' not in st.session_state:
    st.session_state.courses = []

# Function to save new course to BigQuery
def get_courses_data():
    query = """
    SELECT * FROM `paolaalvaradotechx2024.courses_created.new_course`
    """
    result = client.query(query).result()

    courses_data = result.to_dataframe()

    st.dataframe(courses_data)

def save_course_to_bigquery(course_data):
    # Convert date to string format

    # Create a dictionary to store the course data
    course_row = {
        "course_name": course_data['course_name'],
        "description": course_data['description'],
    }

    # Insert the course data into the table
    rows_to_insert = [course_row]
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)
    errors = client.insert_rows(table, rows_to_insert)

    if errors:
        st.error(f"Failed to save course: {errors}")
    else:
        st.success("Course saved successfully.")
    
    
def create_course():
    st.markdown("# Create New Course")

    # Input fields for course details
    course_name = st.text_input("Enter course name")
    description = st.text_area("Enter course description")

    # Button to save the new course
    if st.button("Save Course"):

        # Validate inputs
        if not course_name or not description:
            st.error("Please fill in all fields.")
            return

        # Create a dictionary to store course data
        course_data = {
            "course_name": course_name,
            "description": description,
        }

        # Save the course data to BigQuery
        save_course_to_bigquery(course_data)

        # Add the new course to the session state
        st.session_state.courses.append(course_data)

def page2():
    st.markdown("# Courses")
    if not st.session_state['courses']:
        st.write("No courses created yet.")
    else:
        for course in st.session_state['courses']:
            if st.button(course['course_name']):
                st.write(f"**{course['course_name']}**")
                st.write(f"Description: {course['description']}")

# Function to save homework data to BigQuery including PDF files
dataset_id = 'homework_data'
table_id = 'homework_input'

def save_homework_to_bigquery(course_name, homework_content, due_date):
    # Create a dictionary to store the homework data
    homework_data = {
        "course_name": course_name,
        "homework_content": homework_content,
        "due_date": due_date,
    }

    # Insert the homework data into the BigQuery table
    try:
        table_ref = client.dataset(dataset_id).table(table_id)
        table = client.get_table(table_ref)

        rows_to_insert = [homework_data]
        errors = client.insert_rows(table, rows_to_insert)

        if errors == []:
            st.success("Homework saved successfully to BigQuery.")
        else:
            st.error(f"Failed to save homework: {errors}")
    except Exception as e:
        st.error(f"Error saving homework to BigQuery: {str(e)}")
def create_homework():
    st.markdown("# Create New Homework")

    # Input fields for homework details
    course_name = st.text_input("Enter course name")
    homework_content = st.text_area("Enter homework content")
    due_date = st.date_input("Select due date")

    # Button to save the new homework
    if st.button("Save Homework"):
        # Validate inputs
        if not course_name or not homework_content or not due_date:
            st.error("Please fill in all fields.")
            return

        # Save homework to BigQuery
        save_homework_to_bigquery(course_name, homework_content, due_date)

    # Input field for the prompt
    prompt = st.text_input("Enter a prompt to generate an image.")

    if st.button("Generate Image"):
        if prompt:
            # Initialize Vertex AI
            vertexai.init(project="paolaalvaradotechx2024", location="us-central1")
            # Load the Image Generation model
            model = ImageGenerationModel.from_pretrained("imagegeneration@005")
            # Generate images based on the user's prompt
            images = model.generate_images(prompt=prompt)

            if images:
                # Save the generated image to a file
                images[0].save(location="samplefile.jpg")
                # Display the generated image
                st.image("samplefile.jpg")

                # Add a download button to download the generated image
                st.download_button(label="Download Image", data="samplefile.jpg", file_name="generated_image.jpg")
        else:
            st.warning("Please enter a prompt to generate an image.")

def page3():
    st.markdown("# Homework")

    # Query BigQuery to get homework data
    query = f"""
    SELECT * FROM `paolaalvaradotechx2024.{dataset_id}.{table_id}`
    """
    homework_data = client.query(query).to_dataframe()

    # Display homework data in a table
    st.dataframe(homework_data)


def page4():

    st.markdown("# Your Notes")

    # Query BigQuery to get notes data
    query = """
    SELECT * FROM `paolaalvaradotechx2024.notes_from_student.notes`
    """
    notes_data = client.query(query).to_dataframe()

    # Display notes data in a table
    st.dataframe(notes_data)
    
    # Add sidebar content specific to page 3
    image_url = "https://i.pinimg.com/474x/e4/b5/29/e4b5297f5915b6b5434843864358e96c.jpg"
    st.sidebar.image(image_url,)
    st.sidebar.caption("Welcome to your notes page!")
    


page_names_to_funcs = {
    "Home Page": main_page,   
    "Courses": page2,
    "Homework": page3,
    "Notes": page4,
    "Create Course": create_course, 
    "Take Notes": take_notes, 
    "Create Homework": create_homework
}

# Set the default value for the selectbox to "Main Page"
selected_page = st.sidebar.selectbox(" ", page_names_to_funcs.keys(), index=0)

# Call the function corresponding to the selected page
page_names_to_funcs[selected_page]()

