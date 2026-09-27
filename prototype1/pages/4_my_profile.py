import streamlit as st
import database as db
import ai_helper
import pandas as pd
import plotly.express as px
import os
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(page_title="Professional Profile")

if 'user_id' not in st.session_state: st.stop()
uid = st.session_state['user_id']

st.title("👤 Personal Profile Builder")
with st.expander("📝 Edit Details"):
      bio = st.text_area("Bio")
      skills = st.text_input("Skills")
      exp = st.text_area("Experience")
      col = st.color_picker("Theme Color", "#4A90E2")
      if st.button("Save Profile"):
          db.update_profile(uid, bio, skills, exp, col)
          st.success("Saved!")

st.subheader("🚀 AI Document Analysis")
up = st.file_uploader("Upload CV/Data (PDF, CSV, XLSX)", type=["pdf", "csv", "xlsx"])
if up:
      bytes_data = up.read()
      ext = up.name.split('.')[-1].lower()
      with st.spinner("Analyzing..."):
          res = ai_helper.analyze_document(bytes_data, ext)
          st.info(f"**AI Summary:**\n\n{res}")
          if ext in ["csv", "xlsx"]:
              df = pd.read_csv(io.BytesIO(bytes_data)) if ext=="csv" else pd.read_excel(io.BytesIO(bytes_data))
              num_cols = df.select_dtypes(include=['number']).columns
              if not num_cols.empty:
                  st.plotly_chart(px.bar(df, x=df.index, y=num_cols[0], title=f"Chart: {num_cols[0]}"))