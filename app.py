import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64
from pathlib import Path
import io

# Configure Streamlit page with modern UI
st.set_page_config(
    page_title="AI Food Analyzer Pro",
    page_icon="🍽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define CSS styles
STYLES = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Main Container Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: transparent;
    }
    
    /* Header Styles */
    h1 {
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    h2, h3 {
        color: #334155;
        font-weight: 600;
        margin: 1.5rem 0;
    }
    
    /* Card Styles */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
    }
    
    /* Metric Card Styles */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Health Score Indicators */
    .health-score-high {
        color: #10B981;
        font-weight: 700;
    }
    
    .health-score-medium {
        color: #F59E0B;
        font-weight: 700;
    }
    
    .health-score-low {
        color: #EF4444;
        font-weight: 700;
    }
    
    /* Progress Bar Styles */
    .stProgress > div > div {
        background-color: #3B82F6;
        height: 8px;
        border-radius: 4px;
    }
    
    /* Insight Card Styles */
    .insight-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid #3B82F6;
        transition: transform 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-3px);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        border-right: 1px solid #e2e8f0;
    }
    
    /* Button Styles */
    .stButton>button {
        background: linear-gradient(45deg, #3B82F6, #60A5FA);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #2563EB, #3B82F6);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    /* File Upload Styles */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 2px dashed #3B82F6;
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.9);
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        color: #1e293b;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3B82F6;
        color: white;
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .stSpinner {
        animation: pulse 1.5s infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .metric-card {
            margin: 0.5rem 0;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .custom-card {
            padding: 1rem;
        }
    }
    </style>
"""

class AdvancedFoodAnalyzer:
    def __init__(self):
        # Enhanced food database
        self.food_database = {
            'red_dominant': {
                'name': 'Tomato-based/Red Meat Dish',
                'calories': 250,
                'nutrients': {
                    'protein': 8.0,
                    'carbs': 30.0,
                    'fat': 12.0,
                    'fiber': 4.0,
                    'sugar': 6.0,
                    'sodium': 500.0,
                    'vitamins': {
                        'A': 25,
                        'C': 35,
                        'B12': 40,
                        'D': 15,
                        'E': 20
                    },
                    'minerals': {
                        'Iron': 15,
                        'Zinc': 20,
                        'Magnesium': 10
                    }
                },
                'allergens': ['none'],
                'healthScore': 75,
                'sustainability_score': 65,
                'preparation_time': '30-45 mins',
                'cooking_method': ['Grilling', 'Baking', 'Pan-frying'],
                'dietary_tags': ['High-protein', 'Gluten-free']
            },
            'green_dominant': {
                'name': 'Vegetable/Salad Dish',
                'calories': 150,
                'nutrients': {
                    'protein': 5.0,
                    'carbs': 20.0,
                    'fat': 8.0,
                    'fiber': 6.0,
                    'sugar': 4.0,
                    'sodium': 300.0,
                    'vitamins': {
                        'A': 40,
                        'C': 60,
                        'K': 45,
                        'E': 30,
                        'B6': 25
                    },
                    'minerals': {
                        'Iron': 10,
                        'Calcium': 15,
                        'Potassium': 20
                    }
                },
                'allergens': ['none'],
                'healthScore': 90,
                'sustainability_score': 95,
                'preparation_time': '15-20 mins',
                'cooking_method': ['Raw', 'Steaming', 'Light sautéing'],
                'dietary_tags': ['Vegan', 'Low-calorie', 'High-fiber']
            }
        }

    def analyze_image(self, image):
        """
        Analyze food image and return nutritional information
        """
        try:
            img_array = np.array(image)
            
            if len(img_array.shape) == 3 and img_array.shape[-1] == 4:
                img_array = img_array[:,:,:3]
            elif len(img_array.shape) == 2:
                img_array = np.stack((img_array,) * 3, axis=-1)
                
            pixels = img_array.reshape(-1, 3)
            
            def categorize_color(pixel):
                r, g, b = pixel
                if max(r, g, b) < 30:
                    return 'black'
                elif min(r, g, b) > 225:
                    return 'white'
                elif r > max(g, b) + 20:
                    return 'red'
                elif g > max(r, b) + 20:
                    return 'green'
                elif b > max(r, g) + 20:
                    return 'blue'
                elif abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20:
                    return 'gray'
                elif r > 150 and g > 150:
                    return 'yellow'
                else:
                    return 'brown'
                    
            color_counts = {}
            total_pixels = len(pixels)
            
            for pixel in pixels:
                color = categorize_color(pixel)
                color_counts[color] = color_counts.get(color, 0) + 1
                
            color_distribution = {
                color: f"{(count/total_pixels * 100):.1f}%"
                for color, count in color_counts.items()
            }
            
            dominant_color = max(color_counts.items(), key=lambda x: x[1])[0]
            food_info = self.food_database.get(f'{dominant_color}_dominant', 
                                             self.food_database['red_dominant'])
            
            formatted_nutrients = {
                'protein': f"{food_info['nutrients']['protein']}g",
                'carbs': f"{food_info['nutrients']['carbs']}g",
                'fat': f"{food_info['nutrients']['fat']}g",
                'fiber': f"{food_info['nutrients']['fiber']}g",
                'sugar': f"{food_info['nutrients']['sugar']}g",
                'sodium': f"{food_info['nutrients']['sodium']}mg"
            }
            
            formatted_nutrients['vitamins'] = food_info['nutrients']['vitamins']
            formatted_nutrients['minerals'] = food_info['nutrients']['minerals']
            
            results = {
                'name': food_info['name'],
                'calories': food_info['calories'],
                'nutrients': formatted_nutrients,
                'allergens': food_info['allergens'],
                'healthScore': food_info['healthScore'],
                'sustainability_score': food_info['sustainability_score'],
                'preparation_time': food_info['preparation_time'],
                'cooking_method': food_info['cooking_method'],
                'color_distribution': color_distribution,
                'dietary_tags': food_info.get('dietary_tags', [])
            }
            
            return results
            
        except Exception as e:
            st.error(f"Error analyzing image: {str(e)}")
            return {
                "error": "Error analyzing image",
                "details": str(e)
            }

    def generate_nutrition_insights(self, food_info):
        insights = []
        
        protein = float(food_info['nutrients']['protein'].rstrip('g'))
        if protein > 15:
            insights.append({
                'type': 'positive',
                'icon': '💪',
                'message': 'High in protein - great for muscle maintenance and satiety'
            })
        
        fiber = float(food_info['nutrients']['fiber'].rstrip('g'))
        if fiber > 5:
            insights.append({
                'type': 'positive',
                'icon': '🌾',
                'message': 'Good source of fiber - supports digestive health'
            })
        
        total_nutrients = protein + float(food_info['nutrients']['carbs'].rstrip('g'))
        if total_nutrients > 0:
            balance_score = abs(0.5 - (protein / total_nutrients)) * 100
            
            if balance_score < 20:
                insights.append({
                    'type': 'positive',
                    'icon': '⚖️',
                    'message': 'Well-balanced macronutrient profile'
                })
        
        # Additional health insights based on sustainability
        if food_info.get('sustainability_score', 0) > 80:
            insights.append({
                'type': 'positive',
                'icon': '🌱',
                'message': 'Environmentally friendly choice - low carbon footprint'
            })
            
        # Vitamin and mineral insights
        vitamins = food_info['nutrients'].get('vitamins', {})
        if any(v > 30 for v in vitamins.values()):
            insights.append({
                'type': 'positive',
                'icon': '🍎',
                'message': 'Rich in essential vitamins for optimal health'
            })
            
        return insights

    def create_nutrient_radar_chart(self, nutrients):
        values = []
        labels = []
        
        for key, value in list(nutrients.items())[:5]:
            if isinstance(value, str) and value.rstrip('g').replace('.', '').isdigit():
                values.append(float(value.rstrip('g')))
                labels.append(key)
        
        if not values:
            return None
            
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name='Nutrients'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) * 1.2]
                )
            ),
            showlegend=False,
            margin=dict(t=30, b=30),
            height=400
        )
        
        return fig
   
def main():
    st.title("🍽 AI Food Analyzer Pro")
    st.markdown("### Intelligent Food Analysis & Nutrition Insights")
    
    analyzer = AdvancedFoodAnalyzer()
    
    # Create sidebar for settings and filters
    with st.sidebar:
        st.header("Analysis Settings")
        analysis_mode = st.selectbox(
            "Analysis Mode",
            ["Standard", "Detailed", "Professional"],
            help="Choose the depth of analysis"
        )
        
        st.subheader("Dietary Preferences")
        dietary_prefs = st.multiselect(
            "Select dietary preferences",
            ["Vegetarian", "Vegan", "Gluten-free", "Keto", "Low-carb"]
        )
        
        st.subheader("Health Goals")
        health_goal = st.radio(
            "Primary health goal",
            ["Weight management", "Muscle gain", "General health", "Athletic performance"]
        )
    
    # Main content area with two columns
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("### 📸 Image Input")
        input_method = st.radio("Choose input method:", ["📷 Camera", "📤 Upload"])
        
        if input_method == "📷 Camera":
            image_input = st.camera_input(
                "Take a picture of your food",
                help="Position your food in good lighting for best results"
            )
        else:
            image_input = st.file_uploader(
                "Choose a food image...",
                type=['png', 'jpg', 'jpeg'],
                help="Upload a clear image of your food"
            )
        
        if image_input:
            image = Image.open(image_input)
            st.image(image, caption="Input Image", use_column_width=True)
    
    with col2:
        if image_input:
            with st.spinner('Analyzing food with AI...'):
                results = analyzer.analyze_image(image)
                
                if "error" in results:
                    st.error(results["error"])
                    st.write(results["details"])
                else:
                    st.markdown("### 📊 Analysis Results")
                    
                    # Create modern metric cards
                    metrics_container = st.container()
                    with metrics_container:
                        m1, m2, m3 = st.columns(3)
                        with m1:
                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <h4>Food Type</h4>
                                    <h2>{results['name']}</h2>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        with m2:
                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <h4>Calories</h4>
                                    <h2>{results['calories']} kcal</h2>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        with m3:
                            health_score_class = (
                                'health-score-high' if results['healthScore'] >= 80
                                else 'health-score-medium' if results['healthScore'] >= 60
                                else 'health-score-low'
                            )
                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <h4>Health Score</h4>
                                    <h2 class="{health_score_class}">{results['healthScore']}/100</h2>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    
                    # Nutrient visualization
                    st.markdown("### 📈 Nutrient Distribution")
                    nutrient_fig = analyzer.create_nutrient_radar_chart(results['nutrients'])
                    st.plotly_chart(nutrient_fig, use_container_width=True)
                    
                    # Color distribution with modern progress bars
                    st.markdown("### 🎨 Visual Analysis")
                    color_cols = st.columns(2)
                    for idx, (color, percentage) in enumerate(results['color_distribution'].items()):
                        with color_cols[idx % 2]:
                            st.markdown(f"**{color.title()}**")
                            st.progress(float(percentage.strip('%')) / 100)
                    
                    # Nutrition insights
                    st.markdown("### 💡 Smart Insights")
                    insights = analyzer.generate_nutrition_insights(results)
                    for insight in insights:
                        st.markdown(
                            f"""
                            <div class="insight-card">
                                <h4>{insight['icon']} {insight['message']}</h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    # Detailed analysis in expandable sections
                    with st.expander("🔍 Detailed Analysis"):
                        tabs = st.tabs([
                            "Nutrients",
                            "Allergens",
                            "Sustainability",
                            "Preparation"
                        ])
                        
                        with tabs[0]:
                            st.markdown("#### Detailed Nutrient Breakdown")
                            for nutrient, value in results['nutrients'].items():
                                if isinstance(value, dict):
                                    st.markdown(f"**{nutrient.title()}**")
                                    for sub_nutrient, sub_value in value.items():
                                        st.markdown(f"- {sub_nutrient}: {sub_value}")
                                else:
                                    st.markdown(f"**{nutrient.title()}:** {value}")
                        
                        with tabs[1]:
                            st.markdown("#### Allergen Information")
                            st.markdown(", ".join(results['allergens']).title())
                        
                        with tabs[2]:
                            st.markdown("#### Sustainability Score")
                            st.progress(results['sustainability_score'] / 100)
                            
                        with tabs[3]:
                            if 'preparation_time' in results:
                                st.markdown(f"**Preparation Time:** {results['preparation_time']}")
                            if 'cooking_method' in results:
                                st.markdown("**Suggested Cooking Methods:**")
                                for method in results['cooking_method']:
                                    st.markdown(f"- {method}")

if __name__ == "__main__":
    main()
