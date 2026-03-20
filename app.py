import streamlit as st

st.set_page_config(
    page_title="Kitchen Vision",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global styles injected once ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --sage:        #7C9A6E;
    --sage-light:  #A8C09A;
    --mint:        #B5E2C8;
    --cream:       #F5F0E8;
    --amber:       #D4A853;
    --tomato:      #C0504A;
    --avocado:     #4A6741;
    --bg-dark:     #0D1A0F;
    --bg-mid:      #132015;
    --glass-bg:    rgba(255,255,255,0.07);
    --glass-border:rgba(255,255,255,0.14);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* Background */
.stApp {
    background:
        radial-gradient(ellipse 70% 55% at 10% 15%, rgba(124,154,110,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 88% 80%, rgba(74,103,65,0.20) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 55% 5%,  rgba(181,226,200,0.08) 0%, transparent 55%),
        linear-gradient(145deg, #0D1A0F 0%, #132015 45%, #0A1209 100%);
    background-attachment: fixed;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(13,26,15,0.85) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] * { color: #F5F0E8 !important; }

/* Cards / glass panels */
.glass-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 18px;
    backdrop-filter: blur(20px);
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.08);
    transition: border-color .3s, box-shadow .3s;
}
.glass-card:hover {
    border-color: rgba(168,192,154,0.30);
    box-shadow: 0 12px 52px rgba(0,0,0,0.42), inset 0 1px 0 rgba(255,255,255,0.12);
}

/* Headings */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #F5F0E8 !important; }

/* Ingredient tag pill */
.ing-pill {
    display: inline-block;
    padding: 5px 14px; margin: 4px;
    border-radius: 100px;
    background: rgba(124,154,110,0.15);
    border: 1px solid rgba(124,154,110,0.30);
    color: #A8C09A; font-size: .82rem;
}

/* Section divider label */
.section-lbl {
    display: flex; align-items: center; gap: 10px;
    font-size: .68rem; font-weight: 700; letter-spacing: .18em;
    text-transform: uppercase; color: #A8C09A; margin: 28px 0 16px;
}
.section-lbl::before, .section-lbl::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.10));
}
.section-lbl::after { background: linear-gradient(to left, transparent, rgba(255,255,255,0.10)); }

/* Streamlit widgets */
.stButton > button {
    background: linear-gradient(135deg, #7C9A6E, #4A6741) !important;
    color: #F5F0E8 !important; border: none !important;
    border-radius: 12px !important; font-weight: 600 !important;
    padding: 10px 28px !important;
    box-shadow: 0 4px 20px rgba(124,154,110,0.35) !important;
    transition: opacity .2s, transform .2s !important;
}
.stButton > button:hover { opacity: .88; transform: translateY(-1px); }

[data-testid="stFileUploader"] {
    background: rgba(124,154,110,0.06) !important;
    border: 2px dashed rgba(124,154,110,0.30) !important;
    border-radius: 14px !important; padding: 20px !important;
}

.stSpinner > div { color: #A8C09A !important; }

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 14px; padding: 16px !important;
}
[data-testid="stMetricValue"] { color: #A8C09A !important; font-family: 'Playfair Display', serif !important; }
[data-testid="stMetricLabel"] { color: rgba(245,240,232,.6) !important; }

/* Expander */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
}

/* Text */
p, li, label, .stMarkdown { color: rgba(245,240,232,0.80) !important; }
</style>
""", unsafe_allow_html=True)

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

# ── Route to page ──────────────────────────────────────────────────────────────
if page == "🏠 Home":
    from views.home import render
    render()
else:
    from views.generator import render
    render()