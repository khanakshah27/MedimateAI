import streamlit as st
from med import get_med_info, med_analysis, translate_output

INDIAN_LANGUAGES = [
    "English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada",
    "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali", 
    "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu"
]

st.set_page_config(page_title="MedimateAI: Medicinal Assistant", layout="wide")
st.title("MedimateAI — Medical Assistant")
st.write("Enter medicine names below to get information and analysis.")

medicine_input=st.text_area("Enter name of medicine prescribed: ")
selected_language=st.selectbox("Choose Language for Translation", INDIAN_LANGUAGES)

if "last_output" not in st.session_state:
    st.session_state.last_output = ""

if st.button("Get Medicine Info"):
    info=get_med_info(medicine_input)
    if info:
        st.subheader("Medicine Info")
        st.write(info)
        st.session_state.last_output = info
if st.button("Get Medicinal Analysis"):
    analysis=med_analysis(medicinal_input)
    if analysis:
        st.subheader("Medicinal Analysis")
        st.write(analysis)
        st.session_state.last_output = analysis
if st.button("Translate"):
    if st.session_state.last_output:
        translated = translate_output(st.session_state.last_output, selected_language)
        if translated:
            st.subheader(f"Translated Output ({selected_language})")
            st.write(translated)
    else:
        st.warning("Please generate info or analysis first before translating.")
