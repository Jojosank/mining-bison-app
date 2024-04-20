import streamlit as st
import commonfunctions
from PIL import Image
from io import BytesIO
from google.cloud import bigquery
from datetime import datetime
from fpdf import FPDF
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import base64

client = bigquery.Client('joemotatechx2024')

def create_pdf(story, output_image_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, story)
    pdf.add_page()
    pdf.image(output_image_path, x=10, y=pdf.get_y() + 10, w=150)
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest="S").encode("latin1"))
    pdf_bytes = pdf_output.getvalue()
    return pdf_bytes

def display_story(story_content, output_image_path):
    st.write("Generated Storybook Content:")
    st.write(story_content)
    image = Image.open(output_image_path)
    st.image(image, caption='Story Book Image')

def insert_data_into_bigquery(username, story_name, story_content):
    table_id = "joemotatechx2024.storybook.user_stories"
    timestamp = datetime.utcnow().isoformat()
    row_to_insert = {
        "username": username,
        "story_name": story_name,
        "story": story_content,
        "timestamp": timestamp 
    }
    errors = client.insert_rows_json(table_id, [row_to_insert], row_ids=[None])
    if errors:
        print(f"Errors encountered while inserting data into BigQuery: {errors}")
    else:
        print("Data inserted successfully into BigQuery table.")

def generate_image_from_text(story_content, output_image_path):
    vertexai.init(project="joemotatechx2024", location="us-central1")
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    prompt_info = generate_prompt_for_image_generation(story_content)
    images = model.generate_images(prompt=prompt_info, number_of_images=1)
    images[0].save(location=output_image_path, include_generation_parameters=False)

def generate_prompt_for_image_generation(story_content):
    prompt = "Create a single sentence prompt for Google's text to image generation API to generate an image for this Story Book. Start with the following words: Generate ..."
    prompt += " ".join(story_content)
    return prompt

def generate_image_contents(uploaded_photos):
    image_contents = []
    for photo in uploaded_photos:
        img = Image.open(BytesIO(photo.read()))
        image_contents.append(img)
    return image_contents

def generate_storybook(prompt, image_contents):
    text_model = genai.GenerativeModel('gemini-pro')
    if len(image_contents) > 1:
        prompt += " ".join(image_contents)
    text_response = text_model.generate_content(prompt)
    return text_response.text

def get_last_ten_stories(username):
    table_id = "joemotatechx2024.storybook.user_stories"
    query = f"""
        SELECT story_name, story
        FROM `{table_id}`
        WHERE username = @username
        ORDER BY timestamp DESC
        LIMIT 10
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("username", "STRING", username)]
    )
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    stories = [{"story_name": row["story_name"], "story": row["story"]} for row in results]
    return stories

def main():
    username = commonfunctions.get_username()
    if username:
        st.title(f"Welcome to the Storybook Generator {username}!")
    else:
        st.title("Welcome to the Storybook Generator!")

    st.header("Storybook Creation")

    story_name = st.text_input("Enter the storybook name:")
    uploaded_photos = st.file_uploader("Upload photos for the storybook", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    subject_options = ["Math", "Science", "English Language Arts", "Social Studies/History", "Physical Education"]
    selected_subject = st.selectbox("Select a subject:", subject_options, index=0)
    
    grade_options = ["Kindergarten", "1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade"]
    selected_grade = st.selectbox("Select a grade level:", grade_options, index=0)
    
    customization = st.text_area("Customizations or specific points for the storybook:")

    output_image_path = "output_image.png"

    if st.button("Generate"):
        prompt = f"Generate a storybook on the subject of {selected_subject} for {selected_grade} grade. Special Requests: {customization}. Make sure to provide a title to the story"
        image_contents = generate_image_contents(uploaded_photos) if uploaded_photos else []
        story_content = generate_storybook(prompt, image_contents)
        generate_image_from_text(str(story_content), output_image_path)
        st.success("Storybook generated successfully!")
        display_story(story_content, output_image_path)
        pdf_bytes = create_pdf(story_content, output_image_path)
        filename = f"{story_name}.pdf"
        insert_data_into_bigquery(username, story_name, story_content)
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
        )
        
    st.header("Library")
    last_ten_stories = get_last_ten_stories(username)
    if last_ten_stories:
        story_names = [story["story_name"] for story in last_ten_stories]
        selected_story_name = st.selectbox("Select a story:", story_names)
        if selected_story_name:
            selected_story = next((story for story in last_ten_stories if story["story_name"] == selected_story_name), None)
            if selected_story:
                if st.button("Generate Past Story"):
                    generate_image_from_text(selected_story["story"], output_image_path)
                    display_story(selected_story["story"], output_image_path)
                    pdf_bytes = create_pdf(selected_story["story"], output_image_path)
                    filename = f"{selected_story_name}.pdf"
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                    )
    else:
        st.write("You have no stories created yet.")

if __name__ == "__main__":
    main()
