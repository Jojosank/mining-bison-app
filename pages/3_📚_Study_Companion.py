import streamlit as st
from commonfunctions import get_username,is_verified,log_out
from google.cloud import bigquery
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import pdfplumber
import io
import calendar
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
import bcrypt

client = bigquery.Client(project='paolaalvaradotechx2024')
def main():
    def main_page():
        if st.sidebar.button("Logout"):
            log_out()
            st.rerun()
        st.write(
            f"""
            # Welcome to your Study Companion {get_username()}!""")

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
            ## How to Use This App

            Welcome to the Studio Ghibli Companion! This app is designed to help you manage your courses, homework, notes, and more in a user-friendly way. Here's a step-by-step guide to get started:

            ### 1. Home Page
            - Start from the home page, where you'll find an overview of the app's features and a guide on how to use it effectively.

            ### 2. Courses Page
            - Click on the 'Courses' button in the sidebar to access your courses. Here, you can manage your course schedule.

            ### 3. Homework & Notes Page
            - Use this page to manage your homework assignments, notes, and other study materials.

            ### 4. Create New Course
            - Navigate to the 'Create Course' page from the sidebar. Enter the course name, description, and upload the course syllabus (PDF format). Click 'Save Course' to add it to your list of courses.

            ### 5. Take Notes
            - Click on 'Take Notes' in the sidebar to start taking notes for your courses. Enter the course name and your notes, then click 'Save Notes' to store them securely.

            ### 6. Create New Homework
            - Access the 'Create Homework' page from the sidebar. Enter the course name, homework content, and select the due date. Click 'Save Homework' to add it to your assignments.

            ### 7. AI-Powered Assistance
            - Use the AI-powered features like generating notes, summaries, quizzes, and answering general questions. Enter your query and select the appropriate option to get instant assistance.

            Enjoy using the Studio Ghibli Companion app for a seamless academic experience!
            """)
            # Button for "About this app"
        about_button = st.button("About this app", key="about_button")


        # Show "About this app" content when the button is clicked
        if about_button:
            st.markdown("""
            ## About This App

            Welcome to the Studio Ghibli Companion web app! This app is designed to enhance your academic experience by providing tools and features to manage your courses, assignments, notes, and more. Here's a brief overview:

            ### Features:
            - **Courses Management:** Create, edit, and manage your courses with ease.
            - **Homework Tracker:** Keep track of your homework assignments and due dates.
            - **Notes Organizer:** Take and organize notes for each of your courses.
            - **AI-Powered Assistance:** Get quick answers, summaries, and quiz generation with AI.
            - **User-friendly Interface:** Designed for a seamless and intuitive user experience.

            ### How to Use:
            - Explore the sidebar for different sections like Courses, Homework, Notes, and AI Assistance.
            - Use the buttons and input fields to interact with the app's features.
            - Click on "How to use this app?" for a detailed guide on using each feature.

            ### Privacy and Security:
            - Your data is securely stored and accessible only to you.
            - Log out from the sidebar when you're done to ensure your account's security.
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

        if 'courses' not in st.session_state:
            st.session_state.courses = []

    def insert_data_into_bigquery(username, course_name, description):
        # Define the BigQuery table ID
        # Get the current timestamp
        timestamp = datetime.utcnow().isoformat()

        # Prepare the data to insert
        row_to_insert = {
            "username": username,
            "course_name": course_name,
            "description": description,
            "timestamp": timestamp 
        }

        # Insert the row into the BigQuery table
        errors = client.insert_rows_json(table_id, [row_to_insert])

        if errors:
            st.error(f"Failed to insert data into BigQuery: {errors}")
        else:
            st.success("Data inserted into BigQuery successfully.")

    # Function to save new course to BigQuery
    def get_courses_data():
        query = """
        SELECT * FROM `paolaalvaradotechx2024.courses_created.new_courses`
        """
        result = client.query(query).result()
        courses_data = result.to_dataframe()
        st.dataframe(courses_data)

    # dataset_id = 'courses_created'
    # table_id = 'new_courses'

    def save_course_to_bigquery(course_data):
        # Convert date to string format
        dataset_id = 'courses_created'
        table_id = 'new_courses'
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
        image_url1 = "https://i.pinimg.com/474x/90/91/66/909166632963c38c1c6ddceb2d665be0.jpg"
        st.sidebar.image(image_url1,)
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

            # Save the course data to BigQuery
            save_course_to_bigquery({"course_name": course_name, "description": description})

            # Add the new course to the session state
            st.session_state.courses.append({"course_name": course_name, "description": description})

    def page2():
        st.markdown("# Courses")
        if not st.session_state.courses:
            st.write("No courses created yet.")
        else:
            for course in st.session_state.courses:
                if st.button(course['course_name']):
                    st.write(f"**{course['course_name']}**")
                    st.write(f"Description: {course['description']}")

        image_url1 = "https://i.pinimg.com/474x/7c/ba/df/7cbadf06fabf2bee9d629a02be5fd7c2.jpg"
        st.sidebar.image(image_url1)
        st.sidebar.caption("You got this!")

    # Function to save homework data to BigQuery including PDF files

    def save_homework_to_bigquery(course_name, homework_content, due_date):
        # Create a dictionary to store the homework data
        dataset_id = 'homework_data'
        table_id = 'homework_input'
        
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
                st.success("Homework saved successfully.")
            else:
                st.error(f"Failed to save homework: {errors}")
        except Exception as e:
            st.error(f"Error saving homework to BigQuery: {str(e)}")


    def create_homework():
        
        st.markdown("# Create New Homework")

        image_url1 = "https://i.pinimg.com/564x/ce/82/50/ce825004db3537dd8e42e23ebd261a5a.jpg"
        st.sidebar.image(image_url1,)
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
        #    image_url1 = "https://i.pinimg.com/564x/dc/85/ad/dc85ad2f9f21c8210d33cb4345c47deb.jpg"
        #    st.image(image_url1,)
        st.markdown("# Homework")
        image_url1 = "https://i.pinimg.com/474x/54/09/dc/5409dc6dc6ed4e7e32e1b138f4ccbe74.jpg"
        st.sidebar.image(image_url1,)
        
        dataset_id = 'homework_data'
        table_id = 'homework_input'
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



        # Define your dataset ID and table ID



    def save_notes_to_bigquery(course_name, notes_content):
        # Get the current date
        dataset_id = 'notes_from_student'
        table_id = 'notes'
        current_date = datetime.now().date()


        # Create a dictionary to store the note data
        note_data = {
            "course_name": course_name,
            "date_created": current_date,
            "notes": notes_content,
        }


        # Insert the note data into the BigQuery table
        try:
            table_ref = client.dataset(dataset_id).table(table_id)
            table = client.get_table(table_ref)


            rows_to_insert = [note_data]
            errors = client.insert_rows(table, rows_to_insert)


            if errors == []:
                st.success("Notes saved successfully")
            else:
                st.error(f"Failed to save notes: {errors}")
        except Exception as e:
            st.error(f"Error saving notes to BigQuery: {str(e)}")


    def take_notes():

        image_url1 = "https://i.pinimg.com/474x/3a/24/97/3a2497341730363d623b2d45fa6a12ac.jpg"
        st.sidebar.image(image_url1,)

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

if __name__ == "__main__":
    if is_verified():
        st.write("Sorry you cannot access the storybook because you need to log in first :)")
    else:
        main()


