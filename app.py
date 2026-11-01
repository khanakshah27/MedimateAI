import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from med import get_med_info, med_analysis, translate_output

app = Flask(__name__)
CORS(app, origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","))

INDIAN_LANGUAGES = [
    "English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada",
    "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali",
    "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu",
]
MAX_CHARS = 500
MAX_TRANSLATE_CHARS = 8000


def _json_text(field, limit):
    data = request.get_json(silent=True) or {}
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()[:limit]


def _run(fn, *args):
    try:
        return jsonify({"result": fn(*args)})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.exception("Gemini request failed")
        name = type(e).__name__
        hints = {
            "PermissionDenied": "The Gemini API key was rejected. Check GEMINI_API_KEY on the server.",
            "InvalidArgument": "The Gemini API key or request was invalid. Check GEMINI_API_KEY on the server.",
            "Unauthenticated": "The Gemini API key was rejected. Check GEMINI_API_KEY on the server.",
            "NotFound": "The configured Gemini model was not found.",
            "ResourceExhausted": "The Gemini quota has been reached. Please try again later.",
        }
        msg = hints.get(name, "The assistant is unavailable right now. Please try again shortly.")
        return jsonify({"error": msg, "detail": name}), 502


@app.route("/")
def home():
    return jsonify({"service": "medimate-ai", "status": "ok"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/languages")
def languages():
    return jsonify(INDIAN_LANGUAGES)


@app.route("/api/info", methods=["POST"])
def info():
    medicine = _json_text("medicine", MAX_CHARS)
    if not medicine:
        return jsonify({"error": "Please enter a medicine name."}), 400
    return _run(get_med_info, medicine)


@app.route("/api/analysis", methods=["POST"])
def analysis():
    medicine = _json_text("medicine", MAX_CHARS)
    if not medicine:
        return jsonify({"error": "Please enter a medicine name."}), 400
    return _run(med_analysis, medicine)


@app.route("/api/translate", methods=["POST"])
def translate():
    text = _json_text("text", MAX_TRANSLATE_CHARS)
    language = _json_text("language", 40)
    if not text or language not in INDIAN_LANGUAGES:
        return jsonify({"error": "Generate some information first, then choose a language."}), 400
    return _run(translate_output, text, language)


if __name__ == "__main__":
    app.run(debug=True)
