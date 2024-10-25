import streamlit as st
import numpy as np
from PIL import Image
import io
import os
from dotenv import load_dotenv
import time
import json
from datetime import datetime
import tensorflow as tf
import cv2

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Smart Food Analyzer",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS (keeping the same styling as before)
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .result-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

class FoodAnalyzer:
    def __init__(self):
        # Load pre-trained MobileNetV2 model for image classification
        self.model = tf.keras.applications.MobileNetV2(weights='imagenet')
        
        # Common food categories and their nutritional info
        self.food_database = {
            'pizza': {
                'name': 'Pizza',
                'calories': 266,
                'nutrients': {
                    'protein': '11g',
                    'carbs': '33g',
                    'fat': '10g',
                    'fiber': '2g'
                },
                'allergens': ['wheat', 'dairy'],
                'healthScore': 45
            },
            'hamburger': {
                'name': 'Hamburger',
                'calories': 354,
                'nutrients': {
                    'protein': '20g',
                    'carbs': '29g',
                    'fat': '17g',
                    'fiber': '3g'
                },
                'allergens': ['wheat'],
                'healthScore': 40
            },
            'salad': {
                'name': 'Fresh Salad',
                'calories': 152,
                'nutrients': {
                    'protein': '5g',
                    'carbs': '10g',
                    'fat': '7g',
                    'fiber': '8g'
                },
                'allergens': ['none'],
                'healthScore': 95
            },
            'sushi': {
                'name': 'Sushi Roll',
                'calories': 228,
                'nutrients': {
                    'protein': '9g',
                    'carbs': '38g',
                    'fat': '5g',
                    'fiber': '4g'
                },
                'allergens': ['fish', 'soy'],
                'healthScore': 80
            },
            'pasta': {
                'name': 'Pasta Dish',
                'calories': 320,
                'nutrients': {
                    'protein': '12g',
                    'carbs': '54g',
                    'fat': '8g',
                    'fiber': '4g'
                },
                'allergens': ['wheat'],
                'healthScore': 65
            }
        }
    
    def preprocess_image(self, image):
        """Preprocess image for the model"""
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Resize image to model's required size
        img_resized = cv2.resize(img_array, (224, 224))
        
        # Preprocess for MobileNetV2
        img_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(img_resized)
        
        return np.expand_dims(img_preprocessed, axis=0)

    def is_food(self, prediction_classes, confidence):
        """Check if the image contains food"""
        # List of ImageNet categories that typically correspond to food
        food_related_categories = [
            'pizza', 'hamburger', 'sandwich', 'salad', 'sushi', 'pasta',
            'ice_cream', 'bread', 'coffee', 'cake', 'rice', 'vegetable'
        ]
        
        return any(category in prediction_classes.lower() for category in food_related_categories)

    def get_food_type(self, prediction_classes):
        """Map prediction to food database entry"""
        prediction_lower = prediction_classes.lower()
        
        # Map predicted class to food database
        for food_type in self.food_database.keys():
            if food_type in prediction_lower:
                return food_type
                
        # Default to closest match or None
        return None

    def analyze_image(self, image):
        """Analyze food image and return nutritional information"""
        try:
            # Preprocess image
            preprocessed_img = self.preprocess_image(image)
            
            # Get model predictions
            predictions = self.model.predict(preprocessed_img)
            decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)
            
            # Get top prediction
            top_prediction = decoded_predictions[0][0]
            prediction_class = top_prediction[1]
            confidence = float(top_prediction[2])
            
            # Check if image contains food
            if not self.is_food(prediction_class, confidence):
                return {
                    "error": "No food detected in image",
                    "confidence": confidence,
                    "detected_class": prediction_class
                }
            
            # Get food type and nutritional info
            food_type = self.get_food_type(prediction_class)
            if food_type is None:
                return {
                    "error": "Unable to identify specific food type",
                    "confidence": confidence,
                    "detected_class": prediction_class
                }
            
            # Get nutritional information
            food_info = self.food_database[food_type].copy()
            food_info.update({
                "confidence": confidence,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return food_info
            
        except Exception as e:
            return {
                "error": f"Error analyzing image: {str(e)}",
                "confidence": 0
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
        if "detected_class" in results:
            st.write(f"Detected content: {results['detected_class']}")
            st.write(f"Confidence: {results['confidence']:.2%}")
        return

    st.markdown("### 📊 Analysis Results")
    
    # Main metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Food Item", results["name"])
    with col2:
        st.metric("Calories", f"{results['calories']} kcal")
    with col3:
        st.metric("Health Score", f"{results['healthScore']}/100")

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

    # Confidence
    st.markdown("### 🎯 Detection Confidence")
    st.progress(float(results["confidence"]))
    st.write(f"Confidence: {results['confidence']:.2%}")

def main():
    st.title("🍽️ Smart Food Analyzer")
    
    # Initialize FoodAnalyzer
    analyzer = FoodAnalyzer()
    
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
