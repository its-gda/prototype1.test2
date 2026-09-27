import streamlit as st
import database as db

st.set_page_config(page_title="Explore Stores")

st.title("🌟 Explore Featured Stores")
st.markdown("Discover the best stores on our platform.")

premium_stores = db.get_all_premium_stores()

if not premium_stores:
    st.info("No premium stores to show yet. Be the first to upgrade!")
else:
    # Create a card-like grid
    cols = st.columns(3)
    for i, store in enumerate(premium_stores):
        with cols[i % 3]:
            # store = (name, logo, username)
            if store[1]:
                st.image(store[1], width=100)
            st.markdown(f"**{store[0]}**")
            st.caption(f"by @{store[2]}")
            st.markdown("---")