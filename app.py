import streamlit as st
import google.generativeai as genai
import base64
from io import BytesIO

def setup_page():
    """Configure the Streamlit page"""
    st.set_page_config(page_title='Foodent AI', page_icon='🍽️')
    st.title('✺ FOODENT')

def initialize_ai():
    """Initialize the AI model"""
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        if not api_key:
            st.error("API key not found!")
            return None
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Error initializing AI model: {e}")
        return None

def process_image(file):
    """Process the uploaded file without using PIL"""
    try:
        if not file:
            return None
        
        bytes_data = file.getvalue()
        return [{
            "mime_type": file.type,
            "data": bytes_data
        }]
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

def get_ai_response(model, image_parts, query):
    """Get AI response"""
    try:
        if not model or not image_parts:
            return None

        prompt = f"""
        Analyze this food image and respond to the following query:
        {query}
        
        Please provide:
        - Ingredients identified
        - Nutritional insights
        - Preparation methods
        - Dietary considerations
        """

        response = model.generate_content([prompt] + image_parts)
        return response.text
    except Exception as e:
        st.error(f"Error getting AI response: {e}")
        return None

def main():
    setup_page()
    model = initialize_ai()

    # Sidebar
    st.sidebar.title("Image Settings")
    image_source = st.sidebar.radio("Choose image source:", ["Upload", "Camera"])
    
    # Image input
    if image_source == "Upload":
        file = st.sidebar.file_uploader("Upload food image...", type=['jpg', 'jpeg', 'png'])
    else:
        file = st.sidebar.camera_input("Take a food picture")

    # Display image and handle query
    if file:
        st.image(file, caption="Uploaded Image", width=300)
        image_parts = process_image(file)
        
        query = st.text_area("Ask about your food:",
            placeholder="Example: What ingredients can you identify?")
        
        if query and image_parts:
            with st.spinner("Analyzing..."):
                response = get_ai_response(model, image_parts, query)
                if response:
                    st.markdown(response)
    else:
        st.info("Please upload or capture a food image to begin.")

if __name__ == "__main__":
    main()
