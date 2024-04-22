import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from commonfunctions import*
from google.cloud import bigquery
from datetime import datetime
from fpdf import FPDF
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import base64
import io

client = bigquery.Client('joemotatechx2024')
st.set_page_config(layout='wide')

def create_pdf(story,output_image_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, story)

    pdf.add_page()
    pdf.image(output_image_path, x=10, y=pdf.get_y() + 10, w=150)

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

    prompt = "What is the main idea of this story: "

    prompt += " ".join(story_content)

    text_response = text_model.generate_content(prompt)

    # Access the text attribute of the GenerateContentResponse object
    prompt = "Create a single sentence prompt for Google's text to image generation api to generate an image based on the main idea of this story. " + text_response.text + "Start with the following words, Generate an image.."

    text_response = text_model.generate_content(prompt)
    
    return text_response.text

def generate_image_from_text(story_content, output_image_path, generated):
    try:
        # Initialize the image generation model
        vertexai.init(project="joemotatechx2024", location="us-central1")
        model = ImageGenerationModel.from_pretrained("imagegeneration@006")
        
        promptInfo = generate_prompt_for_image_generation(story_content)
        # Generate the image based on the text
        images = model.generate_images(prompt=promptInfo, number_of_images=1)
        
        # Save the generated image
        images[0].save(location=output_image_path, include_generation_parameters=False)
        return
    except Exception:
        generated = False
        st.error("Sorry we couldnt generate the image. Please try generating again")
        return

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
    if len(image_contents) >= 1:
        prompt += "Here is an image content ".join(image_contents)

    # Generate text content based on the prompt
    text_response = text_model.generate_content(prompt)
    
    return text_response.text

def get_all_stories(username):
    # Define the BigQuery table ID
    table_id = "joemotatechx2024.storybook.user_stories"

    # Construct the SQL query to retrieve all stories for the given username
    query = f"""
        SELECT story_name, story
        FROM `{table_id}`
        WHERE username = @username
        ORDER BY timestamp DESC
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
    stories = [{"story_name": row["story_name"], "story": row["story"]} for row in results]

    return stories

def main():

    if st.sidebar.button("Log Out"):
        log_out()
    video_file = open('HelpVideo.mp4', 'rb')
    video_bytes = video_file.read()
    st.sidebar.title("Need Help?")
    st.sidebar.title("Check out this demo below!")
    st.sidebar.video(video_bytes)

    generated = True

    st.markdown(
        """
        <div style="position: relative; background-color: #FFA421; padding: 1px 0;">
            <h1 style='font-size: 75px; margin: 0; color: white; text-align: center; position: relative; z-index: 2; width: 100%;'>Miner the Story Teller</h1>
            <img src="https://seeklogo.com/images/U/utep-miners-logo-A773F61820-seeklogo.com.png" class="logo" style="position: absolute; top: 20px; left: 20px; z-index: 3; width: 200px; height: auto;">
            <div style="height: 40px; background-color: #FFA421; position: absolute; bottom: 0; left: 0; width: 100%; z-index: 1;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    username = st.session_state.edu_id

    st.markdown(f"<p style='text-align: center; font-size: 55px; color: white; font-weight: bold;'>Let's create your Story {username}!</p>",unsafe_allow_html=True)

    st.markdown("#")

    st.markdown("<p style='text-align: center; font-size: 50px; font-weight: bold;'>Name Your Book</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Give your Story Book a Name</p>", unsafe_allow_html=True)
    story_name = st.text_input("Enter Story Book name below")

    st.markdown("<p style='text-align: center; font-size: 50px; font-weight: bold;'>Upload Content</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>AI analysis regarding their relevance to the story</p>", unsafe_allow_html=True)
    uploaded_photos = st.file_uploader("Upload photos for the Story Book", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Divide the file upload and Help section into two cols so they can be next to each other
    col1, col2  = st.columns(2)  # Adjust the width of the columns as needed

    selected_subject = ""
    with col1:
        st.markdown("<p style='text-align: center; font-size: 50px; font-weight: bold;'>Subject</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Base your story off a specific subject</p>", unsafe_allow_html=True)
        subject_options = ["Math", "Science", "English Language Arts", "Social Studies/History", "Physical Education"]
        selected_subject = st.selectbox("Select a subject:", subject_options, index=0)
    
    selected_grade = ""
    with col2:
        st.markdown("<p style='text-align: center; font-size: 50px; font-weight: bold;'>Grade Level</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Cater you grammer to your Grade Level</p>", unsafe_allow_html=True)
        grade_options = ["Kindergarten", "1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade"]
        selected_grade = st.selectbox("Select a grade level:", grade_options, index=0)

    st.markdown("<p style='text-align: center; font-size: 50px; font-weight: bold;'>Specail Requests</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Add any input or customizations to influence the output of the Story Book</p>", unsafe_allow_html=True)
    customization = st.text_area("Customizations or specific requests for the storybook:")



    output_image_path = "output_image.png"

    button_style = """
        <style >
        .stDownloadButton, div.stButton {text-align:center}
        .stDownloadButton button, div.stButton > button:first-child {
            background-color: #FFA421;
            color: #FF000;
            padding-top: 30px;
            padding-bottom: 30px;
            padding-left: 150px;
            padding-right: 150px;
            font-weight: bold;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)


    if st.button("Generate"):
        if not story_name:
            st.warning("Please enter a story name.")
        else:
            prompt = f"Generate a storybook on the subject of {selected_subject} for {selected_grade} grade. Special Requests: {customization}. Make sure to provide a title to the story"

            image_contents = ""
            # Generate image contents
            if uploaded_photos:
                # Generate image contents
                image_contents = generate_image_contents(uploaded_photos)
            
            # Generate storybook content
            story_content = generate_storybook(prompt, image_contents)

            # Generate an image from the story content
            generate_image_from_text(str(story_content), output_image_path, generated)
            if not generated:
                generated = True
            else:
                st.markdown("<p style='text-align: center; font-size: 50px; font-weight: bold;'>Preview</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Checkout your Story Book</p>", unsafe_allow_html=True)
                # Display generated content
                st.success("Storybook generated successfully!")
                display_story(story_content, output_image_path)

                pdf_bytes = create_pdf(story_content,output_image_path)

                filename = f"{story_name}.pdf"

                #Save your story into big Query
                insert_data_into_bigquery(username, story_name, story_content)

                # Create a download button for the PDF file
                st.markdown("<p style='text-align: center; font-size: 50px; font-weight: bold;'>Finalize</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Download your Story Book</p>", unsafe_allow_html=True)
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                )

    st.markdown("<p style='text-align: center; font-size: 50px; font-weight: bold;'>Library</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Checkout all your previously created Story Books</p>", unsafe_allow_html=True)

    users_stories = get_all_stories(username)

    if users_stories:
        story_names = [story["story_name"] for story in users_stories]
        selected_story_name = st.selectbox("Select a story:", story_names)
    
        if selected_story_name:
            selected_story = next((story for story in users_stories if story["story_name"] == selected_story_name), None)
            if selected_story:
                if st.button("Generate Past Story"):
                    # Generate and display the image for the selected story
                    generate_image_from_text(selected_story["story"], output_image_path,generated)
                    if not generated:
                        generated = True
                    else:
                        display_story(selected_story["story"], output_image_path)
                    
                        # Create and download the PDF for the selected story
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
    if is_verified():
        log_in_message()
        generate_image("Generate an image of a Miner")
    else:
        main()