"""Data-driven, beginner-friendly explanations for the FixPilot visual library."""

import json
import re
from functools import lru_cache
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
LIBRARY_FILE = PROJECT_DIR / "visuals" / "metadata.json"


@lru_cache(maxsize=1)
def visual_library():
    with LIBRARY_FILE.open(encoding="utf-8") as source:
        return json.load(source)


def select_concept(question="", category=""):
    """Return the most relevant existing concept, never an invented asset."""
    question = str(question or "").lower()
    category = str(category or "").lower()
    keyword_matches = []
    category_matches = []
    for entry in visual_library():
        matched_keywords = [
            keyword for keyword in entry["keywords"]
            if re.search(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", question)
        ]
        if matched_keywords:
            # A direct question such as "What is RAM?" must beat the page's
            # default topic. Longer matching phrases are slightly preferred.
            score = sum(10 + len(keyword.split()) for keyword in matched_keywords)
            if category in entry.get("categories", []):
                score += 1
            keyword_matches.append((score, entry))
        elif category in entry.get("categories", []):
            category_matches.append((0, entry))

    # Use the page category only for the initial, empty prompt. A question with
    # no known concept should be answered without an unrelated visual.
    candidates = keyword_matches if question else category_matches
    if not candidates:
        return None
    _, selected = max(candidates, key=lambda candidate: candidate[0])
    asset_path = PROJECT_DIR / selected["image"].lstrip("/")
    return selected if asset_path.is_file() else None


def explanation_response(question="", category=""):
    selected = select_concept(question, category)
    if selected is None:
        return {
            "answer": "I do not have a matching visual lesson for that yet. Try asking about a specific part, such as RAM, DNS, Wi-Fi, storage, charging, cooling, updates, or power.",
            "sections": [],
            "suggestedQuestions": ["What is RAM?", "What is DNS?", "Why is my device overheating?"],
        }
    image = {
        "id": selected["id"],
        "url": selected["image"],
        "alt": selected["alt"],
        "description": selected["title"],
    }
    return {
        "answer": selected["simple"],
        "concept": selected["concept"],
        "sections": [
            {"title": selected["title"], "content": selected["simple"], "image": image},
            {"title": "Why FixPilot checks this", "content": selected["why"], "image": None},
            {"title": "A little more detail", "content": selected["deeper"], "image": None},
        ],
        "suggestedQuestions": selected["suggestions"],
    }
