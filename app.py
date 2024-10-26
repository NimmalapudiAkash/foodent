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

# Configure Streamlit page
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

/* Chat Container Styles */
.chat-container {
    background: white;
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    height: 400px;
    overflow-y: auto;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chat-message {
    padding: 0.5rem 1rem;
    margin: 0.5rem 0;
    border-radius: 10px;
}

.user-message {
    background: #e3f2fd;
    margin-left: 20%;
}

.ai-message {
    background: #f3f4f6;
    margin-right: 20%;
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

/* Input Styles */
.stTextInput>div>div>input {
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.75rem;
    font-size: 1rem;
}

.stTextInput>div>div>input:focus {
    border-color: #3B82F6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Button Styles */
.stButton>button {
    background: linear-gradient(45deg, #3B82F6, #60A5FA);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-weight: 500;
    transition: all 0.3s ease;
    width: 100%;
}

.stButton>button:hover {
    background: linear-gradient(45deg, #2563EB, #3B82F6);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
}
</style>
"""

# Inject CSS
st.markdown(STYLES, unsafe_allow_html=True)

class AdvancedFoodAnalyzer:
    def __init__(self):
        # Food database
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

        # Chat response templates
        self.chat_templates = {
            'greeting': [
                "Hello! I'd be happy to tell you about this food.",
                "Hi there! What would you like to know about this dish?",
                "Welcome! Ask me anything about this food!"
            ],
            'nutrition': [
                "This {name} contains {calories} calories with {protein} protein, {carbs} carbs, and {fat} fat.",
                "The nutritional breakdown shows {calories} calories, with {protein} protein, {carbs} carbs, and {fat} fat.",
                "You're looking at {calories} calories per serving, including {protein} protein, {carbs} carbs, and {fat} fat."
            ],
            'health': [
                "This food has a health score of {score}/100, making it a {rating} choice.",
                "With a health score of {score}/100, this is considered a {rating} option.",
                "The health rating is {score}/100, which indicates it's a {rating} food choice."
            ]
        }

    def analyze_image(self, image):
        """Analyze food image and return nutritional information"""
        try:
            img_array = np.array(image)
            
            # Handle different image formats
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
            
            return {
                'name': food_info['name'],
                'calories': food_info['calories'],
                'nutrients': food_info['nutrients'],
                'allergens': food_info['allergens'],
                'healthScore': food_info['healthScore'],
                'sustainability_score': food_info['sustainability_score'],
                'preparation_time': food_info['preparation_time'],
                'cooking_method': food_info['cooking_method'],
                'color_distribution': color_distribution,
                'dietary_tags': food_info.get('dietary_tags', [])
            }
            
        except Exception as e:
            st.error(f"Error analyzing image: {str(e)}")
            return {"error": str(e)}

    def generate_chat_response(self, query, food_info):
        """Generate contextual responses to user queries about the food"""
        query = query.lower()
        
        # Basic intent recognition
        if any(word in query for word in ['hi', 'hello', 'hey']):
            return np.random.choice(self.chat_templates['greeting'])
            
        elif any(word in query for word in ['calorie', 'calories', 'cal']):
            return f"This {food_info['name']} contains {food_info['calories']} calories."
            
        elif any(word in query for word in ['nutrient', 'nutrition', 'protein', 'carb', 'fat']):
            nutrients = food_info['nutrients']
            return f"Here's the nutritional breakdown:\n- Protein: {nutrients['protein']}g\n- Carbs: {nutrients['carbs']}g\n- Fat: {nutrients['fat']}g\n- Fiber: {nutrients['fiber']}g"
            
        elif any(word in query for word in ['vitamin', 'mineral']):
            vitamins = food_info['nutrients']['vitamins']
            minerals = food_info['nutrients']['minerals']
            return f"Vitamins: {', '.join(f'{k}: {v}%' for k, v in vitamins.items())}\nMinerals: {', '.join(f'{k}: {v}%' for k, v in minerals.items())}"
            
        elif any(word in query for word in ['health', 'healthy', 'score']):
            score = food_info['healthScore']
            rating = "excellent" if score >= 80 else "good" if score >= 60 else "moderate"
            return f"This food has a health score of {score}/100, making it a {rating} choice for your health."
            
        elif any(word in query for word in ['cook', 'prepare', 'make']):
            methods = ", ".join(food_info['cooking_method'])
            return f"You can prepare this dish using these methods: {methods}. It typically takes {food_info['preparation_time']} to prepare."
            
        elif any(word in query for word in ['sustainable', 'environment', 'eco']):
            score = food_info['sustainability_score']
            impact = "very environmentally friendly" if score >= 80 else "moderately sustainable" if score >= 60 else "has room for improvement"
            return f"This food has a sustainability score of {score}/100, meaning it's {impact}."
            
        elif any(word in query for word in ['allergy', 'allergen']):
            allergens = ", ".join(food_info['allergens']) if food_info['allergens'] else "no common allergens"
            return f"Regarding allergens: {allergens}."
            
        else:
            return f"I understand you're asking about the {food_info['name']}. Could you please be more specific? You can ask about calories, nutrients, health score, preparation, or sustainability."

    def create_nutrient_chart(self, nutrients):
        """Create a radar chart for nutrient visualization"""
        categories = ['Protein', 'Carbs', 'Fat', 'Fiber', 'Sugar']
        values = [nutrients[cat.lower()] for cat in categories]
        
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
                )
            ),
            showlegend=False,
            margin=dict(t=30, b=30)
        )
        
        return fig

def main():
    st.title("🍽 AI Food Analyzer Pro")
    st.markdown("### Intelligent Food Analysis & Nutrition Insights with Chat")
    
    analyzer = AdvancedFoodAnalyzer()
    
    # Initialize session state for chat
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    if 'current_food_info' not in st.session_state:
        st.session_state.current_food_info = None
    
    # [Previous sidebar code remains the same...]
    
    # Main content area with three columns
    col1, col2, col3 = st.columns([1, 1.2, 0.8])
    
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
            with st.spinner('Analyzing food with AI...'):
                results = analyzer.analyze_image(image)
                st.session_state.current_food_info = results
                
                if "error" in results:
                    st.error(results["error"])
                else:
                    # [Previous analysis display code remains the same...]
                    pass
    
    with col3:
        st.markdown("### 💬 Chat with AI")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_messages:
                if message["role"] == "user":
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**AI:** {message['content']}")
        
        # Chat input
        if st.session_state.current_food_info:
            user_input = st.text_input("Ask me anything about this food!", key="chat_input")
            
            if user_input:
                # Add user message to chat
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                
                # Generate and add AI response
                ai_response = analyzer.generate_chat_response(user_input, st.session_state.current_food_info)
                st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
                
                # Rerun to update chat display
                st.experimental_rerun()
        else:
            st.info("Upload or take a picture of food to start chatting!")
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.chat_messages = []
            st.experimental_rerun()

if __name__ == "__main__":
    main()
