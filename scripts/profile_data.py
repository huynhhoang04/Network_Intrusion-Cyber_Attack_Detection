#!/usr/bin/env python3
"""Print descriptive statistics for the NSL-KDD dataset.

Reads data/raw/KDDTrain+.txt and data/raw/KDDTest+.txt and prints the numbers
used in the project documentation, so every figure in the docs is reproducible.

Usage:
    python scripts/profile_data.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate", "label", "difficulty",
]

ATTACK_FAMILY = {
    "DoS": [
        "back", "land", "neptune", "pod", "smurf", "teardrop", "mailbomb",
        "processtable", "udpstorm", "apache2", "worm",
    ],
    "Probe": ["satan", "ipsweep", "nmap", "portsweep", "mscan", "saint"],
    "R2L": [
        "ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy",
        "warezclient", "warezmaster", "xlock", "xsnoop", "snmpguess",
        "snmpgetattack", "httptunnel", "sendmail", "named",
    ],
    "U2R": [
        "buffer_overflow", "loadmodule", "perl", "rootkit", "sqlattack",
        "xterm", "ps",
    ],
}

NAME_TO_FAMILY = {attack: family for family, names in ATTACK_FAMILY.items() for attack in names}
CATEGORICAL = ["protocol_type", "service", "flag"]


def load(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, names=COLUMNS)


def family_series(df: pd.DataFrame) -> pd.Series:
    return df["label"].map(
        lambda x: "Normal" if x == "normal" else NAME_TO_FAMILY.get(x, "UNMAPPED")
    )


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
