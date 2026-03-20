import streamlit as st


def render():
    # ── Hero ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center; padding: 40px 0 20px;'>
        <div style='
            display:inline-flex; align-items:center; gap:8px;
            padding:6px 18px; border-radius:100px;
            background:rgba(124,154,110,0.15); border:1px solid rgba(124,154,110,0.30);
            font-size:.72rem; font-weight:700; letter-spacing:.14em;
            text-transform:uppercase; color:#A8C09A; margin-bottom:20px;
        '>
            <span style='width:6px;height:6px;border-radius:50%;background:#A8C09A;display:inline-block;'></span>
            AI-Powered Kitchen Assistant
        </div>
        <h1 style='font-family:Playfair Display,serif; font-size:3.4rem; font-weight:900; line-height:1.08;
            background:linear-gradient(135deg,#F5F0E8 0%,#A8C09A 55%,#B5E2C8 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text; margin-bottom:16px;'>
            Kitchen Vision
        </h1>
        <p style='font-size:1.1rem; color:rgba(245,240,232,.65); max-width:520px; margin:0 auto 36px; line-height:1.7;'>
            Snap a photo of your pantry — AI detects your ingredients,
            generates recipes, and scores your pantry health.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero image ─────────────────────────────────────────────────────────────
    st.image(
        "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=1200&q=85",
        caption="Upload your pantry → AI does the rest",
        use_container_width=True
    )

    st.markdown("<div class='section-lbl'>How It Works</div>", unsafe_allow_html=True)

    # ── Feature steps ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    for col, icon, title, desc in [
        (c1, "📸", "Upload Image",      "Take a photo of your pantry, fridge, or ingredients on the counter."),
        (c2, "🔍", "AI Detection",       "Gemini Vision scans the image and identifies every visible ingredient."),
        (c3, "📖", "Recipe Generation",  "3 beginner-friendly recipes are generated using only what you have."),
        (c4, "❤️", "Health Score",       "Your pantry is scored 1–10 based on nutritional diversity."),
    ]:
        with col:
            st.markdown(f"""
            <div class='glass-card' style='text-align:center;'>
                <div style='font-size:2rem; margin-bottom:10px;'>{icon}</div>
                <div style='font-weight:700; font-size:.95rem; margin-bottom:8px; color:#F5F0E8;'>{title}</div>
                <div style='font-size:.82rem; color:rgba(245,240,232,.60); line-height:1.6;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-lbl'>What You'll Get</div>", unsafe_allow_html=True)

    c_a, c_b = st.columns(2)

    with c_a:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='font-size:1.1rem; margin-bottom:14px;'>🥦 Pantry Features</h3>
            <ul style='color:rgba(245,240,232,.70); line-height:2; font-size:.88rem;'>
                <li>Ingredient detection from any image</li>
                <li>Storage categorisation (Fresh / Cold / Frozen / Dry)</li>
                <li>Expanded substitution suggestions</li>
                <li>Pantry health scoring with explanations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_b:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='font-size:1.1rem; margin-bottom:14px;'>📖 Recipe Features</h3>
            <ul style='color:rgba(245,240,232,.70); line-height:2; font-size:.88rem;'>
                <li>3 structured recipes with step-by-step instructions</li>
                <li>Prep time &amp; difficulty rating per recipe</li>
                <li>Uses only ingredients you already have</li>
                <li>Beginner-friendly language throughout</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀  Go to Pantry Scanner", use_container_width=True):
        st.info("👈 Select **Pantry Scanner** from the sidebar to begin.")