import streamlit as st
from utils.recipe_api import fetch_recipe


st.set_page_config(
    page_title="Intelligent Pantry Chef",
    page_icon="🍽️",
    layout="centered",
)

st.title("🍽️ Intelligent Pantry Chef")
st.subheader("Turn leftovers into delicious meals!")

user_input = st.text_input("Enter your ingredients (comma-separated)", placeholder="e.g. pasta, tomato, spinach")

if st.button("Find Recipe") and user_input.strip():
    with st.spinner("Searching for recipes..."):
        recipes = fetch_recipe(user_input)

    if recipes:
        recipe = recipes[0]
        st.markdown(f"### Recipe: {recipe['title']}")
        st.markdown(f"**Servings:** {recipe['servings']}")
        st.markdown("#### 🧂 Ingredients")
        for item in recipe["ingredients"].split("|"):
            st.markdown(f"- {item.strip()}")
        st.markdown("#### 📖 Instructions")
        st.markdown(recipe["instructions"])
    else:
        st.warning("No matching recipes found. Try changing your ingredients.")