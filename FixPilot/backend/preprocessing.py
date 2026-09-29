import pandas as pd

BOOL_COLS = [
    "random_shutdowns", "blue_screen", "freezing", "crashes",
    "slow_startup", "screen_artifacts", "black_screen",
    "boot_failure", "disk_errors", "internet_problems",
    "wifi_problems", "recent_driver_update",
    "recent_windows_update", "malware_symptoms",
    "overheating", "loud_fans", "performance_slowdown",
    "application_crashes", "system_restarts",
    "power_issues", "error_messages",
]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in BOOL_COLS:
        if c in df.columns:
            df[c] = (
                df[c].astype(str).str.lower()
                .map({"yes": 1, "true": 1, "1": 1, "no": 0, "false": 0, "0": 0})
                .fillna(0)
            )
    df = df.fillna(df.median(numeric_only=True))
    return df


def encode_categoricals(df: pd.DataFrame, cols, fitted=None):
    df = df.copy()
    out = {}
    for c in cols:
        if c not in df.columns:
            continue
        if fitted and c in fitted:
            df[c] = df[c].astype(str).map(fitted[c]).fillna(0)
        else:
            mapping = {v: i for i, v in enumerate(df[c].astype(str).unique())}
            df[c] = df[c].astype(str).map(mapping)
            out[c] = mapping
    return df, out
