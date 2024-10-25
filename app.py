import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Basic Food Analyzer",
    page_icon="🍽️",
    layout="wide"
)

class BasicFoodAnalyzer:
    def __init__(self):
        self.food_database = {
            'red_dominant': {
                'name': 'Tomato-based/Red Meat Dish',
                'calories': 250,
                'nutrients': {
                    'protein': '8g',
                    'carbs': '30g',
                    'fat': '12g',
                    'fiber': '4g'
                },
                'allergens': ['none'],
                'healthScore': 75
            },
            'green_dominant': {
                'name': 'Salad/Vegetables',
                'calories': 150,
                'nutrients': {
                    'protein': '5g',
                    'carbs': '15g',
                    'fat': '7g',
                    'fiber': '8g'
                },
                'allergens': ['none'],
                'healthScore': 95
            },
            'brown_dominant': {
                'name': 'Bread/Grain Dish',
                'calories': 350,
                'nutrients': {
                    'protein': '12g',
                    'carbs': '45g',
                    'fat': '15g',
                    'fiber': '3g'
                },
                'allergens': ['wheat', 'gluten'],
                'healthScore': 65
            },
            'light_dominant': {
                'name': 'Rice/Pasta Dish',
                'calories': 320,
                'nutrients': {
                    'protein': '10g',
                    'carbs': '50g',
                    'fat': '8g',
                    'fiber': '2g'
                },
                'allergens': ['wheat'],
                'healthScore': 70
            },
            'mixed': {
                'name': 'Mixed Dish',
                'calories': 400,
                'nutrients': {
                    'protein': '15g',
                    'carbs': '40g',
                    'fat': '20g',
                    'fiber': '5g'
                },
                'allergens': ['may contain multiple allergens'],
                'healthScore': 80
            }
        }

    def analyze_colors(self, image):
        """Analyze the color distribution in the image using PIL"""
        # Convert image to RGB if it isn't already
        img_rgb = image.convert('RGB')
        
        # Get image data
        pixels = list(img_rgb.getdata())
        num_pixels = len(pixels)
        
        # Simple color categorization
        red_pixels = sum(1 for r, g, b in pixels if r > max(g, b) + 30)
        green_pixels = sum(1 for r, g, b in pixels if g > max(r, b) + 30)
        brown_pixels = sum(1 for r, g, b in pixels if (r > g > b) and (r-b > 30))
        light_pixels = sum(1 for r, g, b in pixels if all(x > 200 for x in (r, g, b)))
        
        # Calculate percentages
        color_dist = {
            'red': (red_pixels / num_pixels) * 100,
            'green': (green_pixels / num_pixels) * 100,
            'brown': (brown_pixels / num_pixels) * 100,
            'light': (light_pixels / num_pixels) * 100
        }
        
        return color_dist

    def is_likely_food(self, image):
        """Basic check if image likely contains food using PIL"""
        # Convert to grayscale
        gray_img = image.convert('L')
        
        # Calculate basic statistics
        pixels = list(gray_img.getdata())
        std_dev = np.std(pixels)
        mean_val = np.mean(pixels)
        
        # Basic heuristic for food images
        return std_dev > 20 and 30 < mean_val < 225

    def get_dominant_type(self, color_dist):
        """Determine the dominant food type based on color distribution"""
        max_color = max(color_dist.items(), key=lambda x: x[1])
        
        if max_color[1] < 15:  # If no clear dominant color
            return 'mixed'
        
        return f"{max_color[0]}_dominant"

    def analyze_image(self, image):
        """Analyze food image and return nutritional information"""
        try:
            # Check if image likely contains food
            if not self.is_likely_food(image):
                return {
                    "error": "No food detected in image",
                    "details": "Image doesn't appear to contain food"
                }
            
            # Analyze colors
            color_dist = self.analyze_colors(image)
            
            # Get food type based on color profile
            food_type = self.get_dominant_type(color_dist)
            
            # Get nutritional information
            food_info = self.food_database[food_type].copy()
            
            # Add analysis metadata
            food_info.update({
                "color_distribution": {k: f"{v:.1f}%" for k, v in color_dist.items()},
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return food_info
            
        except Exception as e:
            return {
                "error": f"Error analyzing image: {str(e)}",
                "details": "Please try with a different image"
            }

def process_image(image_data):
    """Process and validate image"""
    try:
        image = Image.open(image_data)
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        # Standardize size
        max_size = (400, 400)  # Reduced size for faster processing
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def display_results(results):
    """Display analysis results"""
    if "error" in results:
        st.error(results["error"])
        if "details" in results:
            st.write(results["details"])
        return

    st.markdown("### 📊 Analysis Results")
    
    # Main metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Detected Food", results["name"])
    with col2:
        st.metric("Calories", f"{results['calories']} kcal")
    with col3:
        st.metric("Health Score", f"{results['healthScore']}/100")

    # Color distribution
    if "color_distribution" in results:
        st.markdown("### 🎨 Color Analysis")
        cols = st.columns(len(results["color_distribution"]))
        for i, (color, percentage) in enumerate(results["color_distribution"].items()):
            with cols[i]:
                st.metric(color.title(), percentage)

    # Nutrients
    st.markdown("### 🥗 Nutritional Information")
    cols = st.columns(4)
    nutrients = results["nutrients"]
    
    with cols[0]:
        st.metric("Protein", nutrients["protein"])
    with cols[1]:
        st.metric("Carbs", nutrients["carbs"])
    with cols[2]:
        st.metric("Fat", nutrients["fat"])
    with cols[3]:
        st.metric("Fiber", nutrients["fiber"])

    # Allergens
    st.markdown("### ⚠️ Allergens")
    allergens = results["allergens"]
    if allergens == ["none"]:
        st.success("No common allergens detected")
    else:
        st.warning(f"Contains: {', '.join(allergens)}")

def main():
    st.title("🍽️ Basic Food Analyzer")
    
    # Initialize analyzer
    analyzer = BasicFoodAnalyzer()
    
    # Create tabs for input methods
    tab1, tab2 = st.tabs(["📷 Camera Input", "📤 Upload Image"])
    
    with tab1:
        camera_input = st.camera_input("Take a picture of your food")
        if camera_input:
            image = process_image(camera_input)
            if image:
                st.image(image, caption="Captured Image", use_column_width=True)
                with st.spinner('Analyzing food...'):
                    results = analyzer.analyze_image(image)
                    display_results(results)
    
    with tab2:
        uploaded_file = st.file_uploader(
            "Choose a food image...",
            type=['png', 'jpg', 'jpeg']
        )
        if uploaded_file:
            image = process_image(uploaded_file)
            if image:
                st.image(image, caption="Uploaded Image", use_column_width=True)
                with st.spinner('Analyzing food...'):
                    results = analyzer.analyze_image(image)
                    display_results(results)

if __name__ == "__main__":
    main()
