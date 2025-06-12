import json
import streamlit as st
from agents.pantry_agent import run_pantry_agent
from utils.nutrition_api import fetch_nutrition
from utils.image_to_ingr import extract_ingr_from_image
import jwt 
from dotenv import load_dotenv
import os 
load_dotenv()


JWT_SECRET = os.getenv("JWT_SECRET")

def authenticate_user_from_url():
    """Authenticate user from JWT token in URL."""
    query_params = st.query_params
    token = query_params.get("token")
    email = query_params.get("email")

    if token and email:
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            if decoded.get("email") == email:
                st.session_state["user"] = {
                    "email": email,
                    "jwt": token
                }
        except jwt.ExpiredSignatureError:
            st.error("Session expired. Please log in again.")
        except jwt.InvalidTokenError:
            st.error("Invalid token. Please log in again.")


# Page Config
st.set_page_config(page_title="Intelligent Pantry Chef", page_icon="🥗", layout="centered")

authenticate_user_from_url()

if "user" not in st.session_state:
    st.error("You must be logged in to use this app. Please log in first.")
    st.markdown("[👉 Login with Google](http://localhost:8000/login)")
    st.stop()
else:
    st.success(f"Welcome, {st.session_state['user']['email']}")
# --- Header Section ---
st.markdown("""
    <style>
        .heading-box {
            background-color: rgba(46, 139, 87, 0.1);
            padding: 1.5rem;
            border-radius: 1.2rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 1.5rem;
        }
        .heading-box h1 {
            font-size: 2.2rem;
            color: #34d399;
            margin: 0;
        }
        .heading-sub {
            font-size: 1rem;
            color: #ccc;
        }
    </style>

    <div class="heading-box">
        <h1>🍽️ Intelligent Pantry Chef</h1>
        <div class="heading-sub">Turn your leftovers into delicious meals</div>
    </div>
""", unsafe_allow_html=True)


# --- Input Section ---
st.markdown("## 📝 Enter Ingredients")

user_input = st.text_input(
    "Ingredient Input",
    placeholder="e.g. pasta, tomato, spinach",
    label_visibility="collapsed"
)

st.markdown("## 🖼️ Or Upload a Fridge Image")
uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

image_ingr = []
selected_image_ingr = []

# Track last processed filename
if 'last_image_name' not in st.session_state:
    st.session_state.last_image_name = None
if 'cached_ingredients' not in st.session_state:
    st.session_state.cached_ingredients = []

if uploaded_image:
    file_name = uploaded_image.name

    # Run GPT only if the uploaded image is different
    if file_name != st.session_state.last_image_name:
        with st.spinner("Analyzing image using GPT-4.1 mini..."):
            result = extract_ingr_from_image(uploaded_image)
            if result:
                ingr_list = [i.strip() for i in result.split(",") if i.strip()]
                st.session_state.cached_ingredients = ingr_list
                st.session_state.last_image_name = file_name
            else:
                st.warning("Could not detect any ingredients. Try a clearer image.")

    image_ingr = st.session_state.cached_ingredients

    if image_ingr:
        st.success("🧠 Detected Ingredients:")
        selected_image_ingr = st.multiselect(
            "Select ingredients to include:",
            options=image_ingr,
            default=image_ingr,
            key="image_ingr_select"
        )

combined_ingr = user_input.strip()
if selected_image_ingr:
    combined_ingr += f", {', '.join(selected_image_ingr)}" if combined_ingr else ", ".join(selected_image_ingr)


# --- Recipe Generation ---
if st.button("✨ Find Recipe") and combined_ingr.strip():
    with st.spinner("Searching for the perfect recipe..."):
        recipe = run_pantry_agent(combined_ingr)

    # --- Recipe Header ---
    st.markdown(f"### 🥘 {recipe['title']}")
    st.markdown("---")

    # --- Ingredients Section ---
    st.markdown("#### 🧂 Ingredients")
    col1, col2 = st.columns(2)
    for idx, item in enumerate(recipe['ingredients']):
        (col1 if idx % 2 == 0 else col2).markdown(f"- {item}")
    
    st.markdown("---")
    
    # --- Instructions Section ---
    st.markdown("#### 📖 Instructions")
    for step in recipe["instructions"]:
        st.markdown(f"- {step}")
    
    st.markdown("---")

    # --- Nutrition Section ---
    st.markdown("#### 🔍 Total Nutritional Info")
    ingredients_for_nutrition = ", ".join(recipe['ingredients'])
    nutrition_data = fetch_nutrition(ingredients_for_nutrition)

    if nutrition_data:
        st.markdown(f"**Calories:** {nutrition_data.get('calories', 0):.1f} kcal")
        st.markdown(f"**Protein:** {nutrition_data.get('PROCNT', 0):.1f} g")
        st.markdown(f"**Fat:** {nutrition_data.get('FAT', 0):.1f} g")
        st.markdown(f"**Carbohydrates:** {nutrition_data.get('CHOCDF', 0):.1f} g")
        st.markdown(f"**Cholesterol:** {nutrition_data.get('CHOLE', 0):.1f} mg")
    else:
        st.warning("⚠️ Could not fetch nutrition info.")

# Footer
st.markdown("---")
st.caption(" Built using Streamlit")
