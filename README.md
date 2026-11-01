# MediMate AI — Rural Medicine Assistant

MediMate explains prescribed medicines and the conditions they treat in plain language, and translates the answer into 20+ Indian languages. Built to help people in rural and underserved areas understand their care.

## Features

* **Medicine info** — use, common dosage and warnings in simple words
* **Condition analysis** — what the illness is, symptoms, causes, treatment and prevention
* **Translation** — Hindi, Tamil, Bengali, Kannada, Marathi and more

## Architecture

| Part | Tech | Host |
| --- | --- | --- |
| `frontend/` | Static HTML/CSS/JS (Fraunces + Nunito Sans, pastel green) | Vercel |
| `app.py`, `med.py` | Flask API calling Gemini 2.5 Flash | Render |

**Live demo:** _add your Vercel URL here_

## Run locally

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
python app.py            # API on http://127.0.0.1:5000
```

Open `frontend/index.html` after setting `window.API_BASE = "http://127.0.0.1:5000"` in the console (or edit `API_BASE`).

API: `POST /api/info` and `/api/analysis` with `{"medicine": "..."}`; `POST /api/translate` with `{"text": "...", "language": "Hindi"}`.

## Deploy

1. **Render** — New → Blueprint → this repo (reads `render.yaml`). Add the `GEMINI_API_KEY` environment variable when prompted. Note the service URL.
2. In `frontend/index.html`, set `API_BASE` to that URL, commit and push.
3. **Vercel** — import the repo, set **Root Directory** to `frontend`, framework **Other**.
4. Optionally set `ALLOWED_ORIGINS` on Render to your Vercel URL.

Never commit your API key. Render's free tier sleeps when idle, so the first request can be slow.

> MediMate shares general information only and is not a substitute for professional medical advice.
