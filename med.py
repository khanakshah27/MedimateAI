import os

import google.generativeai as genai
from google.api_core.exceptions import NotFound, ResourceExhausted, ServiceUnavailable

DISCLAIMER = (
    "Write for a layperson in simple, calm language. Use short sections with bold headings "
    "and bullet points. End with one line reminding the reader to consult a doctor or "
    "pharmacist before changing any treatment."
)

# Each model has its own quota, so fall through the list when one is exhausted.
DEFAULT_MODELS = [
    "models/gemini-2.5-flash",
    "models/gemini-2.5-flash-lite",
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-lite",
]
_configured = False


def _model_names():
    preferred = os.getenv("GEMINI_MODEL")
    names = ([preferred] if preferred else []) + DEFAULT_MODELS
    return list(dict.fromkeys(names))


def _configure():
    global _configured
    if not _configured:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set on the server.")
        genai.configure(api_key=api_key)
        _configured = True


_available = None


def _available_models():
    """Models this key can call for text generation, newest-looking flash models first."""
    global _available
    if _available is None:
        found = [
            m.name for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        flash = sorted((n for n in found if "flash" in n and "image" not in n and "tts" not in n), reverse=True)
        _available = flash + [n for n in found if n not in flash]
    return _available


def _candidates():
    available = _available_models()
    wanted = [n for n in _model_names() if n in available]
    return wanted + [n for n in available if n not in wanted][:6]


def _generate(prompt):
    _configure()
    last_error = None
    for name in _candidates():
        try:
            response = genai.GenerativeModel(name).generate_content(prompt)
            return response.text.strip() if response.parts else "No response."
        except (ResourceExhausted, NotFound, ServiceUnavailable) as e:
            last_error = e  # try the next model
    raise last_error or NotFound("No usable Gemini model is available for this API key.")


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
