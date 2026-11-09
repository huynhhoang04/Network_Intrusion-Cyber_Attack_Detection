#!/usr/bin/env python3
"""Print descriptive statistics for the NSL-KDD dataset.

Reads data/raw/KDDTrain+.txt and data/raw/KDDTest+.txt and prints the numbers
used in the project documentation, so every figure in the docs is reproducible.

Usage:
    python scripts/profile_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nids.config import CATEGORICAL, COLUMNS, NAME_TO_FAMILY
from nids.data import to_family_label


def load(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, names=COLUMNS)


family_series = to_family_label


def profile(df: pd.DataFrame, name: str) -> None:
    print(f"\n===== {name} =====")
    print(f"shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"normal: {int((df.label == 'normal').sum()):,} "
          f"({(df.label == 'normal').mean():.1%})")

    attacks = sorted(set(df.label.unique()) - {"normal"})
    print(f"attack types: {len(attacks)}")
    print(f"attack rows: {int((df.label != 'normal').sum()):,} "
          f"({(df.label != 'normal').mean():.1%})")

    print("\nby family:")
    print(family_series(df).value_counts().to_string())

    print("\ncategorical cardinality:")
    for col in CATEGORICAL:
        print(f"  {col}: {df[col].nunique()}")

    unmapped = sorted(set(df.label.unique()) - {"normal"} - set(NAME_TO_FAMILY))
    if unmapped:
        print(f"unmapped labels: {unmapped}")

    constant = [c for c in df.columns[:-2] if df[c].nunique() == 1]
    print(f"constant features: {constant or 'none'}")
    print(f"duplicate rows: {int(df.duplicated().sum()):,}")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    train = load(root / "data/raw/KDDTrain+.txt")
    test = load(root / "data/raw/KDDTest+.txt")

    profile(train, "TRAIN (KDDTrain+.txt)")
    profile(test, "TEST (KDDTest+.txt)")

    train_attacks = set(train.label.unique()) - {"normal"}
    test_attacks = set(test.label.unique()) - {"normal"}
    novel = sorted(test_attacks - train_attacks)

    print("\n===== TRAIN vs TEST =====")
    print(f"attack types train/test: {len(train_attacks)}/{len(test_attacks)}")
    print(f"novel attack types in test ({len(novel)}):")
    print("  " + ", ".join(novel))

    for col in CATEGORICAL:
        unseen = sorted(set(test[col]) - set(train[col]))
        print(f"test values unseen in train for {col}: {unseen or 'none'}")


if __name__ == "__main__":
    main()
