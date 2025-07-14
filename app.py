import streamlit as st
from med import extract_text, clarify_prescription, med_analysis, translate_output

INDIAN_LANGUAGES = [
    "English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada",
    "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali", 
    "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu"
]

st.set_page_config(page_title="MediMate: Medical Image Analyzer", layout="wide")
st.title("MedimateAI — Medical Image Analysis")
st.write("Upload a prescription or medical note image to extract and analyze.")

image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if image:
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract & Clarify Prescription"):
        extracted_text = extract_text(image)
        if extracted_text.strip() == "":
            st.warning("No text detected in the image.")
        else:
            st.subheader("Extracted Text")
            st.code(extracted_text)

            clarified = clarify_prescription(extracted_text)
            if clarified:
                st.subheader("Clarified Prescription")
                st.write(clarified)

            analysis = med_analysis(extracted_text)
            if analysis:
                st.subheader("Medical Summary")
                st.write(analysis)

                target_language = st.selectbox("Translate Summary To", INDIAN_LANGUAGES)

                if st.button("Translate"):
                    translated = translate_output(analysis, target_language)
                    if translated:
                        st.subheader(f"Translated Summary ({target_language})")
                        st.write(translated)
                    else:
                        st.warning("Translation failed.")
else:
    st.info("Please upload a valid image to begin.")


