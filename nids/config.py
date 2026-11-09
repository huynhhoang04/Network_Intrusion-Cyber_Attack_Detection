"""Project-wide constants: paths, column names and attack families."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS = PROJECT_ROOT / "reports"

RANDOM_STATE = 36

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

FEATURES = COLUMNS[:-2]
CATEGORICAL = ["protocol_type", "service", "flag"]
FAMILY_ORDER = ["Normal", "DoS", "Probe", "R2L", "U2R"]

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

NAME_TO_FAMILY = {
    attack: family for family, names in ATTACK_FAMILY.items() for attack in names
}
