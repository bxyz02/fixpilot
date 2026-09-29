"""Server-only Gemini integration for FixPilot's Understanding Assistant."""

import os
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from learning import select_concept

PROJECT_DIR = Path(__file__).resolve().parents[1]
MAX_HISTORY_MESSAGES = 12
MAX_MESSAGE_LENGTH = 1_500

SYSTEM_PROMPT = """You are FixPilot's Understanding Assistant: a technical teacher and
diagnostic explainer. Your job is to explain FixPilot technology, steps, terms, and
results to a non-technical user. You are not FixPilot's diagnostic engine.

Start with a short, plain-language answer. Use short paragraphs and a familiar analogy
when it genuinely helps. Then explain why the current FixPilot check matters and what
the user can do next. Define technical words immediately when you use them.

Use the supplied FixPilot context. Clearly label what is confirmed, user-provided,
possible, recommended, or unknown. Never claim a fault is confirmed unless the context
explicitly says so. Do not invent tests, results, symptoms, device details, or evidence.
Stay focused on FixPilot diagnostics and practical technology understanding. Do not give
dangerous electrical, vehicle, or hardware repair instructions; recommend a qualified
technician when safety is uncertain."""


class UnderstandingError(Exception):
    """Safe client-facing failure with an HTTP status."""

    def __init__(self, message, status=500, code="understanding_error"):
        super().__init__(message)
        self.status = status
        self.code = code


def load_local_environment():
    """Load missing local .env values server-side; never expose them."""
    env_path = PROJECT_DIR / ".env"
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _clean_history(history):
    if not isinstance(history, list):
        return []
    cleaned = []
    for item in history[-MAX_HISTORY_MESSAGES:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = str(item.get("content", "")).strip()
        if role in {"user", "assistant"} and content:
            cleaned.append({"role": role, "content": content[:MAX_MESSAGE_LENGTH]})
    return cleaned


def _clean_context(context):
    if not isinstance(context, dict):
        return {}
    allowed = ("category", "categoryName", "step", "stepDescription", "answers", "result")
    return {key: context[key] for key in allowed if key in context and context[key] not in (None, "", {}, [])}


def ask_understanding_assistant(message, context=None, history=None):
    """Ask Gemini with minimal, relevant FixPilot context."""
    message = str(message or "").strip()
    if not message:
        raise UnderstandingError("Type a question before sending.", 400, "empty_message")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise UnderstandingError("Keep each message under 1,500 characters.", 400, "message_too_long")

    load_local_environment()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "YOUR_KEY_HERE":
        raise UnderstandingError(
            "Understanding Assistant needs GEMINI_API_KEY in the server environment. Add it to .env, then restart FixPilot.",
            503,
            "missing_gemini_key",
        )

    safe_context = _clean_context(context)
    prompt_context = f"Current FixPilot context (may be incomplete): {safe_context!r}"
    contents = []
    for item in _clean_history(history):
        role = "model" if item["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": item["content"]}]})
    contents.append({"role": "user", "parts": [{"text": message}]})
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    request_body = json.dumps({
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT + "\n\n" + prompt_context}]},
        "contents": contents,
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 700},
    }).encode("utf-8")
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + urllib.parse.quote(model, safe="-")
        + ":generateContent?key="
        + urllib.parse.quote(api_key, safe="")
    )

    try:
        api_request = urllib.request.Request(
            endpoint, data=request_body, headers={"Content-Type": "application/json"}, method="POST"
        )
        with urllib.request.urlopen(api_request, timeout=30) as api_response:
            response = json.load(api_response)
    except urllib.error.HTTPError as error:
        error_text = error.read().decode("utf-8", "replace").lower()
        if error.code == 404 or "not_found" in error_text or "no longer available" in error_text:
            raise UnderstandingError(
                "The configured Gemini model is unavailable for this API key. "
                "Use GEMINI_MODEL=gemini-3.5-flash-lite in .env, then restart FixPilot.",
                503,
                "gemini_model_unavailable",
            ) from error
        if error.code in {429, 503} or any(marker in error_text for marker in ("high demand", "resource_exhausted", "quota", "rate limit")):
            raise UnderstandingError("Gemini is temporarily busy. Please send the question again in a moment.", 503, "gemini_busy") from error
        if error.code in {401, 403} or "api key" in error_text or "permission_denied" in error_text:
            raise UnderstandingError("The server's Gemini API key was rejected. Check GEMINI_API_KEY and restart FixPilot.", 503, "invalid_gemini_key") from error
        raise UnderstandingError("Gemini could not complete that explanation right now. Please try again.", 502, "gemini_error") from error
    except Exception as error:
        error_text = str(error).lower()
        if "timed out" in error_text:
            raise UnderstandingError("Gemini took too long to respond. Please send the question again.", 504, "gemini_timeout") from error
        raise UnderstandingError("FixPilot could not reach Gemini right now. Check your internet connection and try again.", 503, "gemini_connection_error") from error

    candidates = response.get("candidates", [])
    parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
    answer = "".join(str(part.get("text", "")) for part in parts).strip()
    if not answer:
        raise UnderstandingError("Gemini returned an empty explanation. Please try again.", 502, "empty_response")

    category = str(safe_context.get("category", ""))
    visual = select_concept(message, category)
    visual_payload = None if visual is None else {
        "id": visual["id"],
        "url": visual["image"],
        "alt": visual["alt"],
        "description": visual["title"],
    }
    return {"answer": answer, "visual": visual_payload}
