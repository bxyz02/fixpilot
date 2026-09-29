import os
from pathlib import Path

from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS

from categories import CATEGORIES, SPECS
from learning import explanation_response
from model import predict, train_model
from understanding_service import UnderstandingError, ask_understanding_assistant

app = Flask(__name__)
CORS(app)
PROJECT_DIR = Path(__file__).resolve().parents[1]
PAGES_DIR = PROJECT_DIR / "pages"
DATA_DIR = PROJECT_DIR / "data"
MODELS = {}
PAGES = {
    "index": "index.html",
    "categories": "categories.html",
    "diagnosis": "diagnosis.html",
    "pc": "pc.html",
    "smartphone": "smartphone.html",
    "wifi": "wifi.html",
    "gaming": "gaming.html",
    "battery": "battery.html",
    "car": "car.html",
    "electronics": "electronics.html",
    "electrical": "electrical.html",
    "results": "results.html",
    "about": "about.html",
    "understanding": "understanding.html",
}
DIAGNOSIS_PAGES = {
    "pc": "pc.html",
    "smartphone": "smartphone.html",
    "wifi": "wifi.html",
    "gaming": "gaming.html",
    "battery": "battery.html",
    "car": "car.html",
    "home_electronics": "electronics.html",
    "electrical": "electrical.html",
}

def load_models():
    for category, spec in SPECS.items():
        path = DATA_DIR / spec["dataset"]
        if path.exists():
            MODELS[category] = train_model(category, path)
            print(f"{category}: trained on {MODELS[category][3]['n_samples']:,} rows")
        else:
            print(f"{category}: dataset missing ({path.name}); generate datasets first")

load_models()

@app.get("/")
def home():
    return send_from_directory(PAGES_DIR, "index.html")

@app.get("/<page_name>.html")
def html_page(page_name):
    filename = PAGES.get(page_name)
    if filename is None:
        return jsonify({"error": "Page not found"}), 404
    return redirect(f"/pages/{filename}")

@app.get("/pages/<filename>")
def pages(filename):
    if filename not in PAGES.values():
        return jsonify({"error": "Page not found"}), 404
    return send_from_directory(PAGES_DIR, filename)

@app.get("/diagnosis")
def diagnosis_overview():
    return send_from_directory(PAGES_DIR, "diagnosis.html")

@app.get("/diagnosis/<category>")
def diagnosis_page(category):
    filename = DIAGNOSIS_PAGES.get(category)
    if filename is None:
        return jsonify({"error": "Unknown diagnostic page"}), 404
    return redirect(f"/pages/{filename}")

@app.get("/results")
def results_page():
    return send_from_directory(PAGES_DIR, "results.html")

@app.get("/about")
def about_page():
    return send_from_directory(PAGES_DIR, "about.html")

@app.get("/understanding")
def understanding_page():
    return send_from_directory(PAGES_DIR, "understanding.html")

@app.get("/css/<path:filename>")
def css_files(filename):
    return send_from_directory(PROJECT_DIR / "css", filename)

@app.get("/js/<path:filename>")
def javascript_files(filename):
    return send_from_directory(PROJECT_DIR / "js", filename)

@app.get("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(PROJECT_DIR / "assets", filename)

@app.get("/visuals/<path:filename>")
def visuals(filename):
    return send_from_directory(PROJECT_DIR / "visuals", filename)

def category_payload():
    result = []
    for item in CATEGORIES:
        result.append({**item, "available": item["id"] in MODELS,
                       "dataset_size": MODELS[item["id"]][3]["n_samples"] if item["id"] in MODELS else 0})
    return result

@app.get("/categories")
def categories():
    # Treat wildcard and browser document requests as page navigation. JSON is
    # still available to clients that explicitly request only application/json.
    accept = request.headers.get("Accept", "")
    if request.args.get("format") == "json" or ("application/json" in accept and "text/html" not in accept):
        return jsonify(category_payload())
    return send_from_directory(PAGES_DIR, "categories.html")

@app.get("/api/categories")
def categories_api():
    return jsonify(category_payload())

@app.get("/categories/<category>")
def category_config(category):
    if category not in SPECS:
        return jsonify({"error":"Unknown category"}), 404
    spec = SPECS[category]
    return jsonify({k:spec[k] for k in ("id","name","icon","description","features","sequences","dataset")}
                   | {"available":category in MODELS})

@app.post("/diagnose")
def diagnose():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"error":"Send a JSON object containing category and data."}), 400
    category = body.get("category")
    if category not in SPECS:
        return jsonify({"error":"Choose a valid diagnostic category."}), 400
    if category not in MODELS:
        return jsonify({"error":"This category's dataset or model is unavailable."}), 503
    data = body.get("data", {})
    if not isinstance(data, dict):
        return jsonify({"error":"The data field must be an object."}), 400
    try:
        result = predict(category, *MODELS[category], data)
    except (TypeError, ValueError) as exc:
        return jsonify({"error":f"Please check the submitted values: {exc}"}), 400
    return jsonify(result)

@app.post("/explain")
def explain():
    body = request.get_json(silent=True) or {}
    if not isinstance(body, dict):
        return jsonify({"error": "Send a JSON object containing an optional question and category."}), 400
    question = str(body.get("question", "")).strip()
    category = str(body.get("category", "")).strip()
    if len(question) > 280:
        return jsonify({"error": "Keep the question under 280 characters."}), 400
    return jsonify(explanation_response(question, category))

@app.post("/api/understanding/chat")
def understanding_chat():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"error": "Send a JSON object containing a message."}), 400
    try:
        response = ask_understanding_assistant(
            message=body.get("message", ""),
            context=body.get("context"),
            history=body.get("history"),
        )
        return jsonify(response)
    except UnderstandingError as error:
        return jsonify({"error": str(error), "code": error.code}), error.status

@app.get("/health")
def health():
    return jsonify({"status":"ok", "assistant_provider":"gemini", "categories":len(SPECS), "available_models":list(MODELS),
                    "models":{key:{"samples":bundle[3]["n_samples"],"features":len(bundle[3]["features"])} for key,bundle in MODELS.items()}})

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT",5000)), debug=False)
