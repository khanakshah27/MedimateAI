import streamlit as st 
from med import get_gemini_api_key, med_response, clarify_prescription, translate_output

st.set_page_config(page_title="Medical Image Analysis", layout="wide")
st.title("Medical Image Analysis")
st.write("Upload a medical image to analyze it.")
image= st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
if image:
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Clarify Prescription"):
        prescription = clarify_prescription(image)
        if prescription:
            st.subheader("Prescription Details")
            st.write(prescription)
            if st.button("Medical Analysis"):
                analysis = med_response(image)
                if analysis:
                    st.subheader("Medical Analysis")
                    st.write(analysis)
                    
                    target_language = st.selectbox("Select Language for Translation", ["English","Assamese","Bengali","Bodo","Dogri","Gujarati","Hindi","Kannada","Kashmiri","Konkani","Maithili","Malayalam", "Manipuri","Marathi","Nepali","Odia","Punjabi","Sanskrit","Santali","Sindhi","Tamil","Telugu","Urdu"])
                    if st.button("Translate"):
                        translated_text = translate_output(analysis, target_language)
                        if translated_text:
                            st.subheader(f"Translated Analysis ({target_language})")
                            st.write(translated_text)
                else:
                    st.error("Failed to generate medical analysis.")
      

