import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Food Entertainment App",
    page_icon="🍽️",
    layout="wide"
)

# Initialize session state
if 'foods' not in st.session_state:
    st.session_state.foods = []

def add_food(name, category, calories, date_added):
    st.session_state.foods.append({
        'name': name,
        'category': category,
        'calories': calories,
        'date_added': date_added
    })

# Main app header
st.title("🍽️ Food Entertainment App")
st.markdown("""
    Welcome to the Food Entertainment App! Track your favorite foods and their nutritional information.
    """)

# Sidebar for adding new foods
with st.sidebar:
    st.header("Add New Food")
    food_name = st.text_input("Food Name")
    food_category = st.selectbox(
        "Category",
        ["Breakfast", "Lunch", "Dinner", "Snacks", "Desserts"]
    )
    food_calories = st.number_input("Calories", min_value=0)
    
    if st.button("Add Food"):
        if food_name:
            add_food(
                food_name,
                food_category,
                food_calories,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            st.success(f"Added {food_name} to your food list!")
        else:
            st.error("Please enter a food name!")

# Main content area
st.header("Your Food Collection")

if st.session_state.foods:
    # Convert session state to DataFrame
    df = pd.DataFrame(st.session_state.foods)
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Foods", len(df))
    with col2:
        st.metric("Average Calories", f"{df['calories'].mean():.1f}")
    with col3:
        st.metric("Total Categories", len(df['category'].unique()))
    
    # Display food table
    st.subheader("Food List")
    st.dataframe(
        df,
        column_config={
            "name": "Food Name",
            "category": "Category",
            "calories": "Calories",
            "date_added": "Date Added"
        },
        hide_index=True
    )
    
    # Category breakdown
    st.subheader("Category Breakdown")
    category_counts = df['category'].value_counts()
    st.bar_chart(category_counts)
    
else:
    st.info("No foods added yet. Use the sidebar to add your first food!")

# Footer
st.markdown("""
    ---
    Created with ❤️ using Streamlit
    """)
