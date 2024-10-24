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
    layout="wide",  # Changed to wide layout for better spacing
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for modern design
st.markdown("""
    <style>
    /* Main container styling */
    .main > div {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #2C3E50, #3498DB);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Card styling */
    .stCard {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Upload box styling */
    .upload-box {
        border: 2px dashed #3498DB;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: #F8FAFC;
        transition: all 0.3s ease;
    }
    
    .upload-box:hover {
        border-color: #2980B9;
        background: #EBF5FB;
    }
    
    /* Results section styling */
    .results-container {
        background: #F8FAFC;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
    }
    
    /* Metric cards styling */
    .css-1r6slb0 {
        background: white !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Nutrient cards styling */
    .nutrient-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F8FAFC;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px;
        background: white;
        padding: 0 16px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: #3498DB;
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        background: #3498DB;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #2980B9;
        transform: translateY(-2px);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #3498DB !important;
    }
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Header with gradient background
    st.markdown('''
        <div class="main-header">
            <h1>🍽️ Smart Food Analysis</h1>
            <p>Upload or take a photo of your food to get instant nutritional analysis</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Create container for main content
    main_container = st.container()
    
    with main_container:
        # Create tabs with enhanced styling
        tab1, tab2 = st.tabs([
            "📸 Camera Capture",
            "📤 Upload Image"
        ])
        
        with tab1:
            st.markdown('''
                <div class="stCard">
                    <h3>Take a Photo</h3>
                    <p>Position your food in the frame and take a clear photo</p>
                </div>
            ''', unsafe_allow_html=True)
            camera_input = st.camera_input("", key="camera")
            
            if camera_input:
                process_and_display_results(camera_input)
        
        with tab2:
            st.markdown('''
                <div class="stCard">
                    <h3>Upload Food Image</h3>
                    <p>Select a clear image of your food for analysis</p>
                </div>
            ''', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "",
                type=['png', 'jpg', 'jpeg'],
                key="uploader"
            )
            
            if uploaded_file:
                process_and_display_results(uploaded_file)

def process_and_display_results(image_data):
    try:
        # Process image
        image = process_image(image_data)
        if image:
            # Display image in card
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.image(image, caption="", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Analysis spinner
            with st.spinner('Analyzing your food...'):
                analyzer = FoodAnalyzer()
                results = analyzer.analyze_image(image)
            
            # Display results in styled container
            st.markdown('<div class="results-container animate-fade-in">', unsafe_allow_html=True)
            
            # Main metrics
            st.markdown("### 📊 Analysis Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Food Item", results["name"])
            with col2:
                st.metric("Calories", f"{results['calories']} kcal")
            with col3:
                st.metric("Health Score", f"{results['healthScore']}/100")
            
            # Nutrients section
            st.markdown("### 🍎 Nutritional Breakdown")
            st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">', unsafe_allow_html=True)
            
            # Create nutrient cards
            cols = st.columns(4)
            nutrients = results["nutrients"]
            
            nutrient_colors = {
                "Protein": "#FF6B6B",
                "Carbs": "#4ECDC4",
                "Fat": "#45B7D1",
                "Fiber": "#96CEB4"
            }
            
            for col, (nutrient, value) in zip(cols, nutrients.items()):
                col.markdown(f'''
                    <div style="background: {nutrient_colors[nutrient]}20; padding: 1rem; border-radius: 10px; text-align: center;">
                        <h4 style="color: {nutrient_colors[nutrient]}; margin: 0;">{nutrient}</h4>
                        <p style="font-size: 1.5rem; margin: 0.5rem 0;">{value}</p>
                    </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export section
            st.markdown("### 💾 Export Data")
            results_json = json.dumps(results, indent=2)
            st.download_button(
                label="Download Analysis Report",
                data=results_json,
                file_name="food_analysis.json",
                mime="application/json"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()
