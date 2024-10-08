import bcrypt
import streamlit as st
from google.cloud import bigquery
from commonfunctions import*

client = bigquery.Client('joemotatechx2024')

st.set_page_config(
            page_title="Main",
            page_icon="👋",
        )

st.session_state.status = st.session_state.get("status", "unverified")

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    tmp = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return tmp.decode('utf-8')


def check_password():
    QUERY = (
        f"""SELECT * FROM `joemotatechx2024.user_data.user_login` WHERE username = @username"""
    )

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", st.session_state.username),
        ]
    )

    query_job = client.query(QUERY, job_config=job_config)
    rows = query_job.result()
    if rows.total_rows > 0:
        for row in rows:
            if bcrypt.checkpw(st.session_state.password.encode('utf-8'), row.hashed_password.encode('utf-8')):
                st.session_state.status = "verified"
                return  # Exit function after successful login and update
    if st.session_state.status != "verified":
        st.session_state.status = "incorrect"

def login_prompt():
    username = st.text_input("Enter username:", key="username")
    st.session_state.edu_id = username
    password = st.text_input("Enter password:", key="password")
    st.button("Create user", on_click=create_user)
    st.button("Log in", on_click=check_password)
    if st.session_state.status == "incorrect":
        st.warning("Incorrect username and password. Please try again")
    if st.session_state.status == "user_already_exists":
        st.warning("Username already exists")

def logout():
    st.session_state.status = "unverified"

def create_user():
    QUERY = ("SELECT hashed_password FROM `joemotatechx2024.user_data.user_login` WHERE username = '" +
             st.session_state.username + "'")
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "username", "STRING", st.session_state.username),
        ]
    )
    query_job = client.query(QUERY, job_config=job_config)
    rows = query_job.result()
    if rows.total_rows == 0:
        myquery = "INSERT INTO `joemotatechx2024.user_data.user_login` (username, hashed_password) VALUES (\"%s\", \"%s\")" % (
            st.session_state.username, get_hashed_password(st.session_state.password))
        QUERY = (myquery)
        query_job = client.query(QUERY)  
        rows = query_job.result()  
        st.session_state.status = "verified"
    else:
        st.session_state.status = "user_already_exists"

def welcome():
    st.success("Login successful.")
    st.button("Log out", on_click=logout)

if __name__ == "__main__":
    if st.session_state.status != "verified":
        login_prompt()
    else:
        welcome()

        st.write("# Welcome to Project MB ⛏️🦬!", get_username() + "!")

        st.sidebar.success("Select a demo above.")

        st.write("The purpose of our proposed system is to provide comprehensive support and tools for educators, students, and learners in academic environments. The system comprises three key components, each targeting specific user needs:")

        st.title("Miner the Story Teller")

        st.write("Empower but not limited to teachers to create captivating and educational storybooks effortlessly. This feature automates the process of generating interactive storybooks, allowing teachers to focus on fostering creativity and enhancing learning experiences.")

        st.title("Academic Advising")

        st.write("Support students in making informed decisions about their academic journey. With personalized recommendations and academic advising functionalities, students can navigate course selections, career pathways, and educational goals with confidence.")
        
        st.title("Study Companion")

        st.write("Provide learners with dynamic tools for effective self-study and revision. Our interactive notebook offers features such as note-taking, content summarization, flashcard creation, and practice quizzes, enhancing the learning process and promoting engagement.")

        generate_image("Generate an image of a Miner and Bison combined")
        