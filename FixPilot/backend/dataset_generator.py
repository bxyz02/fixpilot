"""Generate deterministic, category-specific synthetic diagnostic workbooks."""
import os
import random
import sys
from pathlib import Path

import pandas as pd

from categories import SPECS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LOW_WHEN_ACTIVE = {"download_speed", "upload_speed", "signal_strength", "storage_free", "battery_voltage"}

def generate(category, rows=None):
    spec = SPECS[category]
    if rows is None:
        rows = int(os.environ.get(f"DIAGNOSTIC_ROWS_{category.upper()}", os.environ.get("DIAGNOSTIC_ROWS", "10000")))
    DATA.mkdir(exist_ok=True)
    target = DATA / spec["dataset"]
    # Preserve the project's original PC workbook unless the user explicitly
    # removes it before regeneration.
    if category == "pc" and target.exists():
        return str(target)
    rng = random.Random(4100 + list(SPECS).index(category))
    labels = spec["labels"]
    signatures = spec["signatures"]
    records = []
    fields = spec["features"]
    for i in range(rows):
        label = labels[i % len(labels)]
        row = {}
        active = set(signatures.get(label, []))
        for f in fields:
            name, kind = f["name"], f["type"]
            if kind == "boolean":
                row[name] = int(rng.random() < (0.84 if name in active else 0.035))
            elif kind == "select":
                options = f["options"]
                if name == "device_type" and name in active:
                    match = next((part for part in ("printer", "router", "monitor", "speaker") if part in label.lower()), None)
                    row[name] = match or rng.choice(options)
                else:
                    row[name] = rng.choice(options) if name not in active else options[-1]
            else:
                low, high = f.get("min", 0), f.get("max", 100)
                default = f.get("default", (low + high) / 2)
                if name in active:
                    if name in LOW_WHEN_ACTIVE:
                        value = default - (default-low)*rng.uniform(.45,.85)
                    else:
                        value = default + (high-default)*rng.uniform(.45,.9) if default < (low+high)/2 else default-(default-low)*rng.uniform(.45,.85)
                else:
                    value = rng.gauss(default, max((high-low)*.08, .5))
                row[name] = round(min(high, max(low, value)), 1)
        row["problem_category"] = label
        records.append(row)
    frame = pd.DataFrame.from_records(records)
    frame.to_excel(target, index=False)
    return str(target)

def main():
    selected = sys.argv[1:] or list(SPECS)
    for key in selected:
        if key not in SPECS:
            raise SystemExit(f"Unknown category: {key}")
        path = generate(key)
        print(f"{key}: {path}")

if __name__ == "__main__":
    main()
