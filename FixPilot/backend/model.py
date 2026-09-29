import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

from categories import SPECS
from preprocessing import clean, encode_categoricals
from recommendations import RECOMMENDATIONS as PC_RECOMMENDATIONS

def train_model(category, path):
    spec = SPECS[category]
    df = clean(pd.read_excel(path))
    y = df.pop("problem_category").astype(str)
    categorical = [f["name"] for f in spec["features"] if f["type"] == "select"]
    X, encoders = encode_categoricals(df, categorical)
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    Xtr, Xte, ytr, yte = train_test_split(X, y_enc, test_size=.2, random_state=42, stratify=y_enc)
    clf = DecisionTreeClassifier(max_depth=12, min_samples_leaf=3, random_state=42)
    clf.fit(Xtr, ytr)
    meta = {"features": list(X.columns), "train_acc": round(accuracy_score(ytr, clf.predict(Xtr))*100,2),
            "test_acc": round(accuracy_score(yte, clf.predict(Xte))*100,2), "n_samples":len(df)}
    return clf, le, encoders, meta

def predict(category, clf, le, encoders, meta, payload):
    spec = SPECS[category]
    values = {}
    for field in spec["features"]:
        name = field["name"]
        value = payload.get(name, field.get("default", 0))
        if field["type"] == "boolean":
            value = int(bool(value))
        elif field["type"] == "number":
            value = float(value)
            value = max(field.get("min", value), min(field.get("max", value), value))
        elif value not in field.get("options", []):
            value = field.get("default", field["options"][0])
        values[name] = value
    row = pd.DataFrame([values])
    categorical = [f["name"] for f in spec["features"] if f["type"] == "select"]
    row, _ = encode_categoricals(row, categorical, encoders)
    row = row.reindex(columns=meta["features"], fill_value=0).apply(pd.to_numeric, errors="coerce").fillna(0)
    probs = clf.predict_proba(row)[0]
    label = le.inverse_transform([int(probs.argmax())])[0]
    confidence = float(probs.max()) * 100
    if category == "pc":
        rec = PC_RECOMMENDATIONS.get(label, PC_RECOMMENDATIONS["Unknown"])
    else:
        rec = {"description": f"The reported signals are most consistent with {label.lower()}.",
               "actions": spec["actions"].get(label, ["Collect more details and consult a qualified technician."]),
               "severity": "urgent" if any(x in label.lower() for x in ("unsafe","safety")) else "warn", "icon": spec["icon"]}
    detected = []
    for f in spec["features"]:
        v = values[f["name"]]
        if f["type"] == "boolean" and v:
            detected.append(f["label"])
        elif f["type"] == "number" and v > f.get("default", 0) * 1.5 and v != f.get("default", 0):
            detected.append(f"{f['label']}: {v:g}{f.get('unit','')}")
    if not detected:
        detected = ["No strong symptoms reported"]
    return {"category":category, "category_name":spec["name"], "diagnosis":label,
            "confidence":round(confidence,1), "symptoms":detected[:10],
            "actions":rec["actions"], "description":rec["description"], "severity":rec.get("severity","warn"),
            "icon":rec.get("icon",spec["icon"]),
            "model":{"algorithm":"Decision Tree","features":len(meta["features"]),"samples":meta["n_samples"],
                     "train_acc":meta["train_acc"],"test_acc":meta["test_acc"]}}
