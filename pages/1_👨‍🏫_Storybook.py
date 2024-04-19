import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from commonfunctions import is_verified
from commonfunctions import get_logged_in_username
from google.cloud import bigquery
from datetime import datetime
from fpdf import FPDF
from reportlab.pdfgen import canvas
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import base64
import io

client = bigquery.Client('joemotatechx2024')

def create_pdf(story,output_image_path,):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, story)

    pdf.image(output_image_path, x=10, y=pdf.get_y() + 10, w=100)

    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output(dest="S").encode("latin1"))
    pdf_bytes = pdf_output.getvalue()
    return pdf_bytes

def display_story(story_content, output_image_path):
    st.write("Generated Storybook Content:")
    st.write(story_content)
    image = Image.open(output_image_path)
    st.image(image, caption='Story Book Image')
        

def insert_data_into_bigquery(username, story_name, story_content):
    # Define the BigQuery table ID
    table_id = "joemotatechx2024.storybook.user_stories"

    # Get the current timestamp
    timestamp = datetime.utcnow().isoformat()

    # Prepare the data to insert
    row_to_insert = {
        "username": username,
        "story_name": story_name,
        "story": story_content,
        "timestamp": timestamp 
    }

    # Insert the row into the BigQuery table
    errors = client.insert_rows_json(table_id, [row_to_insert], row_ids=[None])

    if errors:
        print(f"Errors encountered while inserting data into BigQuery: {errors}")
    else:
        print("Data inserted successfully into BigQuery table.")

def generate_prompt_for_image_generation(story_content):
    api_key = "AIzaSyAl7yfZiDw6Rj0cTk4eRifush_1Ijhpaug"
    genai.configure(api_key=api_key)

    # Create text generation model
    text_model = genai.GenerativeModel('gemini-pro')

    # Add generated story contents to the prompt
    prompt = "create a simple prompt for Google's text to image generation api to understand this story and doesnt give me this error: This prompt contains words that violate Vertex AI's usage guidelines. Story Book: "

    prompt += " ".join(story_content)
    # Generate text content based on the prompt
    text_response = text_model.generate_content(prompt)

    return text_response.text

def generate_image_from_text(story_content, output_image_path):
    # Initialize the image generation model
    vertexai.init(project="joemotatechx2024", location="us-central1")
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    
    promptInfo = generate_prompt_for_image_generation(story_content)
    # Generate the image based on the text
    images = model.generate_images(prompt=promptInfo, number_of_images=1)
    
    # Save the generated image
    images[0].save(location=output_image_path, include_generation_parameters=False)

def generate_image_contents(uploaded_photos):
    api_key = "AIzaSyAl7yfZiDw6Rj0cTk4eRifush_1Ijhpaug" 
    genai.configure(api_key=api_key)

    # Create image understanding model
    vision_model = genai.GenerativeModel('gemini-pro-vision')

    image_contents = []

    for photo in uploaded_photos:
        # Open the uploaded photo
        img = Image.open(BytesIO(photo.read()))

        # Generate content based on the image
        image_response = vision_model.generate_content(img)
        image_contents.append(image_response.text)

    return image_contents

def generate_storybook(prompt, image_contents):
    api_key = "AIzaSyAl7yfZiDw6Rj0cTk4eRifush_1Ijhpaug"
    genai.configure(api_key=api_key)

    # Create text generation model
    text_model = genai.GenerativeModel('gemini-pro')

    # Add generated image contents to the prompt
    prompt += " ".join(image_contents)

    # Generate text content based on the prompt
    text_response = text_model.generate_content(prompt)

    return text_response.text

def get_last_two_stories(username):
    # Define the BigQuery table ID
    table_id = "joemotatechx2024.storybook.user_stories"

    # Construct the SQL query to retrieve the last two stories for the given username
    query = f"""
        SELECT story_name, story
        FROM `{table_id}`
        WHERE username = @username
        ORDER BY timestamp DESC
        LIMIT 2
    """

    # Set up the query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username)
        ]
    )

    # Execute the query
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Process the results
    stories = []
    for i, row in enumerate(results):
        story_name = row["story_name"]
        story_content = row["story"]
        output_image_path = f"image_output{i+2}.png"
        generate_image_from_text(story_content, output_image_path)
        stories.append({
            "story_name": story_name,
            "story": story_content,
            "image_path": output_image_path
        })

    return stories

def main():
    username = get_logged_in_username()

    if username:
        st.title(f"Welcome to the Storybook Generator {username}!")
    else:
        st.title("Welcome to the Storybook Generator!")

    # Text input section for storybook name
    st.header("Storybook Name")
    story_name = st.text_input("Enter the storybook name:")

    # File uploader section for photos
    st.header("Upload Photos")
    uploaded_photos = st.file_uploader("Upload photos for the storybook", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

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
    customization = st.text_area("Add any customizations or specific points you want to get across in the storybook or how many pages you want in the story book etc.:")

    # Generate Button
    if st.button("Generate") and uploaded_photos:
        prompt = f"Generate a storybook on the subject of {selected_subject} for {selected_grade} grade. Special Requests: {customization}. Make sure to provide a title to the story"

        # Generate image contents
        image_contents = generate_image_contents(uploaded_photos)
        
        # Generate storybook content
        story_content = generate_storybook(prompt, image_contents)

        # Generate an image from the story content
        output_image_path = "output_image.png"
        generate_image_from_text(str(story_content), output_image_path)

        # Display generated content
        st.success("Storybook generated successfully!")
        display_story(story_content, output_image_path)

        pdf_bytes = create_pdf(story_content,output_image_path)

        filename = "story.pdf"

        insert_data_into_bigquery(username, story_name, story_content)

        # Create a download button for the PDF file
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
        )
        
    # Library Section    
    st.header("Library")

    # Get the last two stories for the user
    last_two_stories = get_last_two_stories(username)

    if last_two_stories:
        for i, story in enumerate(last_two_stories):
            st.subheader(f"Story {i+1}: {story['story_name']}")
            st.write(story['story'])
            image = Image.open(story['image_path'])
            st.image(image, caption='Story Image')
    else:
        st.write("You have no stories yet.")
    

if __name__ == "__main__":
    if is_verified():
        st.write("Sorry you cannot access the storybook because you need to log in first :)")
    else:
        main()