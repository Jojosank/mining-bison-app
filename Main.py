import streamlit as st
import bcrypt
from google.cloud import bigquery

client = bigquery.Client('joemotatechx2024')

# st.title("My login page")

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
    QUERY = ("SELECT * FROM `joemotatechx2024.user_data.user_login` WHERE username = '" +
             st.session_state.username + "'")
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "username", "STRING", st.session_state.username),
        ]
    )
    query_job = client.query(QUERY, job_config=job_config)
    rows = query_job.result()
    if rows.total_rows > 0:
        for row in rows:
            if bcrypt.checkpw(st.session_state.password.encode('utf-8'), row.hashed_password.encode('utf-8')):
                #Update logged_in to YES if password matches
                update_query = f"""
                    UPDATE `joemotatechx2024.user_data.user_login`
                    SET logged_in = 'YES'
                    WHERE username = @username
                """
                update_job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("username", "STRING", st.session_state.username)
                    ]
                )
                client.query(update_query, job_config=update_job_config)
                st.session_state.status = "verified"
                return  # Exit function after successful login and update
    if st.session_state.status != "verified":
        st.session_state.status = "incorrect"


def login_prompt():
    st.text_input("Enter username:", key="username")
    st.text_input("Enter password:", key="password")
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
        query_job = client.query(QUERY)  # API request
        rows = query_job.result()  # Waits for query to finish
        st.session_state.status = "unverified"
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

        st.write("# Welcome to Project MB ⛏️🦬!")

        st.sidebar.success("Select a demo above.")

        st.markdown(
            """
            The purpose of our proposed system is to provide comprehensive support and tools for educators, students, and learners in academic environments. The system comprises three key components, each targeting specific user needs:

            1. Storybook Generator for Teachers:
            The first component focuses on assisting teachers by automating the creation of interactive storybooks. This feature enables teachers to develop engaging and educational content for their students, fostering creativity and enhancing learning experiences.

            2. Academic Advising and Course Recommendation for Students:
            The second component is designed to aid students in making informed decisions about their academic journey. Students can receive guidance on course selections, career pathways, and educational goals through personalized recommendations and academic advising functionalities.

            3. Interactive Notebook with Learning Support:
            The third component aims to empower learners with interactive tools for note-taking, content summarization, flashcard creation, and practice quizzes. This component enhances the learning process by providing dynamic and engaging resources for self-study and revision.
        """
        )