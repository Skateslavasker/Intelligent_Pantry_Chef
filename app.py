import json
import streamlit as st
from utils.recipe_api import fetch_recipe
from utils.nutrition_api import fetch_nutrition
from utils.image_to_ingr import extract_ingr_from_image
from utils.generate_recipe import generate_recipe

# Page Config
st.set_page_config(page_title="Intelligent Pantry Chef", page_icon="🥗", layout="centered")

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



if st.button("✨ Find Recipe") and combined_ingr.strip():
    with st.spinner("Searching for the perfect recipe..."):
        recipes = fetch_recipe(combined_ingr)

    if recipes:
        recipe = recipes[0]
        
        # --- Recipe Header ---
        st.markdown(f"### 🥘 {recipe['title']}")
        st.markdown(f"**🍽️ Servings:** {recipe['servings']}")
        st.markdown("---")

        # --- Ingredient Columns ---
        st.markdown("#### 🧂 Ingredients")
        ingredients = [i.strip() for i in recipe["ingredients"].split("|")]
        col1, col2 = st.columns(2)
        for idx, item in enumerate(ingredients):
            if idx % 2 == 0:
                col1.markdown(f"- {item}")
            else:
                col2.markdown(f"- {item}")
        st.markdown("---")

        # --- Instructions ---
        st.markdown("#### 📖 Instructions")
        st.markdown(f"<div style='line-height: 1.8;'>{recipe['instructions']}</div>", unsafe_allow_html=True)

        # --- Nutrition Info ---
        st.markdown("---")
        ingredients_text = recipe["ingredients"].replace("|", ",").replace(";", "")

        st.markdown("#### 🔍 Total Nutritional Info")

        nutrition_data = fetch_nutrition(ingredients_text)
        
        if nutrition_data:
            calories = nutrition_data.get("calories", 0)
            fat = nutrition_data.get("FAT", 0)
            protein = nutrition_data.get("PROCNT", 0)
            carbs = nutrition_data.get("CHOCDF", 0)
            cholesterol = nutrition_data.get("CHOLE", 0)

            st.markdown(f"**Calories:** {calories:.1f} kcal")
            st.markdown(f"**Protein:** {protein:.1f} g")
            st.markdown(f"**Fat:** {fat:.1f} g")
            st.markdown(f"**Carbohydrates:** {carbs:.1f} g")
            st.markdown(f"**Cholesterol:** {cholesterol:.1f} mg")
        
        else:
            st.warning("Could not fetch nutrition info.")

    else:
        with st.spinner("🧠 No recipes found. Generating recipe with AI..."):
            raw_response = generate_recipe([i.strip() for i in combined_ingr.split(",") if i.strip()])
            if not raw_response:
                st.error("Failed to generate a recipe. Please try again with different ingredients.")
                st.stop()

            # title, ingredients, instructions = parse_mixtral_response(raw_response)
            recipe_json = json.loads(raw_response)
            title = recipe_json["title"]
            ingredients = recipe_json["ingredients"]
            instructions = recipe_json["instructions"]

            st.markdown(f"### 🥘 {title}")
            st.markdown("---")

            st.markdown("#### 🧂 Ingredients")
            for item in ingredients:
                st.markdown(f"- {item}")
            
            st.markdown("---")

            st.markdown("#### 📖 Instructions")
            for step in instructions:
                st.markdown(step)
            
            
            st.markdown("---") 
            st.markdown("#### 🔍 Total Nutritional Info ")
            nutrition_data = fetch_nutrition(ingredients)

            if nutrition_data:
                calories = nutrition_data.get("calories", 0)
                fat = nutrition_data.get("FAT", 0)
                protein = nutrition_data.get("PROCNT", 0)
                carbs = nutrition_data.get("CHOCDF", 0)
                cholesterol = nutrition_data.get("CHOLE", 0)
                
                st.markdown(f"**Calories:** {calories:.1f} kcal")
                st.markdown(f"**Protein:** {protein:.1f} g")
                st.markdown(f"**Fat:** {fat:.1f} g")
                st.markdown(f"**Carbohydrates:** {carbs:.1f} g")
                st.markdown(f"**Cholesterol:** {cholesterol:.1f} mg")
            else:
                st.warning("Could not fetch nutrition info for the generated recipe.")

# Footer
st.markdown("---")
st.caption("Powered by API Ninjas • Built with ❤️ using Streamlit")
