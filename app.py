import json
import os
import streamlit as st

st.set_page_config(
    page_title="Kitchen Vision",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Load styles from assets ────────────────────────────────────────────────────
def load_css(path: str):
    with open(path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/styles.css")

# ── Sidebar navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍳 KitchenVision")
    st.markdown("---")
    st.markdown("**Navigate**")
    page = st.radio(
        label="",
        options=["🏠 Home", "🥦 Pantry Scanner"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:rgba(245,240,232,.4)'>Powered by Gemini AI</small>",
        unsafe_allow_html=True
    )

# ── Save results helper ────────────────────────────────────────────────────────
def save_results(detected_items, categorized_items, recipes, substitutions, health_score):
    results = {
        "detected_items": detected_items,
        "categorized_items": categorized_items,
        "recipes": recipes,
        "substitutions": substitutions,
        "health_score": health_score
    }
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/results.json", "w") as f:
        json.dump(results, f, indent=2)

# ── Route to page ──────────────────────────────────────────────────────────────
if page == "🏠 Home":
    from views.home import render
    render()
else:
    from views.generator import render
    render(save_results=save_results)
