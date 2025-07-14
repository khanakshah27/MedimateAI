import streamlit as st
import google.generativeai as genai
import os

def get_gemini_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("GEMINI_API_KEY not found. Please set it.")
            st.stop()
        return api_key

genai.configure(api_key=get_gemini_api_key())
model = genai.GenerativeModel("models/gemini-2.5-flash")

def get_med_info(text):
    try:
        prompt = f"Give simple, layman-friendly information about the following medicines:\n{text}\nInclude their use, common dosage, and warnings."
        response = model.generate_content(prompt)
        return response.text.strip() if response.parts else "No response."
    except Exception as e:
        st.error(f"Error fetching medicine info: {e}")
        return None

def med_analysis(text):
    try:
        prompt = f"""Based on the following medicine names: {text}, identify the disease(s) or medical conditions they are commonly used to treat.
Then, provide a detailed explanation of the condition(s), including:
- What it is
- Common symptoms
- Causes
- How it spreads (if applicable)
- Standard treatments
- Preventive measures

Explain in simple, non-technical terms.
"""
        response = model.generate_content(prompt)
        return response.text.strip() if response.parts else "No response."
    except Exception as e:
        st.error(f"Error generating analysis: {e}")
        return None

def translate_output(text, target_language):
    try:
        prompt = f"Translate the following text to {target_language}:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip() if response.parts else "No response."
    except Exception as e:
        st.error(f"Error translating text: {e}")
        return None
