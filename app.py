import streamlit as st
import numpy as np
from PIL import Image
import io
import os
from dotenv import load_dotenv
import time
import json
import pandas as pd
from datetime import datetime
import base64
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Configure Streamlit page
st.set_page_config(
    page_title="Food Analysis",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_css():
    """Return custom CSS styling"""
    return """
    <style>
    /* Custom components */
    .feature-card {
        background: linear-gradient(90deg, #3498DB, #2980B9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
    }

    .dashboard-card {
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .animate-fade {
        animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .custom-button {
        background: #3498DB;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .custom-button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }

    .stButton>button {
        width: 100%;
    }

    .feature-card h1, .feature-card p {
        color: white !important;
    }
    </style>
    """

def process_image(image_input):
    """Process the uploaded image or camera input"""
    if image_input is None:
        return None
        
    try:
        image_bytes = image_input.getvalue()
        image = Image.open(io.BytesIO(image_bytes))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        max_size = 1024
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            
        return image
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

class FoodAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('FOOD_API_KEY', 'default_key')
        
    def analyze_image(self, image):
        """Enhanced food analysis with detailed metrics"""
        time.sleep(2)  # Simulating API call
        
        return {
            "name": "Detected Food Item",
            "calories": 250,
            "confidence": 0.92,
            "nutrients": {
                "protein": "12g",
                "carbs": "30g",
                "fat": "8g",
                "fiber": "4g",
                "sugar": "6g",
                "sodium": "400mg",
                "vitamins": {
                    "A": "10%",
                    "C": "15%",
                    "D": "5%",
                    "B12": "20%"
                }
            },
            "allergens": ["none detected"],
            "healthScore": 85,
            "sustainability_score": 78,
            "preparation_time": "15 mins",
            "portion_size": "1 serving",
            "dietary_tags": ["vegetarian", "low-fat", "high-protein"],
            "estimated_glycemic_index": 52
        }

def create_nutrition_radar_chart(nutrients):
    """Create a radar chart for nutritional information"""
    categories = list(nutrients.keys())[:5]
    values = [float(str(nutrients[cat]).rstrip('g%')) for cat in categories]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color='#3498DB'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values) * 1.2])
        ),
        showlegend=False
    )
    return fig

def create_health_gauge(score):
    """Create a gauge chart for health score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#3498DB"},
            'steps': [
                {'range': [0, 33], 'color': "#FF6B6B"},
                {'range': [33, 66], 'color': "#FFD93D"},
                {'range': [66, 100], 'color': "#6BCB77"}
            ]
        }
    ))
    return fig

def main():
    # Apply custom CSS
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings & History")
        
        # Language selector
        language = st.selectbox(
            "🌐 Language",
            ["English", "Español", "Français", "中文"],
            index=0
        )
        
        # Dark mode toggle
        if st.toggle("🌙 Dark Mode", st.session_state.dark_mode):
            st.session_state.dark_mode = True
            # Use Streamlit's native dark theme
            st.markdown("""
                <style>
                    [data-testid="stAppViewContainer"] {
                        background-color: #1a1a1a;
                    }
                </style>
            """, unsafe_allow_html=True)
        else:
            st.session_state.dark_mode = False
        
        # History section
        st.markdown("### 📚 Recent Analysis")
        for item in st.session_state.history[-5:]:
            with st.expander(f"{item['name']} - {item['date']}"):
                st.write(f"Calories: {item['calories']}")
                st.write(f"Health Score: {item['health_score']}")
    
    # Header
    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h1>🍽️ Advanced Food Analysis</h1>
            <p>AI-Powered Nutritional Analysis & Health Insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📸 Analysis",
        "📊 Dashboard",
        "🎯 Goals",
        "📚 Knowledge Base"
    ])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            input_method = st.radio(
                "Choose input method:",
                ["Camera", "Upload", "URL"],
                horizontal=True
            )
            
            if input_method == "Camera":
                image_input = st.camera_input("Take a photo of your food")
            elif input_method == "Upload":
                image_input = st.file_uploader("Upload food image", type=['png', 'jpg', 'jpeg'])
            else:
                image_url = st.text_input("Enter image URL")
                image_input = None
            
            if image_input:
                image = process_image(image_input)
                if image:
                    st.image(image, caption="Processed Image", use_column_width=True)
                    
                    with st.spinner("Analyzing your food..."):
                        analyzer = FoodAnalyzer()
                        results = analyzer.analyze_image(image)
                        
                        history_item = {
                            'name': results['name'],
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                            'calories': results['calories'],
                            'health_score': results['healthScore']
                        }
                        st.session_state.history.append(history_item)
                    
                    # Results display
                    with st.container():
                        st.markdown("### 📊 Analysis Results")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Calories", f"{results['calories']} kcal")
                        with col2:
                            st.metric("Health Score", f"{results['healthScore']}/100")
                        with col3:
                            st.metric("Sustainability", f"{results['sustainability_score']}/100")
                        
                        st.markdown("### 🍎 Nutritional Breakdown")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.plotly_chart(
                                create_nutrition_radar_chart(results['nutrients']),
                                use_container_width=True
                            )
                        
                        with col2:
                            st.plotly_chart(
                                create_health_gauge(results['healthScore']),
                                use_container_width=True
                            )
                        
                        st.markdown("### 🏷️ Details")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### Dietary Tags")
                            for tag in results['dietary_tags']:
                                st.markdown(f"- {tag}")
                        
                        with col2:
                            st.markdown("#### Vitamins & Minerals")
                            for vitamin, value in results['nutrients']['vitamins'].items():
                                st.markdown(f"- Vitamin {vitamin}: {value}")
                        
                        st.markdown("### 💾 Export Options")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("Generate PDF Report"):
                                st.success("PDF report generated! (Demo)")
                        
                        with col2:
                            if st.button("Export Raw Data (JSON)"):
                                results_json = json.dumps(results, indent=2)
                                st.download_button(
                                    "Download JSON",
                                    results_json,
                                    file_name="food_analysis.json",
                                    mime="application/json"
                                )
    
    with tab2:
        st.markdown("### 📊 Nutrition Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Analyses", len(st.session_state.history))
        with col2:
            avg_calories = sum(item['calories'] for item in st.session_state.history) / len(st.session_state.history) if st.session_state.history else 0
            st.metric("Avg. Calories", f"{avg_calories:.0f}")
        with col3:
            avg_health = sum(item['health_score'] for item in st.session_state.history) / len(st.session_state.history) if st.session_state.history else 0
            st.metric("Avg. Health Score", f"{avg_health:.1f}")
        with col4:
            st.metric("Favorite Foods", len(st.session_state.favorites))
        
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            fig = px.line(df, x='date', y='calories', title='Calorie Intake Trend')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎯 Set Health Goals")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Daily Targets")
            calories_goal = st.number_input("Daily Calories Target", 1000, 5000, 2000)
            protein_goal = st.number_input("Daily Protein Goal (g)", 0, 200, 60)
            water_goal = st.number_input("Daily Water Goal (L)", 0.0, 5.0, 2.0)
        
        with col2:
            st.markdown("#### Today's Progress")
            st.progress(0.7, "Calories (70%)")
            st.progress(0.5, "Protein (50%)")
            st.progress(0.3, "Water (30%)")
    
    with tab4:
        st.markdown("### 📚 Nutrition Knowledge Base")
        
        st.text_input("Search nutrition information...", placeholder="Type to search...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("🥑 Common Foods Nutrition Facts"):
                st.markdown("""
                    - Banana (105 calories, 27g carbs)
                    - Apple (95 calories, 25g carbs)
                    - Chicken Breast (165 calories, 31g protein)
                    - Salmon (208 calories, 22g protein)
                    - Avocado (160 calories, 15g fat)
                """)
        
        with col2:
            with st.expander("🏃‍♂️ Exercise Equivalents"):
                st.markdown("""
                    - 100 calories = 20 min walking
                    - 200 calories = 30 min cycling
                    - 300 calories = 30 min running
                    - 400 calories = 45 min swimming
                    - 500 calories = 60 min HIIT
                """)

if __name__ == "__main__":
    main()
