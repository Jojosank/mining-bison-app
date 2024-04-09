import streamlit as st

st.set_page_config(
    page_title="Main",
    page_icon="👋",
)

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