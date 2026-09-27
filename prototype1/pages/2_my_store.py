import sys, os
import streamlit as st

  # Ensure the app can find the database.py file in the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db

st.set_page_config(page_title="Public Store Preview")

def get_contrast_color(hex_color):
      try:
          h = hex_color.lstrip('#')
          rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
          # Returns black for light backgrounds, white for dark backgrounds
          return "black" if ((0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2])/255) > 0.5 else "white"
      except:
          return "black"

  # 1. Security Check: Ensure user is logged in
if st.session_state.get('user_id') is None:
      st.error("Please login first!")
      st.stop()

  # 2. Fetch Store Data
store = db.get_store_details(st.session_state['user_id'])
if not store:
      st.warning("Your store is not set up yet! Please go to the Dashboard.")
      st.stop()

  # FIX: Correct unpacking of the store tuple
  # store indices: 0:user_id, 1:store_name, 2:logo_path, 3:brand_color, 4:layout, 5:animation_style
user_id = store[0]
name = store[1]
logo = store[2]
color = store[3]
layout = store[4]
animation = store[5]

text_col = get_contrast_color(color)

  # 3. Animation Logic
if animation == "Fade":
      anim_css = "@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }"
      card_animation = "fadeIn"
else:
      anim_css = "@keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }"
      card_animation = "slideUp"

  # 4. Dynamic Styling
st.markdown(f"""
      <style>
      @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter&display=swap');

      .stApp {{
          background-color: {color};
          font-family: 'Inter';
      }}

      {anim_css}

      .store-title {{
          text-align: center;
          font-family: 'Playfair Display';
          font-size: 42px;
          color: {text_col};
          animation: {card_animation} 1.5s;
          margin-bottom: 20px;
      }}

      .product-card {{
          background: rgba(255,255,255,0.2);
          backdrop-filter: blur(10px);
          border-radius: 15px;
          padding: 20px;
          color: {text_col};
          animation: {card_animation} 1s;
          margin-bottom: 10px;
      }}
      </style>
      """, unsafe_allow_html=True)

  # 5. Store Header
st.markdown(f'<div class="store-title">{name}</div>', unsafe_allow_html=True)
if logo:
      st.image(logo, width=150)

  # 6. Products Display
products = db.get_products(st.session_state['user_id'])

if not products:
      st.info("No products added to the store yet.")
elif layout == "Grid":
      cols = st.columns(2)
      for i, p in enumerate(products):
          with cols[i % 2]:
              # p indices: 0:id, 1:user_id, 2:name, 3:desc, 4:price, 5:link, 6:image_path
              image_html = f'<img src="{p[6]}" style="width:100%; border-radius:10px;">' if p[6] else ''
              st.markdown(
                  f'''
                  <div class="product-card">
                    {image_html}
                    <div style="font-weight:bold; font-size:18px;">{p[2]}</div>
                    <div style="font-size:14px;">{p[3]}</div>
                    <div style="font-weight:bold; font-size:20px; margin-top:10px;">${p[4]}</div>
                  </div>
                  ''',
                  unsafe_allow_html=True,
              )
              st.link_button("Buy Now", p[5], use_container_width=True)
else:
      # List Layout
      for p in products:
          st.markdown(f'''
              <div class="product-card">
                  <b>{p[2]}</b> — {p[3]} — <b style="font-size:18px;">${p[4]}</b>
              </div>
              ''', unsafe_allow_html=True)
          st.link_button("Buy Now", p[5], use_container_width=True)