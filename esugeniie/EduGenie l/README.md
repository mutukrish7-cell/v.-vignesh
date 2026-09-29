# EduGenie — Google Gemini Powered Learning Assistant

A lightweight AI-powered educational assistant with 5 features:
Q&A, Explanation, Summarization, Quiz Generation, and Learning Path
recommendations. Backend: FastAPI. Frontend: HTML + CSS + vanilla JS.

---

## 1. Project structure

```
EduGenie/
├── main.py                  # FastAPI app & all API routes
├── gemini_config.py         # Loads GEMINI_API_KEY, configures the SDK
├── qna.py                   # /qa      — Gemini Q&A
├── explanation_module.py    # /explain — local model + Gemini fallback
├── summary_module.py        # /summarize — Gemini summarization
├── quiz_module.py           # /quiz    — Gemini MCQ generation
├── learning_path.py         # /learn/recommendations — Gemini
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 2. Setup in VS Code (step-by-step)

### Step 1 — Open the folder
Open VS Code → **File → Open Folder** → select the `EduGenie` folder.

### Step 2 — Open a terminal
`Terminal → New Terminal` (or `` Ctrl+` ``).

### Step 3 — Create a virtual environment
```bash
python -m venv venv
```
Activate it:
- **Windows:** `venv\Scripts\activate`
- **macOS / Linux:** `source venv/bin/activate`

VS Code may prompt "Select interpreter" — pick the `venv` one
(bottom-right corner, or `Ctrl+Shift+P → Python: Select Interpreter`).

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```
This includes `transformers` and `torch` for the local explanation
model. **These are optional** — if you'd rather skip the ~1–2 GB
download, you can remove the last two lines from `requirements.txt`
before installing. The app automatically falls back to Gemini for
`/explain` if the local model isn't available — it will never crash
the server.

### Step 5 — Add your Gemini API key
1. Get a free key at https://aistudio.google.com/app/apikey
2. Copy `.env.example` to a new file named `.env`
3. Paste your key:
   ```
   GEMINI_API_KEY=AIza...your_real_key...
   ```

### Step 6 — Run the app
```bash
uvicorn main:app --reload
```
You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Step 7 — Open it in the browser
Go to **http://127.0.0.1:8000**

---

## 3. Testing each feature

| Feature | How to test |
|---|---|
| Q&A | Type "Which is the largest ocean?" → Get Answer |
| Explanation | Type "Photosynthesis" → Explain |
| Summarize | Paste a paragraph → Summarize |
| Quiz | Type "Pythagoras theorem" → Generate Quiz → pick an option → Check Answer |
| Learning Path | Type "SQL" → Get Recommendations |

You can also test the API directly (no browser UI) via the built-in
Swagger docs at **http://127.0.0.1:8000/docs**.

---

## 4. Troubleshooting "the page won't open / server won't start"

1. **"Address already in use"** — something else is already using port
   8000. Run on a different port:
   ```bash
   uvicorn main:app --reload --port 8080
   ```
   then open http://127.0.0.1:8080

2. **Page loads but every feature shows an error** — your `.env` file
   is missing or `GEMINI_API_KEY` is empty/invalid. Double-check step 5.

3. **`ModuleNotFoundError`** — you installed packages outside the venv,
   or forgot to activate it. Re-run step 3 then step 4.

4. **Server seems to hang forever on the first `/explain` request** —
   the first call tries to download the local LaMini-Flan-T5 model
   (~800 MB) and can take a while on a slow connection. This does
   **not** block the rest of the app (Q&A, quiz, summary, learning
   path all work immediately) — only wait on the explanation feature,
   or remove `transformers`/`torch` from `requirements.txt` to skip
   the local model entirely and always use Gemini for `/explain`.

5. **`uvicorn: command not found`** — make sure your venv is activated
   (you should see `(venv)` in the terminal prompt), then
   `pip install -r requirements.txt` again.

6. Confirm the server process itself is healthy anytime by visiting
   **http://127.0.0.1:8000/health** — it should return `{"status":"ok"}`
   even if a specific AI feature is failing.

---

## 5. Notes

- All 5 endpoints (`/qa`, `/explain/`, `/summarize/`, `/quiz`,
  `/learn/recommendations`) are implemented exactly as described in
  the project documentation, using **Gemini 1.5 Pro** for Q&A,
  summarization, quiz generation, and learning paths, and the local
  **LaMini-Flan-T5-783M** model (with automatic Gemini fallback) for
  explanations.
- The frontend uses plain `fetch()` calls (no framework needed) so it
  works the same in any modern browser.
- Quiz answers are checked entirely client-side once the questions are
  generated, so clicking "Check Answer" is instant.
