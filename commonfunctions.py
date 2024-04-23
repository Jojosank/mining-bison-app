import streamlit as st
from google.cloud import bigquery
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

#check is user has logged in else show the Message to log in
def is_verified():
  return st.session_state.status != "verified"

#get the curr username
def get_username():
  return st.session_state.edu_id

#logout function
def log_out():
  st.session_state.status = "unverified"
  st.rerun()

def log_in_message():
  st.title("Sorry, you cannot access the app until you log in.")

def generate_image(prompt):
  vertexai.init(project="joemotatechx2024", location="us-central1")
  # Load the Image Generation model
  model = ImageGenerationModel.from_pretrained("imagegeneration@006")
  # Generate images based on the user's prompt
  image = model.generate_images(prompt=prompt, number_of_images=1)
  if image:
    # Save the generated image to a file
    image[0].save(location="samplefile.jpg")
    # Display the generated image
    st.image("samplefile.jpg")