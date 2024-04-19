import streamlit as st
import commonfunctions
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import pdfplumber
import io
from commonfunctions import is_verified, update_logout_status, get_logged_in_username

def main():
    if 'courses' not in st.session_state:
        st.session_state['courses'] = []

    def main_page():
        image_url1 = "https://i.pinimg.com/474x/f5/48/5d/f5485d686f3913957ad6a3c3084b7db3.jpg"
        # Display the image using st.image
        st.sidebar.image(image_url1,)


        # Display the image using st.image
        image_url = "https://i.pinimg.com/564x/42/c0/2a/42c02af84fac1f5a1f4b36b46de807fd.jpg"
        st.image(image_url,)

        st.markdown("# Studio Ghibli Companion")
        st.sidebar.markdown(" ")
        # Add sidebar content specific to the main page

        st.caption("How to use this app!")
        # Caption for the button
        button_caption = "Welcome to the Studio Ghibli Companion! This app is designed to help you manage your courses, homework, notes, and more in a user-friendly way. Here's how to get started: Home Page: Start from the home page, where you'll find an overview of the app's features and a guide on how to use it effectively. Courses Page: Click on the 'Courses' button to access your courses. Here, you can create new courses, upload syllabuses, and manage your course schedule. Creating a New Course: Navigate to the 'Create Course' page. Enter the course name and description. Upload the course syllabus (PDF format). Click 'Create Course' to add it to your list of courses. Homework & Notes Page: Use this page to upload and manage your homework assignments, notes, and other study materials. Calendar Integration: Access your calendar to set important dates for your courses and assignments. This helps you stay organized and on track. AI-Powered Assistance: Ask questions using the AI-powered content generator to get quick responses and assistance with your studies. Customize Your Experience: Explore the sidebar for additional features and options tailored to your needs."

        button_clicked = st.button(button_caption)

        selected_date = st.date_input("Select a date")

        if selected_date:
            st.write(f"You selected: {selected_date}")

        st.caption("About this app :)")
        button_caption = "This notebook application’s purpose is to help the student by keeping them organized with their note taking. They will be able to set their courses in these sections and in them will hold their notebook for that specific class."
        # Display the button with a caption
        button_clicked = st.button(button_caption)


        topics = ["Math", "Science", "History", "English", "Computer Science", "Art"]


        # Display the select box for choosing topics
        selected_topic = st.selectbox("Select a topic you need help with", topics)


        # Display the selected topic
        if selected_topic:
            st.write(f"You selected: {selected_topic}")


    def page2():
        st.markdown("# Courses")
        st.sidebar.markdown("# Your courses")

        # Display existing courses
        if len(st.session_state['courses']) > 0:
            st.sidebar.subheader("Existing Courses")
            for course in st.session_state['courses']:
                new_course = st.sidebar.button(course["name"])
                


    def create_course():
        st.markdown("# Create New Course")

        # Add inputs for course creation with unique keys
        course_name = st.text_input("Course Name", key="course_name_input")
        course_description = st.text_area("Course Description", key="course_description_input")
        upload_syllabus = st.file_uploader("Upload Syllabus (PDF)", type=["pdf"])

        if st.button("Create Course"):
            # Validate inputs
            if not course_name:
                st.error("Please enter a course name.")
                return

            # Create course dictionary
            new_course = {
                "name": course_name,
                "description": course_description,
                "syllabus": upload_syllabus
            }

            # Add new course to the courses list
            st.session_state['courses'].append(new_course)
            st.success(f"Course '{course_name}' created successfully!")

            # Clear inputs after course creation
            st.text_input("Course Name", value="", key="clear_course_name_input")
            st.text_area("Course Description", value="", key="clear_course_description_input")
            st.empty()
            

    def display_courses():
        st.markdown("# Courses")
        if not st.session_state['courses']:
            st.write("No courses created yet.")
        else:
            for course in st.session_state['courses']:
                st.write(f"**{course['name']}**")
                st.write(f"Description: {course['description']}")
                if course['syllabus'] is not None:
                    st.write("Syllabus uploaded")
                else:
                    st.write("No syllabus uploaded")


    def page3():
        st.markdown("# Homework ")
        st.sidebar.markdown("# this is your homework page")
        # Add sidebar content specific to page 3
        image_url = "https://i.pinimg.com/564x/7f/94/f0/7f94f02bfa3f2ca3c1cb8fef7a94e8fb.jpg"
        st.sidebar.image(image_url,)


        
        uploaded_file = st.file_uploader("Please upload your file in a pdf form", type=["pdf"])

        if uploaded_file is not None:
            # Display file details
            file_details = {
                "Filename": uploaded_file.name,
                "File type": uploaded_file.type,
                "File size (bytes)": uploaded_file.size,
            }
            st.write("File details:", file_details)

            # Check if the file is a PDF
            if uploaded_file.type == 'application/pdf':
                # Read PDF file
                with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                    pdf_text = ''
                    for page in pdf.pages:
                        pdf_text += page.extract_text()

                # Display the extracted text
                st.write("PDF file contents:")
                st.text(pdf_text)
            else:
                # Display the uploaded file contents (for non-PDF files)
                file_contents = uploaded_file.read()
                st.write("Uploaded file contents:")
                st.write(file_contents)



    def page4():
        st.markdown("# Notes ")
        st.sidebar.markdown("# this is your notes page")
        # Add sidebar content specific to page 3
        image_url = "https://i.pinimg.com/474x/9d/6b/99/9d6b9908dbd1b4a932a7256c2fa531b6.jpg"
        st.sidebar.image(image_url,)
        
        genai.configure(api_key='AIzaSyCK-rU375-vmt4Th9hvfBhFXthGFNeuCUk')

        model = genai.GenerativeModel('gemini-pro')
        input_text = st.text_input("what is your question? ")
        if input_text:
            response = model.generate_content(input_text)
            st.write(response.text)

    page_names_to_funcs = {
        "Home Page": main_page,   
        "Courses": page2,
        "Homework": page3,
        "Notes": page4,
        "Create Course": create_course, 
    }

    # Set the default value for the selectbox to "Main Page"
    selected_page = st.sidebar.selectbox(" ", page_names_to_funcs.keys(), index=0)

    # Call the function corresponding to the selected page
    page_names_to_funcs[selected_page]()


if __name__ == "__main__":
    if is_verified():
        st.write("Sorry you cannot access the storybook because you need to log in first :)")
    else:
        main()