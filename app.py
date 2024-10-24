pip install google-generativeai
import streamlit as st
from PIL import Image
import os
import io
import google.generativeai as ai

# Load the API key from Streamlit secrets
api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.error("API key not found! Please configure your API key in Streamlit secrets.")
else:
    ai.configure(api_key=api_key)

# The rest of your code remains the same


# Instantiate the GenerativeModel
try:
    model = ai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error initializing the AI model: {e}")

def get_gemini_response(input_text, image_parts, prompt):
    """Fetche s a response from the AI model with text and image inputs."""
    if not image_parts:
        raise ValueError("Image required for this model. Please upload an image and try again.")
    try:
        response = model.generate_content([input_text] + image_parts + [prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating AI response: {e}")
        return None

def input_image_details(uploaded_file):
    """Processes uploaded images into a format suitable for the AI model."""
    try:
        image = Image.open(uploaded_file)
        byte_array = io.BytesIO()
        image.save(byte_array, format=image.format)
        resized_bytes = byte_array.getvalue()

        image_parts = {
            "mime_type": uploaded_file.type,
            "data": resized_bytes
        }
        return [image_parts], image
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None, None

# Streamlit page setup
st.set_page_config(page_title='Cosmeic AI', page_icon='https://hmp.me/ed22')
st.title('✺ FOODENT')

# Sidebar for image upload options
st.sidebar.title("Image Settings")
image_source_option = st.sidebar.radio("Choose an image source", ["Upload", "Camera"])

# Upload or capture image
uploaded_file = st.sidebar.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png']) if image_source_option == "Upload" else None
captured_image = st.sidebar.camera_input("Take a picture") if image_source_option == "Camera" else None

# Handle the image (upload or capture)
file_to_use = uploaded_file or captured_image
image_parts, display_image = None, None

if file_to_use:
    image_parts, display_image = input_image_details(file_to_use)

# Chat input for user query
user_query = st.chat_input("Upload img & Ask for your cosmetics product")

if user_query and image_parts:
    try:
        with st.spinner('AI is generating a response...'):
            ai_response = get_gemini_response("", image_parts, user_query)
            if ai_response:
                st.markdown(ai_response)
    except ValueError as e:
        st.error(str(e))  # Display the error message to the user
else:
    st.info("Please upload an image and ask a question to get a response.")

# Display uploaded or captured image
if display_image is not None:
    st.image(display_image, caption='Uploaded Image.', width=300)
