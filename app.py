import streamlit as st
from utils.recipe_api import fetch_recipe

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
#user_input = st.text_input("", placeholder="e.g. pasta, tomato, spinach")

user_input = st.text_input(
    "Ingredient Input",
    placeholder="e.g. pasta, tomato, spinach",
    label_visibility="collapsed"
)

if st.button("✨ Find Recipe") and user_input.strip():
    with st.spinner("Searching for the perfect recipe..."):
        recipes = fetch_recipe(user_input)

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

        # Optional: Nutrition Info
        # st.markdown("#### 🍽️ Nutrition Info")
        # nutrition = fetch_nutrition(recipe["ingredients"])
        # if nutrition:
        #     st.markdown("... nutrition info here ...")

    else:
        st.warning("❌ No recipes found. Try a different combination.")

# Footer
st.markdown("---")
st.caption("Powered by API Ninjas • Built with ❤️ using Streamlit")
