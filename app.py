import streamlit as st 
from med import get_gemini_api_key, med_response, clarify_prescription, translate_output

st.set_page_config(page_title="Medical Image Analysis", layout="wide")
st.title("Medical Image Analysis")
st.write("Upload a medical image to clarify prescriptions, get analysis, and translate results.")


image = st.file_uploader("Upload a medical image (jpg, jpeg, png):", type=["jpg", "jpeg", "png"])
if image:
    st.image(image, caption="Uploaded Image", use_column_width=True)


    if st.button("Clarify Prescription"):
        st.session_state.show_prescription = True
        st.session_state.prescription = clarify_prescription(image)

    if st.session_state.get("show_prescription") and st.session_state.get("prescription"):
        st.subheader("Prescription Details")
        st.write(st.session_state.prescription)

      
        if st.button("Medical Analysis"):
            st.session_state.show_analysis = True
            st.session_state.analysis = med_response(image)


    if st.session_state.get("show_analysis") and st.session_state.get("analysis"):
        st.subheader("Medical Analysis")
        st.write(st.session_state.analysis)

   
        target_language = st.selectbox(
            "Select Language for Translation", 
            ["English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada",
             "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali", 
             "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu"]
        )

        if st.button("Translate"):
            translated_text = translate_output(st.session_state.analysis, target_language)
            if translated_text:
                st.subheader(f"Translated Analysis ({target_language})")
                st.write(translated_text)

else:
    st.info("Please upload a valid image to begin.")

      

