import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from commonfunctions import is_verified
from commonfunctions import get_logged_in_username
from google.cloud import bigquery


def generate_content(prompt, uploaded_photos, uploaded_texts):
    api_key = "AIzaSyAl7yfZiDw6Rj0cTk4eRifush_1Ijhpaug"
    genai.configure(api_key=api_key)

    # Create text generation model
    text_model = genai.GenerativeModel('gemini-pro')

    # Create image understanding model
    vision_model = genai.GenerativeModel('gemini-pro-vision')

    # Generate text content based on the prompt
    text_response = text_model.generate_content(prompt)

    # Generate image content based on the uploaded photos
    image_responses = []
    image_texts = []  # Store generated text from images
    for photo in uploaded_photos:
        # Open the uploaded photo
        img = Image.open(BytesIO(photo.read()))

        # Generate content based on the image
        image_response = vision_model.generate_content(img)
        image_responses.append(image_response.text)
        image_texts.append(image_response.text)

    # Generate text content based on the uploaded texts
    text_responses = []
    for text_file in uploaded_texts:
        # Read the content of the uploaded text file
        text_content = text_file.getvalue().decode("utf-8")
        
        # Generate content based on the text
        text_response = text_model.generate_content(text_content)
        text_responses.append(text_response.text)

    # Add generated text from images to the prompt
    prompt += " ".join(image_texts)

    return text_response.text, image_responses, text_responses


def main():
    username = get_logged_in_username()
    if username:
        st.title(f"Welcome to the Storybook Generator {username}!")
    else:
        st.title("Welcome to the Storybook Generator!")

    # Text input section for storybook name
    st.header("Storybook Name")
    storybook_name = st.text_input("Enter the storybook name:")

    # File uploader section for photos
    st.header("Upload Photos")
    uploaded_photos = st.file_uploader("Upload photos for the storybook", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # File uploader section for text files
    st.header("Upload Texts")
    uploaded_texts = st.file_uploader("Upload text files for the storybook", type=["txt"], accept_multiple_files=True)

    # Dropdown menu for subjects
    st.header("Subject Selection")
    subject_options = ["Math", "Science", "English Language Arts", "Social Studies/History", "Physical Education"]
    selected_subject = st.selectbox("Select a subject:", subject_options, index=0)

    # Dropdown menu for grade levels
    st.header("Grade Level")
    grade_options = ["Kindergarten", "1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade"]
    selected_grade = st.selectbox("Select a grade level:", grade_options, index=0)

    # Customization section
    st.header("Customizations")
    customization = st.text_area("Add any customizations or specific points you want to get across in the storybook:")

    # Generate button
    if st.button("Generate"):
        prompt = f"Generate a storybook for {storybook_name} on the subject of {selected_subject} for {selected_grade} grade. Customizations: {customization}."
        text_content, image_contents, text_responses = generate_content(prompt, uploaded_photos, uploaded_texts)
        
        # Display generated content
        st.success("Storybook generated successfully!")
        st.write("Generated Text Content:")
        st.write(text_content)
        st.write("Generated Image Content:")
        for image_content in image_contents:
            st.write(image_content)
        st.write("Generated Text Content from Files:")
        for text_response in text_responses:
            st.write(text_response)


if __name__ == "__main__":
    if is_verified():
        st.write("Sorry you cannot access the story book because you need to log in first :)")
    else:
        main()
