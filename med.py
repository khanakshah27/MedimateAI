import os

import google.generativeai as genai

DISCLAIMER = (
    "Write for a layperson in simple, calm language. Use short sections with bold headings "
    "and bullet points. End with one line reminding the reader to consult a doctor or "
    "pharmacist before changing any treatment."
)

_model = None


def get_model():
    """Configure Gemini lazily so the server can boot (and report errors) without a key."""
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set on the server.")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash"))
    return _model


def _generate(prompt):
    response = get_model().generate_content(prompt)
    return response.text.strip() if response.parts else "No response."


def get_med_info(text):
    return _generate(
        f"Give simple, layman-friendly information about the following medicines:\n{text}\n"
        f"Include their use, common dosage, and warnings.\n{DISCLAIMER}"
    )


def med_analysis(text):
    return _generate(
        f"""Based on the following medicine names: {text}, identify the disease(s) or medical conditions they are commonly used to treat.
Then, provide a detailed explanation of the condition(s), including:
- What it is
- Common symptoms
- Causes
- How it spreads (if applicable)
- Standard treatments
- Preventive measures

Explain in simple, non-technical terms.
{DISCLAIMER}"""
    )


def translate_output(text, target_language):
    return _generate(
        f"Translate the following text to {target_language}. Keep the markdown formatting:\n\n{text}"
    )
