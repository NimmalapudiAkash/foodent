import streamlit as st
import json
from datetime import datetime
import base64
from io import BytesIO

class FoodAnalyzer:
    def __init__(self):
        self.food_database = {
            "fruits": ["apple", "banana", "orange", "grape", "strawberry"],
            "vegetables": ["carrot", "broccoli", "spinach", "tomato", "cucumber"],
            "grains": ["rice", "bread", "pasta", "oats", "quinoa"],
            "proteins": ["chicken", "fish", "beef", "eggs", "tofu"],
            "dairy": ["milk", "cheese", "yogurt", "butter", "cream"]
        }
        
        self.nutrition_facts = {
            "fruits": "Rich in vitamins, minerals, and antioxidants",
            "vegetables": "High in fiber, vitamins, and minerals",
            "grains": "Good source of carbohydrates and fiber",
            "proteins": "Essential for muscle building and repair",
            "dairy": "Excellent source of calcium and protein"
        }

    def basic_analysis(self, food_type):
        """Provide basic food analysis based on category"""
        return {
            "category": food_type,
            "common_items": self.food_database.get(food_type, []),
            "nutrition": self.nutrition_facts.get(food_type, "Nutrition information not available"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class FoodentApp:
    def __init__(self):
        self.analyzer = FoodAnalyzer()
        self.setup_session_state()
        
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        if 'image_counter' not in st.session_state:
            st.session_state.image_counter = 0

    def setup_page(self):
        """Configure the Streamlit page"""
        st.set_page_config(page_title='Foodent', page_icon='🍽️', layout='wide')
        st.title('✺ FOODENT')
        st.markdown("""
        ### Your Personal Food Analysis Assistant
        Upload food images and get basic insights about different food categories.
        """)

    def save_uploaded_file(self, uploaded_file):
        """Save uploaded file information"""
        if uploaded_file is not None:
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size
            }
            return file_details
        return None

    def display_analysis(self, food_type):
        """Display food analysis results"""
        analysis = self.analyzer.basic_analysis(food_type)
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Category Analysis")
            st.write(f"Selected Category: {analysis['category'].title()}")
            st.write("Common Items:", ", ".join(analysis['common_items']))
            
        with col2:
            st.subheader("Nutritional Insights")
            st.write(analysis['nutrition'])
        
        # Add to history
        st.session_state.analysis_history.append(analysis)
        
        # Show preparation suggestions
        st.subheader("Preparation Suggestions")
        st.write(self.get_preparation_tips(food_type))

    def get_preparation_tips(self, food_type):
        """Get preparation tips based on food type"""
        tips = {
            "fruits": "• Wash thoroughly before eating\n• Can be eaten raw or added to smoothies\n• Great for healthy snacking",
            "vegetables": "• Steam or roast for best nutrition\n• Can be eaten raw in salads\n• Store in refrigerator",
            "grains": "• Cook in water or broth\n• Follow package instructions\n• Store in airtight containers",
            "proteins": "• Cook thoroughly\n• Use proper food safety guidelines\n• Store at appropriate temperature",
            "dairy": "• Keep refrigerated\n• Check expiration dates\n• Use in recommended portions"
        }
        return tips.get(food_type, "No specific preparation tips available.")

    def show_history(self):
        """Display analysis history"""
        if st.session_state.analysis_history:
            st.subheader("Recent Analysis History")
            for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):
                with st.expander(f"Analysis {len(st.session_state.analysis_history) - i}"):
                    st.write(f"Category: {analysis['category'].title()}")
                    st.write(f"Timestamp: {analysis['timestamp']}")
                    st.write("Nutrition Info:", analysis['nutrition'])

    def run(self):
        """Run the Streamlit application"""
        self.setup_page()
        
        # Sidebar
        with st.sidebar:
            st.title("Food Analysis Options")
            image_source = st.radio("Choose image source:", ["Upload", "Camera"])
            
            if image_source == "Upload":
                uploaded_file = st.file_uploader("Upload food image...", 
                                               type=['jpg', 'jpeg', 'png'])
            else:
                uploaded_file = st.camera_input("Take a food picture")

            # Food category selection
            food_type = st.selectbox("Select food category:",
                                   ["fruits", "vegetables", "grains", "proteins", "dairy"])
            
            if st.button("Analyze Food"):
                if uploaded_file:
                    file_details = self.save_uploaded_file(uploaded_file)
                    if file_details:
                        st.success("Image uploaded successfully!")
                        st.write("File Details:", file_details)
                        
                        # Display image
                        st.image(uploaded_file, caption="Uploaded Food Image", 
                               use_column_width=True)
                        
                        # Show analysis
                        self.display_analysis(food_type)
                else:
                    st.warning("Please upload an image first!")

        # Main content area
        if uploaded_file:
            # Display current image
            st.image(uploaded_file, caption="Current Image", width=300)
            
        # Show analysis history
        self.show_history()
        
        # Additional information
        with st.expander("About Foodent"):
            st.write("""
            Foodent is a simple food analysis tool that helps you:
            - Analyze different food categories
            - Get basic nutritional insights
            - Learn about food preparation
            - Track your food analysis history
            """)

if __name__ == "__main__":
    app = FoodentApp()
    app.run()
