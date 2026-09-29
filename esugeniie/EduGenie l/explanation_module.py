"""
explanation_module.py
----------------------
Generates simple, student-friendly explanations of a topic.

Primary engine : MBZUAI/LaMini-Flan-T5-783M (local, lightweight, CPU-friendly)
Fallback engine: Google Gemini (used automatically if the local model
                  cannot be loaded — e.g. no internet on first run, or
                  not enough RAM). This keeps the server from failing to
                  start and keeps the /explain endpoint working either way.

The local model is loaded LAZILY (only the first time /explain is called),
not at import time. This is important: importing torch/transformers and
downloading a ~800MB model at server startup is a common reason the app
"hangs" or fails to open in the browser. Loading it lazily means the
server (and the rest of the UI) is available immediately.
"""

from gemini_config import get_model

# Cache so we only try to load the local model once per process
_local_tokenizer = None
_local_model = None
_local_model_failed = False


def _try_load_local_model():
    """Attempt to load the local LaMini-Flan-T5 model. Only runs once."""
    global _local_tokenizer, _local_model, _local_model_failed

    if _local_model is not None or _local_model_failed:
        return

    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

        model_name = "MBZUAI/LaMini-Flan-T5-783M"
        _local_tokenizer = AutoTokenizer.from_pretrained(model_name)
        _local_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        print("✅ Loaded local explanation model:", model_name)
    except Exception as e:
        print(f"⚠️  Could not load local explanation model ({e}). "
              f"Falling back to Gemini for /explain.")
        _local_model_failed = True


def _explain_with_local_model(topic: str) -> str:
    input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
    inputs = _local_tokenizer(input_text, return_tensors="pt")

    outputs = _local_model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        do_sample=True,
    )

    return _local_tokenizer.decode(outputs[0], skip_special_tokens=True)


def _explain_with_gemini(topic: str) -> str:
    model = get_model()
    prompt = (
        f"Explain the concept of '{topic}' in a simple, clear way for a "
        f"school student. Keep it concise (3-5 sentences)."
    )
    response = model.generate_content(prompt)
    return response.text.strip()


def explain_topic(topic: str) -> str:
    """Public entry point used by the /explain endpoint."""
    _try_load_local_model()

    if _local_model is not None:
        try:
            return _explain_with_local_model(topic)
        except Exception as e:
            print(f"⚠️  Local model failed at inference time ({e}); "
                  f"falling back to Gemini.")

    # Fallback path (local model unavailable or failed)
    try:
        return _explain_with_gemini(topic)
    except Exception as e:
        return f"⚠️ Error generating explanation: {e}"
