import streamlit as st
from PIL import Image
import pytesseract
import google.generativeai as genai
import os

# Setup Gemini
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def extract_text(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

def clarify_prescription(text):
    try:
        prompt = f"Clarify the following prescription: \n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Gemini error: {e}")
        return None

def med_analysis(text):
    try:
        prompt = f"Analyze this medical note and provide a summary: \n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Gemini error: {e}")
        return None

def translate_output(text, lang):
    try:
        prompt = f"Translate the following medical text to {lang}:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Gemini error: {e}")
        return None
