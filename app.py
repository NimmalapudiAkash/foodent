import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px

# Configure Streamlit page with enhanced custom CSS
st.set_page_config(
    page_title="Smart Food Analyzer Pro",
    page_icon="🍽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for modern UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    
    .st-emotion-cache-18ni7ap {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .st-emotion-cache-18ni7ap:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    h1 {
        color: #1e3a8a;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h3 {
        color: #334155;
        margin: 1.5rem 0;
        font-weight: 600;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 15px 0;
        border: 1px solid #e2e8f0;
    }
    
    .stProgress > div > div > div > div {
        background-color: #3b82f6;
    }
    
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    .nutrition-chart {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8fafc;
    }
    
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    
    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

class EnhancedFoodAnalyzer(AdvancedFoodAnalyzer):
    def __init__(self):
        super().__init__()
        # Add more detailed nutritional information
        for food_type in self.food_database:
            self.food_database[food_type].update({
                'minerals': {
                    'iron': np.random.randint(10, 30),
                    'calcium': np.random.randint(15, 35),
                    'magnesium': np.random.randint(10, 25),
                    'zinc': np.random.randint(8, 20)
                },
                'meal_timing': self._get_meal_recommendations(),
                'portion_size': self._calculate_portion_size(),
                'preparation_time': np.random.randint(15, 45),
                'cooking_method': self._get_cooking_recommendations(),
                'seasonal_rating': np.random.randint(70, 100)
            })
    
    def _get_meal_recommendations(self):
        return {
            'breakfast': np.random.randint(0, 100),
            'lunch': np.random.randint(0, 100),
            'dinner': np.random.randint(0, 100),
            'snack': np.random.randint(0, 100)
        }
    
    def _calculate_portion_size(self):
        return {
            'recommended_grams': np.random.randint(200, 400),
            'servings': np.random.randint(1, 4)
        }
    
    def _get_cooking_recommendations(self):
        methods = ['Baking', 'Grilling', 'Steaming', 'Sautéing', 'Raw']
        return np.random.choice(methods, 2, replace=False).tolist()

    def generate_nutrition_chart(self, nutrients):
        """Generate an interactive radar chart for nutritional data"""
        categories = list(nutrients.keys())
        values = [float(str(v).rstrip('g%')) for v in nutrients.values() if isinstance(v, (str, int, float))]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line_color='#3b82f6'
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

def create_meal_timing_chart(timing_data):
    """Create a bar chart for meal timing recommendations"""
    fig = go.Figure(data=[
        go.Bar(
            x=list(timing_data.keys()),
            y=list(timing_data.values()),
            marker_color=['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe']
        )
    ])
    
    fig.update_layout(
        title="Meal Timing Suitability",
        yaxis_title="Suitability Score",
        height=300
    )
    return fig

def main():
    st.title("🍽 Smart Food Analyzer Pro")
    
    # Initialize session state for history
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    # Sidebar for settings and history
    with st.sidebar:
        st.header("📊 Analysis Settings")
        
        analysis_mode = st.selectbox(
            "Analysis Mode",
            ["Standard", "Detailed", "Professional"],
            help="Choose the depth of analysis"
        )
        
        show_advanced = st.checkbox("Show Advanced Metrics", value=True)
        
        st.markdown("---")
        st.header("📜 Analysis History")
        for hist in st.session_state.analysis_history[-5:]:
            with st.expander(f"{hist['timestamp']} - {hist['name']}"):
                st.write(f"Calories: {hist['calories']} kcal")
                st.write(f"Health Score: {hist['healthScore']}/100")
    
    analyzer = EnhancedFoodAnalyzer()
    
    # Main content area
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("### 📸 Image Input")
        tab1, tab2 = st.tabs(["📷 Camera", "📤 Upload"])
        
        with tab1:
            image_input = st.camera_input("Take a picture of your food")
        with tab2:
            image_input = st.file_uploader("Choose a food image...", type=['png', 'jpg', 'jpeg'])
        
        if image_input:
            image = Image.open(image_input)
            st.image(image, caption="Input Image", use_column_width=True)
    
    with col2:
        if image_input:
            with st.spinner('Analyzing your food with AI...'):
                results = analyzer.analyze_image(image)
                
                if "error" in results:
                    st.error(results["error"])
                    st.write(results["details"])
                else:
                    # Add to history
                    st.session_state.analysis_history.append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        **results
                    })
                    
                    # Main metrics
                    st.markdown("### 📊 Analysis Results")
                    cols = st.columns(4)
                    metrics = [
                        ("Food Type", results['name'], ""),
                        ("Calories", results['calories'], "kcal"),
                        ("Health Score", results['healthScore'], "/100"),
                        ("Sustainability", results['sustainability_score'], "/100")
                    ]
                    
                    for col, (label, value, unit) in zip(cols, metrics):
                        with col:
                            st.metric(label, f"{value}{unit}")
                    
                    # Tabs for different aspects of analysis
                    tab1, tab2, tab3 = st.tabs(["📊 Nutrition", "🎨 Visual Analysis", "🔍 Details"])
                    
                    with tab1:
                        if show_advanced:
                            nutrition_chart = analyzer.generate_nutrition_chart(results['nutrients'])
                            st.plotly_chart(nutrition_chart, use_container_width=True)
                        
                        with st.expander("📋 Detailed Nutrients"):
                            for category, values in results['nutrients'].items():
                                if isinstance(values, dict):
                                    st.write(f"**{category.title()}**")
                                    for name, value in values.items():
                                        st.write(f"- {name}: {value}")
                                else:
                                    st.write(f"**{category.title()}:** {values}")
                    
                    with tab2:
                        st.markdown("##### 🎨 Color Distribution")
                        for color, percentage in results['color_distribution'].items():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.progress(float(percentage.strip('%')) / 100)
                            with col2:
                                st.write(f"{percentage}")
                    
                    with tab3:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("##### ⏱️ Preparation")
                            st.write(f"Cooking Time: {results['preparation_time']} minutes")
                            st.write("Recommended Methods:")
                            for method in results['cooking_method']:
                                st.write(f"- {method}")
                        
                        with col2:
                            st.markdown("##### 🍽️ Portion Info")
                            st.write(f"Recommended serving: {results['portion_size']['recommended_grams']}g")
                            st.write(f"Servings per dish: {results['portion_size']['servings']}")
                        
                        # Meal timing chart
                        st.markdown("##### ⌚ Best Time to Eat")
                        timing_chart = create_meal_timing_chart(results['meal_timing'])
                        st.plotly_chart(timing_chart, use_container_width=True)
                        
                        # Additional information
                        with st.expander("🏷️ Additional Information"):
                            st.write(f"Analysis Version: {results['analysis_version']}")
                            st.write(f"Confidence Score: {results['confidence_score']}")
                            st.write(f"Seasonal Rating: {results['seasonal_rating']}/100")
                            st.write("Allergens:", ", ".join(results['allergens']).title())

if __name__ == "__main__":
    main()
