import google.generativeai as genai
import  streamlit as st
import pandas as pd
import PyPDF2
import io

try:
      api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GEMENI_API_KEY")
      if not api_key:
          raise KeyError("Missing Gemini API key")
      genai.configure(api_key=api_key)
except Exception:
      st.error("API Key missing in secrets.toml. Add GEMINI_API_KEY.")

def generate_description(product_name):
      try:
          model = genai.GenerativeModel('gemini-1.5-flash')
          prompt = f"Write a catchy, professional one-sentence e-commerce product description for: {product_name}."
          return model.generate_content(prompt).text
      except:
          return f"Premium {product_name} designed for quality and style."

def generate_design_suggestions(store_name, category):
      try:
          model = genai.GenerativeModel('gemini-1.5-flash')
          prompt = f"Suggest a luxury color (HEX) and layout (Grid/List) for '{store_name}' in '{category}' category."
          return model.generate_content(prompt).text
      except:
          return "Suggested: #D4AF37, Grid, Luxury look."

def analyze_document(file_bytes, file_type):
      try:
          text = ""
          stream = io.BytesIO(file_bytes)
          if file_type == "pdf":
              reader = PyPDF2.PdfReader(stream)
              text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
          elif file_type in ["csv", "xlsx"]:
              df = pd.read_csv(stream) if file_type == "csv" else pd.read_excel(stream)
              text = df.to_string()

          if not text:
              return "Could not extract text from document."

          model = genai.GenerativeModel('gemini-1.5-flash')
          prompt = f"Generate a professional one-paragraph bio based on this: {text}"
          return model.generate_content(prompt).text
      except Exception as e:
          return f"Error: {str(e)}"