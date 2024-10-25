import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import json
from typing import Dict, List, Tuple
import cv2
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Enhanced Food Analyzer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ImageProcessor:
    """Handles all image processing operations"""
    @staticmethod
    def process_image(image_data) -> Image.Image:
        """Process and validate uploaded image"""
        try:
            image = Image.open(image_data)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            max_size = (800, 800)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            return image
        except Exception as e:
            logger.error(f"Image processing error: {str(e)}")
            return None

    @staticmethod
    def enhance_image(image: Image.Image) -> Image.Image:
        """Enhance image quality for better analysis"""
        try:
            img_cv = np.array(image)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
            
            # Apply light enhancement
            lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            enhanced = cv2.merge((cl,a,b))
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
            
            return Image.fromarray(enhanced)
        except Exception as e:
            logger.warning(f"Image enhancement failed: {str(e)}")
            return image

class FoodAnalyzer:
    """Main class for food analysis"""
    def __init__(self):
        self.food_database = self._initialize_database()
        self.image_processor = ImageProcessor()

    def _initialize_database(self) -> Dict:
        """Initialize food database with nutritional information"""
        return {
            'red_dominant': {
                'name': 'Tomato-based/Red Meat Dish',
                'possible_foods': ['Pizza', 'Tomato Sauce Pasta', 'Steak', 'Meat Curry'],
                'calories': 250,
                'nutrients': {
                    'protein': '8g',
                    'carbs': '30g',
                    'fat': '12g',
                    'fiber': '4g',
                    'vitamins': ['A', 'B12', 'Iron']
                },
                'allergens': ['none'],
                'healthScore': 75,
                'portion_size': 'medium'
            },
            'green_dominant': {
                'name': 'Salad/Vegetables',
                'possible_foods': ['Garden Salad', 'Steamed Vegetables', 'Spinach Dish', 'Broccoli'],
                'calories': 150,
                'nutrients': {
                    'protein': '5g',
                    'carbs': '15g',
                    'fat': '7g',
                    'fiber': '8g',
                    'vitamins': ['A', 'C', 'K', 'Folate']
                },
                'allergens': ['none'],
                'healthScore': 95,
                'portion_size': 'large'
            },
            'brown_dominant': {
                'name': 'Bread/Grain Dish',
                'possible_foods': ['Whole Grain Bread', 'Brown Rice', 'Quinoa', 'Oatmeal'],
                'calories': 350,
                'nutrients': {
                    'protein': '12g',
                    'carbs': '45g',
                    'fat': '15g',
                    'fiber': '3g',
                    'vitamins': ['B1', 'B3', 'Iron']
                },
                'allergens': ['wheat', 'gluten'],
                'healthScore': 65,
                'portion_size': 'medium'
            },
            'light_dominant': {
                'name': 'Rice/Pasta Dish',
                'possible_foods': ['White Rice', 'Pasta', 'Noodles', 'Mashed Potatoes'],
                'calories': 320,
                'nutrients': {
                    'protein': '10g',
                    'carbs': '50g',
                    'fat': '8g',
                    'fiber': '2g',
                    'vitamins': ['B1', 'B6', 'Folate']
                },
                'allergens': ['wheat'],
                'healthScore': 70,
                'portion_size': 'medium'
            },
            'mixed': {
                'name': 'Mixed Dish',
                'possible_foods': ['Stir Fry', 'Mixed Rice Bowl', 'Salad Bowl', 'Buddha Bowl'],
                'calories': 400,
                'nutrients': {
                    'protein': '15g',
                    'carbs': '40g',
                    'fat': '20g',
                    'fiber': '5g',
                    'vitamins': ['Multiple vitamins present']
                },
                'allergens': ['may contain multiple allergens'],
                'healthScore': 80,
                'portion_size': 'large'
            }
        }

    def analyze_image_quality(self, image: Image.Image) -> Dict:
        """Analyze image quality metrics"""
        img_array = np.array(image)
        width, height = image.size
        brightness = np.mean(img_array)
        contrast = np.std(img_array)
        
        quality_issues = []
        if width < 200 or height < 200:
            quality_issues.append("Image resolution is too low")
        if brightness < 50:
            quality_issues.append("Image is too dark")
        elif brightness > 200:
            quality_issues.append("Image is too bright")
        if contrast < 20:
            quality_issues.append("Image has low contrast")
            
        return {
            "resolution": f"{width}x{height}",
            "brightness": f"{brightness:.1f}/255",
            "contrast": f"{contrast:.1f}",
            "quality_issues": quality_issues
        }

    def analyze_colors(self, image: Image.Image) -> Dict:
        """Analyze color distribution in the image"""
        img_array = np.array(image)
        
        def is_red(img):
            return (img[:,:,0] > img[:,:,1]) & (img[:,:,0] > img[:,:,2])
        def is_green(img):
            return (img[:,:,1] > img[:,:,0]) & (img[:,:,1] > img[:,:,2])
        def is_brown(img):
            r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
            return (r > g) & (g > b) & (r < 200)
        def is_light(img):
            return np.mean(img, axis=2) > 200
        def is_dark(img):
            return np.mean(img, axis=2) < 50
        
        total_pixels = img_array.shape[0] * img_array.shape[1]
        
        color_dist = {
            'red': np.sum(is_red(img_array)) / total_pixels * 100,
            'green': np.sum(is_green(img_array)) / total_pixels * 100,
            'brown': np.sum(is_brown(img_array)) / total_pixels * 100,
            'light': np.sum(is_light(img_array)) / total_pixels * 100,
            'dark': np.sum(is_dark(img_array)) / total_pixels * 100
        }
        
        return color_dist

    def estimate_portion_size(self, image: Image.Image) -> str:
        """Estimate food portion size"""
        img_array = np.array(image.convert('L'))
        non_background = np.sum(img_array < 250)
        total_pixels = img_array.size
        coverage_ratio = non_background / total_pixels
        
        if coverage_ratio < 0.3:
            return "small"
        elif coverage_ratio < 0.6:
            return "medium"
        else:
            return "large"

    def is_likely_food(self, image: Image.Image) -> Tuple[bool, List[str]]:
        """Determine if image likely contains food"""
        img_array = np.array(image.convert('L'))
        std_dev = np.std(img_array)
        mean_val = np.mean(img_array)
        
        reasons = []
        if std_dev < 20:
            reasons.append("Image lacks texture variation typical of food")
        if mean_val < 30:
            reasons.append("Image is too dark to be food")
        if mean_val > 225:
            reasons.append("Image is too bright/white to be food")
            
        return (std_dev > 20 and 30 < mean_val < 225), reasons

    def get_dominant_type(self, color_dist: Dict) -> str:
        """Determine dominant food type"""
        max_color = max(color_dist.items(), key=lambda x: x[1])
        return f"{max_color[0]}_dominant" if max_color[1] >= 15 else "mixed"

    def calculate_confidence_score(self, color_dist: Dict, quality_info: Dict) -> int:
        """Calculate analysis confidence score"""
        score = 100
        score -= len(quality_info['quality_issues']) * 15
        max_color_percentage = max(color_dist.values())
        if max_color_percentage < 20:
            score -= 20
        return max(0, min(100, score))

    def analyze_image(self, image: Image.Image) -> Dict:
        """Main image analysis method"""
        try:
            enhanced_image = self.image_processor.enhance_image(image)
            quality_info = self.analyze_image_quality(enhanced_image)
            
            is_food, food_detection_reasons = self.is_likely_food(enhanced_image)
            if not is_food:
                return {
                    "error": "No food detected in image",
                    "details": food_detection_reasons,
                    "quality_info": quality_info
                }
            
            color_dist = self.analyze_colors(enhanced_image)
            food_type = self.get_dominant_type(color_dist)
            portion_size = self.estimate_portion_size(enhanced_image)
            
            food_info = self.food_database[food_type].copy()
            portion_multiplier = {'small': 0.7, 'medium': 1.0, 'large': 1.3}[portion_size]
            food_info['calories'] = int(food_info['calories'] * portion_multiplier)
            
            food_info.update({
                "color_distribution": {k: f"{v:.1f}%" for k, v in color_dist.items()},
                "quality_info": quality_info,
                "detected_portion_size": portion_size,
                "confidence_score": self.calculate_confidence_score(color_dist, quality_info),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return food_info
            
        except Exception as e:
            logger.error(f"Analysis error: {traceback.format_exc()}")
            return {
                "error": f"Error analyzing image: {str(e)}",
                "details": "Please try with a different image",
                "debug_info": {
                    "error_type": type(e).__name__,
                    "error_details": str(e)
                }
            }

def display_results(results: Dict):
    """Display analysis results in Streamlit"""
    if "error" in results:
        st.error(results["error"])
        if "details" in results:
            st.write("📋 Details:", results["details"])
        if "quality_info" in results:
            st.write("📸 Image Quality Information:")
            for issue in results["quality_info"]["quality_issues"]:
                st.warning(f"- {issue}")
        return

    # Main metrics
    st.markdown("### 📊 Analysis Results")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Detected Food", results["name"])
    with col2:
        st.metric("Calories", f"{results['calories']} kcal")
    with col3:
        st.metric("Health Score", f"{results['healthScore']}/100")
    with col4:
        st.metric("Confidence", f"{results['confidence_score']}%")

    # Possible foods
    st.markdown("### 🍽️ Possible Foods")
    st.write(", ".join(results["possible_foods"]))

    # Color distribution
    if "color_distribution" in results:
        st.markdown("### 🎨 Color Analysis")
        cols = st.columns(len(results["color_distribution"]))
        for i, (color, percentage) in enumerate(results["color_distribution"].items()):
            with cols[i]:
                st.metric(color.title(), percentage)

    # Nutritional information
    st.markdown("### 🥗 Nutritional Information")
    nutrients_col1, nutrients_col2 = st.columns(2)
    
    with nutrients_col1:
        st.markdown("**Macronutrients:**")
        for nutrient, value in results["nutrients"].items():
            if nutrient != "vitamins":
                st.metric(nutrient.title(), value)
    
    with nutrients_col2:
        st.markdown("**Vitamins & Minerals:**")
        st.write(", ".join(results["nutrients"]["vitamins"]))

    # Portion size and allergens
    st.markdown("### 📏 Portion Size & Allergens")
    portion_col, allergen_col = st.columns(2)
    
    with portion_col:
        st.metric("Detected Portion Size", results["detected_portion_size"].title())
    
    with allergen_col:
        allergens = results["allergens"]
        if allergens == ["none"]:
            st.success("No common allergens detected")
        else:
            st.warning(f"Contains: {', '.join(allergens)}")

    # Image quality information
    if "quality_info" in results:
        st.markdown("### 📸 Image Quality")
        quality_col1, quality_col2, quality_col3 = st.columns(3)
        
        with quality_col1:
            st.metric("Resolution", results["quality_info"]["resolution"])
        with quality_col2:
            st.metric("Brightness", results["quality_info"]["brightness"])
        with quality_col3:
            st.metric("Contrast", results["quality_info"]["contrast"])
        
        if results["quality_info"]["quality_issues"]:
            st.warning("Quality Issues Detected:")
            for issue in results["quality_info"]["quality_issues"]:
                st.write(f"- {issue}")

def main():
    st.title("🍽️ Enhanced Food Analyzer")
    st.markdown("""
    ## Welcome to the Enhanced Food Analyzer!
    Upload or take a photo of your food to get detailed nutritional information and analysis.
