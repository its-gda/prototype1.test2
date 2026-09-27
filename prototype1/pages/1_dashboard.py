import streamlit as st
import os
import sys

# Fix pathing so pages can find the root modules (database and ai_helper)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database as db
import ai_helper

st.set_page_config(page_title="Builder Dashboard")

# Secure session check to prevent crashes if user accesses page directly
if 'user_id' not in st.session_state or st.session_state['user_id'] is None:
    st.error("Please login first!")
    st.stop()

user_id = st.session_state['user_id']

st.title("🛠️ Store Builder Dashboard")

# --- Section 1: Store Branding ---
st.header("1. Store Branding")
with st.expander("Edit Brand Details"):
    store_name = st.text_input("Store Name", value="My Awesome Store")
    brand_color = st.color_picker("Brand Theme Color", "#FF4B4B")
    layout = st.selectbox("Page Layout", ["Grid", "List"])
    logo_file = st.file_uploader("Upload Logo", type=["jpg", "png", "jpeg"])

    if st.button("Save Branding"):
        logo_path = None
        if logo_file:
            # Ensure uploads folder exists
            if not os.path.exists("uploads"):
                os.makedirs("uploads")
            logo_path = os.path.join("uploads", f"logo_{user_id}.png")
            with open(logo_path, "wb") as f:
                f.write(logo_file.getbuffer())

        db.update_store(user_id, store_name, brand_color, layout, logo_path)
        st.success("Branding Updated!")

# --- Section 2: Product Management ---
st.header("2. Add Products")
with st.form("product_form"):
    p_name = st.text_input("Product Name")
    p_desc = st.text_area("Description")
    p_price = st.number_input("Price ($)", min_value=0.0)
    p_link = st.text_input("External Purchase Link (Shopify/Amazon)")
    p_img = st.file_uploader("Product Image", type=["jpg", "png", "jpeg"])

    submit_p = st.form_submit_button("Save Product")

    if submit_p:
        if p_name and p_desc:
            img_path = None
            if p_img:
                if not os.path.exists("uploads"):
                    os.makedirs("uploads")
                img_path = os.path.join("uploads", f"prod_{user_id}_{p_name}.png")
                with open(img_path, "wb") as f:
                    f.write(p_img.getbuffer())
            db.add_product(user_id, p_name, p_desc, p_price, p_link, img_path)
            st.success("Product Added!")
        else:
            st.error("Name and Description are required.")

# AI Suggestion Section (Outside form for interactivity)
st.markdown("---")
st.subheader("✨ AI Assistant")
temp_name = st.text_input("Enter product name for AI description:")
if st.button("Generate AI Description"):
    if temp_name:
        suggestion = ai_helper.generate_description(temp_name)
        st.info(f"Suggested Description: {suggestion}")
    else:
        st.warning("Please enter a product name first.")

# --- Section 3: Tier Simulation ---
st.markdown("---")
st.header("3. Account Tier")
col1, col2 = st.columns(2)
with col1:
    if st.button("Stay on Free Plan"):
        db.update_user_tier(user_id, "Free")
        st.write("Free Plan: Direct link access only.")
with col2:
    if st.button("Upgrade to Premium 🌟"):
        db.update_user_tier(user_id, "Premium")
        st.success("Premium: Your store is now on the Explore page!")