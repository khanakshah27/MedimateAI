# Medimate

MediMate – AI-Powered Prescription Assistant

MediMate is a Streamlit-based web application that uses Google’s Gemini API to analyze handwritten medical prescriptions, clarify their contents in simple language, and translate the explanation into various Indian languages — making healthcare more accessible and understandable.

Features

- Image Upload: Accepts handwritten prescription images from users.
- Gemini AI Integration: Uses Google's Gemini 2.5 Flash model for prescription analysis.
- Simplified Output: Converts complex medical terms into patient-friendly language.
- Multilingual Support: Translates the summary into over 20 Indian languages.
- Streamlit Interface: Fast, interactive, and easy-to-use frontend.

Tech Stack

- Frontend: Streamlit
- Backend: Python
- AI Model: Gemini 2.5 Flash (generative-language API)
- Libraries:
  - google-generativeai
  - streamlit
  - os

Example Workflow

1. Upload a photo of your handwritten medical prescription.
2. (Optional) Choose a preferred Indian language for output.
3. The app returns a simplified and translated explanation of your prescription.
