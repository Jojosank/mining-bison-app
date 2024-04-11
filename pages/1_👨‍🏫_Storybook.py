import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO

#function to generate content using Gen AI
def generate_content(prompt, uploaded_photos):

    api_key = "AIzaSyAl7yfZiDw6Rj0cTk4eRifush_1Ijhpaug"

    genai.configure(api_key=api_key)

    #create text generation model
    text_model = genai.GenerativeModel('gemini-pro')

    #create image understanding model
    vision_model = genai.GenerativeModel('gemini-pro-vision')

    #generate text content based on the prompt
    text_response = text_model.generate_content(prompt)

    #generate image content based on the uploaded photos
    image_responses = []
    for photo in uploaded_photos:
        #open the uploaded photo
        img = Image.open(BytesIO(photo.read()))

        #generate content based on the image
        image_response = vision_model.generate_content(img)
        image_responses.append(image_response.text)

    return text_response.text, image_responses

def main():
    st.title("Storybook Creator")

    #ask user to enter a storybook name
    storybook_name = st.text_input("Enter the storybook name:")

    #file uploader section for photos
    st.header("Upload Photos")
    uploaded_photos = st.file_uploader("Upload photos for the storybook", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    #dropdown menu for subjects
    st.header("Subject Selection")
    subject_options = ["Math", "Science", "English Language Arts", "Social Studies/History", "Physical Education"]
    selected_subject = st.selectbox("Select a subject:", subject_options, index=0)

    #dropdown menu for grade levels
    st.header("Grade Level")
    grade_options = ["Kindergarten", "1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade"]
    selected_grade = st.selectbox("Select a grade level:", grade_options, index=0)

    #customization section
    st.header("Customizations")
    customization = st.text_area("Add any customizations or specific points you want to get across in the storybook:")

    #generate button
    if st.button("Generate"):
        prompt = f"Generate a storybook for {storybook_name} on the subject of {selected_subject} for {selected_grade} grade. Customizations: {customization}."
        text_content, image_contents = generate_content(prompt, uploaded_photos)
        
        # Display generated content
        st.success("Storybook generated successfully!")
        st.write("Generated Text Content:")
        st.write(text_content)
        st.write("Generated Image Content:")
        for image_content in image_contents:
            st.write(image_content)

if __name__ == "__main__":
    main()
