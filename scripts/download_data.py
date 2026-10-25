#!/usr/bin/env python3
"""Download the NSL-KDD dataset used by this project.

The Kaggle page referenced in TOPIC.md requires an authenticated account, so the
files are pulled by default from the public `defcom17/NSL_KDD` GitHub mirror,
which hosts the exact same KDDTrain+ / KDDTest+ files. Download with the Kaggle
CLI manually if you prefer:

    kaggle datasets download -d hassan06/nslkdd -p data/raw --unzip

Usage:
    python scripts/download_data.py            # skip files already present
    python scripts/download_data.py --force    # re-download everything
"""

from __future__ import annotations

import argparse
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master"

# filename -> expected number of lines (each line = 41 features + label + difficulty)
FILES = {
    "KDDTrain+.txt": 125_973,
    "KDDTest+.txt": 22_544,
}

N_COLUMNS = 43


def download(url: str, dest: Path) -> None:
    """Download `url` to `dest` atomically, showing a progress line."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        done = 0
        with tmp.open("wb") as out:
            while chunk := resp.read(1 << 16):
                out.write(chunk)
                done += len(chunk)
                if total:
                    pct = done * 100 / total
                    print(
                        f"\r  {done / 1e6:6.2f}/{total / 1e6:.2f} MB ({pct:5.1f}%)",
                        end="",
                        flush=True,
                    )
    tmp.replace(dest)
    print("\r" + " " * 44 + "\r", end="")


def verify(path: Path, expected_lines: int) -> tuple[bool, str]:
    """Check line count and that every row has the expected number of fields."""
    n_lines = 0
    with path.open("r", encoding="utf-8", errors="strict") as f:
        for i, line in enumerate(f, start=1):
            if not line.strip():
                continue
            n_lines += 1
            if line.count(",") + 1 != N_COLUMNS:
                return False, f"line {i}: expected {N_COLUMNS} fields, got {line.count(',') + 1}"
    if n_lines != expected_lines:
        return False, f"expected {expected_lines} lines, found {n_lines}"
    return True, f"{n_lines} lines, {N_COLUMNS} fields OK"


def main() -> int:
    parser = argparse.ArgumentParser(description="Download the NSL-KDD dataset")
    parser.add_argument(
        "--output-dir",
        default="data/raw",
        help="destination directory (default: data/raw)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="re-download even if the file already exists",
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for name, expected_lines in FILES.items():
        dest = out_dir / name
        print(f"[{name}]")

        if dest.exists() and not args.force:
            ok, msg = verify(dest, expected_lines)
            if ok:
                print(f"  already present, {msg}")
                continue
            print(f"  existing file invalid ({msg}); re-downloading")

        url = f"{BASE_URL}/{urllib.parse.quote(name)}"
        print(f"  downloading from {BASE_URL}")
        try:
            download(url, dest)
        except Exception as exc:  # network / HTTP errors
            print(f"  ERROR: {exc}", file=sys.stderr)
            failures += 1
            continue

        ok, msg = verify(dest, expected_lines)
        if ok:
            print(f"  verified: {msg}")
        else:
            print(f"  VERIFY FAILED: {msg}", file=sys.stderr)
            failures += 1

    if failures:
        print(f"\n{failures} file(s) failed.", file=sys.stderr)
        return 1
    print(f"\nDone. Dataset ready in {out_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
