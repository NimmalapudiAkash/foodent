import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

# Configure Streamlit page with custom CSS
st.set_page_config(
    page_title="Advanced Food Analyzer",
    page_icon="🍽",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main {
        background-color: #f8f9fa;
    }
    .st-emotion-cache-18ni7ap {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h3 {
        color: #34495e;
        margin-top: 20px;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

class AdvancedFoodAnalyzer:
    def __init__(self):
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
                        'B12': 40
                    }
                },
                'allergens': ['none'],
                'healthScore': 75,
                'sustainability_score': 65
            },
            'green_dominant': {
                'name': 'Salad/Vegetables',
                'calories': 150,
                'nutrients': {
                    'protein': 5.0,
                    'carbs': 15.0,
                    'fat': 7.0,
                    'fiber': 8.0,
                    'sugar': 3.0,
                    'sodium': 200.0,
                    'vitamins': {
                        'A': 80,
                        'C': 90,
                        'K': 70
                    }
                },
                'allergens': ['none'],
                'healthScore': 95,
                'sustainability_score': 90
            },
            'brown_dominant': {
                'name': 'Bread/Grain Dish',
                'calories': 350,
                'nutrients': {
                    'protein': 12.0,
                    'carbs': 45.0,
                    'fat': 15.0,
                    'fiber': 3.0,
                    'sugar': 2.0,
                    'sodium': 400.0,
                    'vitamins': {
                        'B1': 60,
                        'B3': 45,
                        'E': 30
                    }
                },
                'allergens': ['wheat', 'gluten'],
                'healthScore': 65,
                'sustainability_score': 75
            },
            'light_dominant': {
                'name': 'Rice/Pasta Dish',
                'calories': 320,
                'nutrients': {
                    'protein': 10.0,
                    'carbs': 50.0,
                    'fat': 8.0,
                    'fiber': 2.0,
                    'sugar': 1.0,
                    'sodium': 300.0,
                    'vitamins': {
                        'B1': 40,
                        'B6': 35,
                        'E': 20
                    }
                },
                'allergens': ['wheat'],
                'healthScore': 70,
                'sustainability_score': 70
            },
            'mixed': {
                'name': 'Mixed Dish',
                'calories': 400,
                'nutrients': {
                    'protein': 15.0,
                    'carbs': 40.0,
                    'fat': 20.0,
                    'fiber': 5.0,
                    'sugar': 4.0,
                    'sodium': 600.0,
                    'vitamins': {
                        'A': 45,
                        'C': 40,
                        'B12': 35,
                        'D': 30
                    }
                },
                'allergens': ['may contain multiple allergens'],
                'healthScore': 80,
                'sustainability_score': 60
            }
        }

    def analyze_colors(self, image):
        """Enhanced color analysis with more precise binning"""
        img_rgb = image.convert('RGB')
        pixels = np.array(img_rgb)
        
        # Flatten the pixel array
        pixels_flat = pixels.reshape(-1, 3)
        
        # Enhanced color categorization with HSV conversion
        hsv_pixels = np.array([self._rgb_to_hsv(*pixel) for pixel in pixels_flat])
        
        # More precise color binning
        red_mask = (hsv_pixels[:, 0] >= 0.95) | (hsv_pixels[:, 0] <= 0.05)
        green_mask = (hsv_pixels[:, 0] >= 0.25) & (hsv_pixels[:, 0] <= 0.40)
        brown_mask = ((hsv_pixels[:, 0] >= 0.05) & (hsv_pixels[:, 0] <= 0.15) & 
                     (hsv_pixels[:, 1] >= 0.2) & (hsv_pixels[:, 2] <= 0.8))
        light_mask = (hsv_pixels[:, 2] >= 0.8)
        
        total_pixels = len(pixels_flat)
        
        color_dist = {
            'red': (np.sum(red_mask) / total_pixels) * 100,
            'green': (np.sum(green_mask) / total_pixels) * 100,
            'brown': (np.sum(brown_mask) / total_pixels) * 100,
            'light': (np.sum(light_mask) / total_pixels) * 100
        }
        
        return color_dist

    def _rgb_to_hsv(self, r, g, b):
        """Convert RGB to HSV color space"""
        r, g, b = r/255.0, g/255.0, b/255.0
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        diff = cmax - cmin

        if cmax == cmin:
            h = 0
        elif cmax == r:
            h = (60 * ((g-b)/diff) + 360) % 360
        elif cmax == g:
            h = (60 * ((b-r)/diff) + 120) % 360
        else:
            h = (60 * ((r-g)/diff) + 240) % 360

        s = 0 if cmax == 0 else diff/cmax
        v = cmax

        return h/360, s, v

    def is_likely_food(self, image):
        """Enhanced food detection with texture analysis"""
        gray_img = np.array(image.convert('L'))
        
        # Calculate texture features
        texture_stats = stats.describe(gray_img.flatten())
        std_dev = np.sqrt(texture_stats.variance)
        mean_val = texture_stats.mean
        
        # Enhanced heuristics
        texture_complexity = np.mean(np.abs(np.diff(gray_img)))
        edge_density = self._calculate_edge_density(gray_img)
        
        return (std_dev > 20 and 
                30 < mean_val < 225 and 
                texture_complexity > 5 and 
                edge_density > 0.1)

    def _calculate_edge_density(self, gray_img):
        """Calculate edge density using simple gradient"""
        gradient_x = np.diff(gray_img, axis=1)
        gradient_y = np.diff(gray_img, axis=0)
        
        edge_pixels = np.sum(np.abs(gradient_x) > 30) + np.sum(np.abs(gradient_y) > 30)
        total_pixels = gray_img.size
        
        return edge_pixels / total_pixels

    def get_dominant_type(self, color_dist):
        """Enhanced food type determination with weighted analysis"""
        # Apply weights to different colors based on typical food compositions
        weights = {'red': 1.2, 'green': 1.3, 'brown': 1.1, 'light': 1.0}
        weighted_dist = {k: v * weights[k] for k, v in color_dist.items()}
        
        max_color = max(weighted_dist.items(), key=lambda x: x[1])
        
        # More nuanced threshold for mixed classification
        if max_color[1] < 25:  # Adjusted threshold
            return 'mixed'
        
        return f"{max_color[0]}_dominant"

    def analyze_image(self, image):
        """Enhanced image analysis with confidence scores"""
        try:
            if not self.is_likely_food(image):
                return {
                    "error": "No food detected in image",
                    "details": "The image doesn't appear to contain food",
                    "confidence": 0.0
                }
            
            color_dist = self.analyze_colors(image)
            food_type = self.get_dominant_type(color_dist)
            
            # Calculate confidence score
            max_color_percent = max(color_dist.values())
            confidence = min(max_color_percent / 30, 1.0)  # Normalize to 0-1
            
            # Get base food info
            food_info = self.food_database[food_type].copy()
            
            # Add enhanced analysis metadata
            food_info.update({
                "color_distribution": {k: f"{v:.2f}%" for k, v in color_dist.items()},
                "confidence_score": f"{confidence:.2f}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "analysis_version": "2.0"
            })
            
            return food_info
            
        except Exception as e:
            return {
                "error": f"Error analyzing image: {str(e)}",
                "details": "Please try with a different image",
                "confidence": 0.0
            }

def create_nutrient_chart(nutrients):
    """Create an interactive radar chart for nutrients"""
    categories = list(nutrients.keys())
    values = list(nutrients.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
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
        title="Nutrient Distribution"
    )
    return fig

def create_color_distribution_chart(color_dist):
    """Create an interactive pie chart for color distribution"""
    values = [float(v.strip('%')) for v in color_dist.values()]
    labels = [k.title() for k in color_dist.keys()]
    
    fig = px.pie(
        values=values,
        names=labels,
        title="Color Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig

def main():
    st.title("🍽 Advanced Food Analyzer")
    st.markdown("### Upload or capture food images for detailed nutritional analysis")
    
    analyzer = AdvancedFoodAnalyzer()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📸 Image Input")
        input_method = st.radio("Choose input method:", ["📷 Camera", "📤 Upload"])
        
        if input_method == "📷 Camera":
            image_input = st.camera_input("Take a picture of your food")
        else:
            image_input = st.file_uploader("Choose a food image...", type=['png', 'jpg', 'jpeg'])
        
        if image_input:
            image = Image.open(image_input)
            st.image(image, caption="Input Image", use_column_width=True)
    
    with col2:
        if image_input:
            with st.spinner('Analyzing food...'):
                results = analyzer.analyze_image(image)
                
                if "error" in results:
                    st.error(results["error"])
                    st.write(results["details"])
                else:
                    st.markdown("### 📊 Analysis Results")
                    
                    # Create metrics row
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric("Food Type", results['name'])
                    with m2:
                        st.metric("Calories", f"{results['calories']} kcal")
                    with m3:
                        st.metric("Health Score", f"{results['healthScore']}/100")
                    
                    # Create charts
                    st.plotly_chart(create_nutrient_chart(results['nutrients']))
                    st.plotly_chart(create_color_distribution_chart(results['color_distribution']))
                    
                    # Detailed information in expandable sections
                    with st.expander("🔍 Detailed Analysis"):
                        st.write("##### Confidence Score")
                        st.progress(float(results['confidence_score']))
                        
                        st.write("##### Nutrients Breakdown")
                        for nutrient, value in results['nutrients'].items():
                            if isinstance(value, dict):
                                st.write(f"**{nutrient.title()}:**")
                                for sub_nutrient, sub_value in value.items():
                                    st.write(f"- {sub_nutrient}: {sub_value}%")
                            else:
                                st.write(f"**{nutrient.title()}:** {value}g")
                        
                        st.write("##### Allergen Information")
                        st.write(", ".join(results['allergens']).title())
                        
                        st.write("##### Sustainability Score")
                        st.progress(results['sustainability_score'] / 100)

if __name__ == "__main__":
    main()
