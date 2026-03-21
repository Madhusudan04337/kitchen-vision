import streamlit as st
from PIL import Image
import numpy as np

from services.vision_service import detect_ingredients
from services.recipe_service import generate_recipes
from services.substitution_service import suggest_substitutions
from services.health_service import health_score
from utils.image_utils import preprocess_image
from utils.helpers import categorize_items


# ── Session-state helpers ──────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "ingredients": None,
        "recipes":     None,
        "subs":        None,
        "health":      None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def _reset():
    for key in ["ingredients", "recipes", "subs", "health"]:
        st.session_state[key] = None


def _flatten_ing(ing) -> str:
    if isinstance(ing, dict):
        item = ing.get("item", ing.get("name", ""))
        qty  = ing.get("quantity", ing.get("amount", ""))
        return f"{qty} {item}".strip() if qty else item
    return str(ing)


# ── Main render ────────────────────────────────────────────────────────────────
def render(save_results=None):
    _init_state()

    # styles already loaded globally by app.py — no inject needed here

    st.markdown("""
    <h1 style='margin-bottom:4px;'>🥦 Pantry Scanner</h1>
    <p style='color:rgba(245,240,232,.55); margin-bottom:24px; font-size:.95rem;'>
        Upload a pantry or fridge photo — AI will detect every ingredient.
    </p>
    """, unsafe_allow_html=True)

    # ── Upload ─────────────────────────────────────────────────────────────────
    uploaded_file = st.file_uploader(
        "Upload a pantry image",
        type=["jpg", "jpeg", "png"],
        on_change=_reset,
        help="Supported formats: JPG, JPEG, PNG"
    )

    if not uploaded_file:
        st.markdown("""
        <div class='upload-placeholder'>
            <div class='up-icon'>📷</div>
            <div class='up-text'>Upload an image above to get started</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Image preview ──────────────────────────────────────────────────────────
    image    = Image.open(uploaded_file)
    image_np = np.array(image)

    col_orig, col_proc = st.columns(2)

    with col_orig:
        st.markdown("<div class='img-label'>📸 Original Image</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='padding:12px;'>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_proc:
        processed = preprocess_image(image_np)
        st.markdown("<div class='img-label'>✨ Enhanced (AI-Ready)</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='padding:12px;'>", unsafe_allow_html=True)
        st.image(processed, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Step 1: Detect ingredients ─────────────────────────────────────────────
    if st.button("🔍  Detect Ingredients", use_container_width=True):
        with st.spinner("Analysing your pantry with Gemini Vision…"):
            try:
                st.session_state["ingredients"] = detect_ingredients(image)
                st.session_state["recipes"] = None
                st.session_state["subs"]    = None
                st.session_state["health"]  = None
            except RuntimeError as e:
                st.error(f"❌ Detection failed: {e}")
                return

    # ── Detected ingredients ───────────────────────────────────────────────────
    if st.session_state["ingredients"]:
        ingredients = st.session_state["ingredients"]

        st.markdown("<div class='section-lbl'>Detected Ingredients</div>", unsafe_allow_html=True)
        pills = "".join(f"<span class='ing-pill'>{i.title()}</span>" for i in ingredients)
        st.markdown(f"<div style='margin-bottom:8px;'>{pills}</div>", unsafe_allow_html=True)

        # ── Pantry categories ──────────────────────────────────────────────────
        st.markdown("<div class='section-lbl'>Pantry Categories</div>", unsafe_allow_html=True)
        categories = categorize_items(ingredients)
        cat_cols   = st.columns(len(categories))

        for col, (cat, items) in zip(cat_cols, categories.items()):
            with col:
                items_html = (
                    "".join(f"<div class='cat-item'>• {i.title()}</div>" for i in items)
                    if items else "<div class='cat-empty'>None detected</div>"
                )
                st.markdown(f"""
                <div class='cat-card'>
                    <div class='cat-title'>{cat}</div>
                    {items_html}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Step 2: Generate recipes ───────────────────────────────────────────
        if st.button("👨‍🍳  Generate Recipes", use_container_width=True):
            with st.spinner("Crafting recipes just for you…"):
                try:
                    recipes      = generate_recipes(ingredients)
                    subs         = suggest_substitutions(ingredients)
                    health       = health_score(ingredients)

                    st.session_state["recipes"] = recipes
                    st.session_state["subs"]    = subs
                    st.session_state["health"]  = health

                    # ── Save results to outputs/results.json ───────────────────
                    if save_results:
                        save_results(
                            detected_items    = ingredients,
                            categorized_items = categorize_items(ingredients),
                            recipes           = recipes,
                            substitutions     = subs,
                            health_score      = {"score": health[0], "explanation": health[1]}
                        )

                except RuntimeError as e:
                    st.error(f"❌ Recipe generation failed: {e}")
                    return

    # ── Recipes ────────────────────────────────────────────────────────────────
    if st.session_state["recipes"]:
        recipes = st.session_state["recipes"]

        st.markdown("<div class='section-lbl'>Generated Recipes</div>", unsafe_allow_html=True)

        recipe_emojis = ["🥗", "🍳", "🫕"]
        for idx, recipe in enumerate(recipes):
            emoji      = recipe_emojis[idx % len(recipe_emojis)]
            name       = recipe.get("name", "Recipe")
            time_val   = recipe.get("time", "?")
            difficulty = recipe.get("difficulty", "?")
            ing_list   = recipe.get("ingredients", [])
            step_list  = recipe.get("steps", [])

            with st.expander(
                f"{emoji}  {name}  —  ⏱ {time_val}  ·  {difficulty}",
                expanded=(idx == 0)
            ):
                st.markdown(f"""
                <div class='recipe-meta'>
                    <span class='meta-badge'>⏱ {time_val}</span>
                    <span class='meta-badge'>📊 {difficulty}</span>
                    <span class='meta-badge'>🥄 {len(ing_list)} ingredients</span>
                    <span class='meta-badge'>📋 {len(step_list)} steps</span>
                </div>
                """, unsafe_allow_html=True)

                c_ing, c_steps = st.columns([1, 2])

                with c_ing:
                    rows = "".join(
                        f"<div class='recipe-ing-row'>"
                        f"<div class='recipe-ing-dot'></div>"
                        f"<div>{_flatten_ing(ing)}</div>"
                        f"</div>"
                        for ing in ing_list
                    )
                    st.markdown(f"""
                    <div style='margin-bottom:6px; font-size:.78rem; font-weight:700;
                                letter-spacing:.08em; text-transform:uppercase; color:#A8C09A;'>
                        🛒 Ingredients
                    </div>
                    <div class='glass-card' style='padding:14px 16px;'>
                        {rows}
                    </div>
                    """, unsafe_allow_html=True)

                with c_steps:
                    step_rows = ""
                    for i, step in enumerate(step_list, 1):
                        step_text = step if isinstance(step, str) else step.get("description", str(step))
                        step_rows += (
                            f"<div class='recipe-step-row'>"
                            f"<div class='step-num'>{i}</div>"
                            f"<div>{step_text}</div>"
                            f"</div>"
                        )
                    st.markdown(f"""
                    <div style='margin-bottom:6px; font-size:.78rem; font-weight:700;
                                letter-spacing:.08em; text-transform:uppercase; color:#A8C09A;'>
                        👨‍🍳 Steps
                    </div>
                    <div class='glass-card' style='padding:14px 16px;'>
                        {step_rows}
                    </div>
                    """, unsafe_allow_html=True)

        # ── Substitutions ──────────────────────────────────────────────────────
        st.markdown("<div class='section-lbl'>Substitution Suggestions</div>", unsafe_allow_html=True)

        subs = st.session_state.get("subs", {})
        if subs:
            sub_cols = st.columns(min(len(subs), 3))
            for col, (original, substitute) in zip(sub_cols * 10, subs.items()):
                with col:
                    st.markdown(f"""
                    <div class='sub-card'>
                        <div class='sub-icon'>🔄</div>
                        <div class='sub-from'>{original.title()}</div>
                        <div class='sub-label'>can be replaced with</div>
                        <div class='sub-to'>{substitute}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='glass-card' style='text-align:center; color:rgba(245,240,232,.55);
                        font-size:.88rem; padding:20px;'>
                ✅ No common substitutions needed for your current ingredients.
            </div>
            """, unsafe_allow_html=True)

        # ── Health score ───────────────────────────────────────────────────────
        st.markdown("<div class='section-lbl'>Pantry Health Score</div>", unsafe_allow_html=True)

        score, explanation = st.session_state.get("health", (0, ""))

        score_col, exp_col = st.columns([1, 2])

        with score_col:
            color = "#7C9A6E" if score >= 7 else "#D4A853" if score >= 4 else "#C0504A"
            label = (
                "🌟 Excellent pantry!" if score >= 8 else
                "👍 Good variety!"     if score >= 6 else
                "⚠️ Room to improve"   if score >= 4 else
                "🔴 Add more fresh items"
            )
            st.markdown(f"""
            <div class='health-score-card'>
                <div class='health-number'
                     style='color:{color}; text-shadow:0 0 28px {color}44;'>
                    {score}
                </div>
                <div class='health-denom'>out of 10</div>
                <div class='health-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

        with exp_col:
            exp_rows = ""
            for line in explanation.split("\n\n"):
                line = line.strip()
                if not line:
                    continue
                exp_rows += (
                    f"<div class='health-exp-row'>"
                    f"<div>{line}</div>"
                    f"</div>"
                )
            st.markdown(f"""
            <div class='health-exp-card'>
                <div class='health-exp-title'>What we found</div>
                {exp_rows}
            </div>
            """, unsafe_allow_html=True)