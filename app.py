import streamlit as st
import numpy as np
from PIL import Image
import io
import os
from dotenv import load_dotenv
import time
import json

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Food Analysis App",
    page_icon="🍽️",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

class FoodAnalyzer:
    def __init__(self):
        # In production, get API key from environment variables
        self.api_key = os.getenv('FOOD_API_KEY', 'default_key')
    
    def analyze_image(self, image):
        """
        Simulate food analysis from image
        In production, this would make actual API calls
        """
        # Simulate processing time
        time.sleep(2)
        
        # Mock response - in production, this would come from an API
        return {
            "name": "Detected Food Item",
            "calories": 250,
            "confidence": 0.92,
            "nutrients": {
                "protein": "12g",
                "carbs": "30g",
                "fat": "8g",
                "fiber": "4g"
            },
            "allergens": ["none detected"],
            "healthScore": 85
        }

def process_image(image_data):
    """Process image using PIL instead of OpenCV"""
    try:
        image = Image.open(image_data)
        return image
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def main():
    st.title("🍽️ Food Analysis App")
    
    # Initialize session state for storing analysis results
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Initialize FoodAnalyzer
    analyzer = FoodAnalyzer()
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📷 Camera Input", "📤 Upload Image"])
    
    with tab1:
        st.header("Take a Picture")
        camera_input = st.camera_input("Take a picture of your food")
        
        if camera_input:
            try:
                image = process_image(camera_input)
                if image:
                    st.image(image, caption="Captured Image", use_column_width=True)
                    
                    with st.spinner('Analyzing food...'):
                        results = analyzer.analyze_image(image)
                    st.session_state.analysis_results = results
                
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
    
    with tab2:
        st.header("Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a food image...",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of the food item"
        )
        
        if uploaded_file:
            try:
                image = process_image(uploaded_file)
                if image:
                    st.image(image, caption="Uploaded Image", use_column_width=True)
                    
                    with st.spinner('Analyzing food...'):
                        results = analyzer.analyze_image(image)
                    st.session_state.analysis_results = results
                
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
    
    # Display results if available
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        st.markdown("### Analysis Results")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Food Item", results["name"])
            st.metric("Calories", f"{results['calories']} kcal")
            st.metric("Health Score", f"{results['healthScore']}/100")
        
        with col2:
            st.metric("Confidence", f"{results['confidence']*100:.1f}%")
            st.metric("Allergens", ", ".join(results["allergens"]))
        
        # Nutrient information
        st.markdown("### Nutritional Information")
        nutrients = results["nutrients"]
        cols = st.columns(4)
        
        with cols[0]:
            st.metric("Protein", nutrients["protein"])
        with cols[1]:
            st.metric("Carbs", nutrients["carbs"])
        with cols[2]:
            st.metric("Fat", nutrients["fat"])
        with cols[3]:
            st.metric("Fiber", nutrients["fiber"])
        
        # Export results button
        if st.button("Export Results"):
            # Create JSON string
            results_json = json.dumps(results, indent=2)
            # Create download button
            st.download_button(
                label="Download JSON",
                data=results_json,
                file_name="food_analysis.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
