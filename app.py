# requirements.txt should include:
# streamlit>=1.39.0
# Pillow>=10.0.0
# google-generativeai>=0.3.0
# python-dotenv>=1.0.0

import streamlit as st
from PIL import Image
import io
import google.generativeai as genai
from typing import Optional, Tuple, Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FoodentApp:
    def __init__(self):
        self.setup_page()
        self.initialize_ai()

    def setup_page(self):
        """Configure the Streamlit page settings"""
        st.set_page_config(
            page_title='Foodent AI',
            page_icon='🍽️',
            layout='wide'
        )
        st.title('✺ FOODENT')
        st.markdown("""
        Analyze your food and get detailed insights using AI.
        Upload or capture an image to get started!
        """)

    def initialize_ai(self):
        """Initialize the Google Generative AI model"""
        try:
            api_key = st.secrets["GOOGLE_API_KEY"]
            if not api_key:
                st.error("API key not found in Streamlit secrets!")
                return
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            logger.info("AI model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AI model: {e}")
            st.error("Failed to initialize AI model. Please check your API key and try again.")
            self.model = None

    def process_image(self, file) -> Tuple[Optional[List[Dict]], Optional[Image.Image]]:
        """Process uploaded image file"""
        try:
            if not file:
                return None, None

            image = Image.open(file)
            
            # Convert to RGB if necessary
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            # Resize image if too large (optional)
            max_size = 1600
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            byte_stream = io.BytesIO()
            image.save(byte_stream, format='JPEG')
            image_data = byte_stream.getvalue()

            image_parts = [{
                "mime_type": "image/jpeg",
                "data": image_data
            }]
            
            return image_parts, image
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            st.error("Failed to process image. Please try another image.")
            return None, None

    def get_ai_response(self, image_parts: List[Dict], query: str) -> Optional[str]:
        """Get response from AI model"""
        try:
            if not self.model:
                st.error("AI model not initialized")
                return None

            prompt = f"""
            Analyze this food image and respond to the following query:
            {query}
            
            Please provide detailed information about:
            - Ingredients identification
            - Nutritional insights
            - Preparation methods (if visible)
            - Any relevant dietary considerations
            """

            response = self.model.generate_content([prompt] + image_parts)
            return response.text
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            st.error("Failed to get AI response. Please try again.")
            return None

    def run(self):
        """Run the Streamlit application"""
        # Sidebar settings
        with st.sidebar:
            st.title("Image Settings")
            image_source = st.radio("Choose image source:", ["Upload", "Camera"])
            
            if image_source == "Upload":
                file = st.file_uploader("Upload food image...", type=['jpg', 'jpeg', 'png'])
            else:
                file = st.camera_input("Take a food picture")

        # Main content area
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if file:
                image_parts, display_image = self.process_image(file)
                if display_image:
                    st.image(display_image, caption="Your food image", use_column_width=True)

        with col2:
            if file:
                query = st.text_area("Ask about your food:", 
                    placeholder="Example: What ingredients can you identify? What are the nutritional benefits?")
                
                if query and image_parts:
                    with st.spinner("Analyzing your food..."):
                        response = self.get_ai_response(image_parts, query)
                        if response:
                            st.markdown("### Analysis Results")
                            st.markdown(response)
            else:
                st.info("Please upload or capture a food image to begin analysis.")

if __name__ == "__main__":
    app = FoodentApp()
    app.run()
