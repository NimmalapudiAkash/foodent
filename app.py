import streamlit as st
import numpy as np
from PIL import Image
import cv2
from datetime import datetime
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Simple Food Analyzer",
    page_icon="🍽️",
    layout="wide"
)

class SimpleFoodAnalyzer:
    def __init__(self):
        # Food database with color profiles and nutrition info
        self.food_database = {
            'red_foods': {
                'name': 'Tomato-based Dish',
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
            'green_foods': {
                'name': 'Green Salad/Vegetables',
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
            'brown_foods': {
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
            'yellow_foods': {
                'name': 'Pasta/Rice Dish',
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
            'mixed_colors': {
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

    def analyze_colors(self, img_array):
        """Analyze the color distribution in the image"""
        # Convert to HSV color space
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Define color ranges
        color_ranges = {
            'red': ([0, 50, 50], [10, 255, 255]),
            'green': ([35, 50, 50], [85, 255, 255]),
            'brown': ([10, 50, 50], [20, 255, 255]),
            'yellow': ([20, 50, 50], [35, 255, 255])
        }
        
        # Calculate color percentages
        color_percentages = {}
        total_pixels = hsv.shape[0] * hsv.shape[1]
        
        for color, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            color_pixels = cv2.countNonZero(mask)
            percentage = (color_pixels / total_pixels) * 100
            color_percentages[color] = percentage
            
        return color_percentages

    def is_likely_food(self, img_array):
        """Basic check if image likely contains food"""
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Calculate image statistics
        std_dev = np.std(gray)
        mean_val = np.mean(gray)
        
        # Images with very low variation or extreme brightness/darkness
        # are less likely to be food
        return std_dev > 20 and 30 < mean_val < 225

    def get_dominant_color_profile(self, color_percentages):
        """Determine the dominant color profile"""
        if max(color_percentages.values()) < 10:
            return 'mixed_colors'
        
        dominant_color = max(color_percentages.items(), key=lambda x: x[1])[0]
        return f"{dominant_color}_foods"

    def analyze_image(self, image):
        """Analyze food image and return nutritional information"""
        try:
            # Convert PIL image to numpy array
            img_array = np.array(image)
            
            # Check if image likely contains food
            if not self.is_likely_food(img_array):
                return {
                    "error": "No food detected in image",
                    "details": "Image doesn't appear to contain food"
                }
            
            # Analyze colors
            color_percentages = self.analyze_colors(img_array)
            
            # Get food type based on color profile
            food_type = self.get_dominant_color_profile(color_percentages)
            
            # Get nutritional information
            food_info = self.food_database[food_type].copy()
            
            # Add analysis metadata
            food_info.update({
                "color_distribution": {k: f"{v:.1f}%" for k, v in color_percentages.items()},
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
        max_size = (800, 800)
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
    st.title("🍽️ Simple Food Analyzer")
    
    # Initialize FoodAnalyzer
    analyzer = SimpleFoodAnalyzer()
    
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
