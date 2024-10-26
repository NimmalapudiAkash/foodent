import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Configure Streamlit page with modern UI
st.set_page_config(
    page_title="AI Food Analyzer Pro",
    page_icon="🍽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design principles
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .block-container {
        padding: 2rem 3rem;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin: 1rem 0;
        border: 1px solid #f0f0f0;
    }
    
    .health-score-high {
        color: #10B981;
    }
    
    .health-score-medium {
        color: #F59E0B;
    }
    
    .health-score-low {
        color: #EF4444;
    }
    
    .stProgress {
        height: 10px;
        border-radius: 5px;
    }
    
    .nutrition-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        padding: 1rem;
        background: white;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    .insight-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)

class AdvancedFoodAnalyzer:
    def __init__(self):
        # Enhanced food database with more detailed nutritional information
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
            # ... [Previous database entries remain the same]
        }
        
        # Add more sophisticated food categories here...

    def generate_nutrition_insights(self, food_info):
        """Generate personalized nutrition insights based on analysis"""
        insights = []
        
        # Protein analysis
        protein = float(food_info['nutrients']['protein'].rstrip('g'))
        if protein > 15:
            insights.append({
                'type': 'positive',
                'icon': '💪',
                'message': 'High in protein - great for muscle maintenance and satiety'
            })
        
        # Fiber analysis
        fiber = float(food_info['nutrients']['fiber'].rstrip('g'))
        if fiber > 5:
            insights.append({
                'type': 'positive',
                'icon': '🌾',
                'message': 'Good source of fiber - supports digestive health'
            })
        
        # Calculate balance score
        total_nutrients = protein + float(food_info['nutrients']['carbs'].rstrip('g'))
        balance_score = abs(0.5 - (protein / total_nutrients)) * 100
        
        if balance_score < 20:
            insights.append({
                'type': 'positive',
                'icon': '⚖️',
                'message': 'Well-balanced macronutrient profile'
            })
        
        return insights

    def create_nutrient_radar_chart(self, nutrients):
        """Create an interactive radar chart for nutrient distribution"""
        # Extract nutrient values and convert to numeric
        values = [float(v.rstrip('g')) for v in list(nutrients.values())[:5]]
        labels = list(nutrients.keys())[:5]
        
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
                )),
            showlegend=False,
            height=400
        )
        
        return fig

    # ... [Previous analysis methods remain the same]
def analyze_image(self, image):
    """
    Analyze food image and return nutritional information
    
    Args:
        image (PIL.Image): Input image to analyze
        
    Returns:
        dict: Analysis results including nutritional information
    """
    try:
        # Convert image to numpy array
        img_array = np.array(image)
        
        # Basic color analysis
        # Convert to RGB if image is in RGBA
        if img_array.shape[-1] == 4:
            img_array = img_array[:,:,:3]
            
        # Calculate color distribution
        pixels = img_array.reshape(-1, 3)
        
        # Simple color categorization
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
        
        # Determine dominant color
        dominant_color = max(color_counts.items(), key=lambda x: x[1])[0]
        
        # Map dominant color to food type from database
        if dominant_color in ['red']:
            food_info = self.food_database['red_dominant']
        else:
            # Default case if color not recognized
            food_info = self.food_database['red_dominant']  # Using as default for example
        
        # Format nutrients with units
        formatted_nutrients = {
            'protein': f"{food_info['nutrients']['protein']}g",
            'carbs': f"{food_info['nutrients']['carbs']}g",
            'fat': f"{food_info['nutrients']['fat']}g",
            'fiber': f"{food_info['nutrients']['fiber']}g",
            'sugar': f"{food_info['nutrients']['sugar']}g",
            'vitamins': food_info['nutrients']['vitamins'],
            'minerals': food_info['nutrients']['minerals']
        }
        
        # Compile results
        results = {
            'name': food_info['name'],
            'calories': food_info['calories'],
            'nutrients': formatted_nutrients,
            'allergens': food_info['allergens'],
            'healthScore': food_info['healthScore'],
            'sustainability_score': food_info['sustainability_score'],
            'preparation_time': food_info['preparation_time'],
            'cooking_method': food_info['cooking_method'],
            'color_distribution': color_distribution
        }
        
        return results
        
    except Exception as e:
        return {
            "error": "Error analyzing image",
            "details": str(e)
        }
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
