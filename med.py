

import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

st.write("Gemini SDK Version:", genai.__version__)


def get_gemini_api_key():
    """Get Gemini API key from Streamlit secrets or environment variables."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("GEMINI_API_KEY not found. Please add it to secrets.toml or .env.")
            st.stop()
        return api_key

genai.configure(api_key=get_gemini_api_key())
model = genai.GenerativeModel("gemini-pro-vision")


def med_response(image_file):
    try:
        image = Image.open(image_file)
        response = model.generate_content(
            parts=[
                image,
                "Analyze the medical image and provide a detailed report."
            ],
            generation_config={
                "max_output_tokens": 1000,
                "temperature": 0.5
            }
        )
        if response.parts:
            return response.text.strip()
        else:
            st.warning("No content returned. It may have been blocked.")
            return None
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

def clarify_prescription(image_file):
    try:
        image = Image.open(image_file)
        response = model.generate_content(
            parts=[
                image,
                "Clarify the prescription details from this medical image."
            ],
            generation_config={
                "max_output_tokens": 500,
                "temperature": 0.5
            }
        )
        if response.parts:
            return response.text.strip()
        else:
            st.warning("No content returned. It may have been blocked.")
            return None
    except Exception as e:
        st.error(f"Error clarifying prescription: {e}")
        return None

def translate_output(text, target_language):
    try:
        prompt = f"Translate the following medical summary into {target_language}:\n\n{text}"
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 500,
                "temperature": 0.5
            }
        )
        if response.parts:
            return response.text.strip()
        else:
            st.warning("No content returned. It may have been blocked.")
            return None
    except Exception as e:
        st.error(f"Error translating text: {e}")
        return None
