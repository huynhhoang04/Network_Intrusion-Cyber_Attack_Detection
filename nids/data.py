"""Loading and label helpers for the NSL-KDD dataset."""

from __future__ import annotations

import pandas as pd

from .config import COLUMNS, DATA_RAW, NAME_TO_FAMILY

FILES = {"train": "KDDTrain+.txt", "test": "KDDTest+.txt"}


def load_raw(split: str) -> pd.DataFrame:
    """Load KDDTrain+ or KDDTest+ with the 43 NSL-KDD column names."""
    if split not in FILES:
        raise ValueError(f"split must be one of {list(FILES)}, got {split!r}")
    return pd.read_csv(DATA_RAW / FILES[split], names=COLUMNS)


def load_train_test() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return the raw (train, test) pair."""
    return load_raw("train"), load_raw("test")


def to_binary_label(df: pd.DataFrame) -> pd.Series:
    """1 for any attack, 0 for normal."""
    return (df["label"] != "normal").astype(int)


def to_family_label(df: pd.DataFrame) -> pd.Series:
    """Collapse concrete attack names into Normal/DoS/Probe/R2L/U2R."""
    return df["label"].map(
        lambda name: "Normal" if name == "normal" else NAME_TO_FAMILY.get(name, "UNMAPPED")
    )


def novel_attack_types(train: pd.DataFrame, test: pd.DataFrame) -> list[str]:
    """Attack names present in test but never seen in train."""
    train_attacks = set(train["label"].unique()) - {"normal"}
    test_attacks = set(test["label"].unique()) - {"normal"}
    return sorted(test_attacks - train_attacks)
