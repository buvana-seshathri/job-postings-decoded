"""
Phase 4: Build Final Dataset
-------------------------------
Converts the parsed JSON into a clean, published-ready CSV. This is the
file that gets committed to data/processed/ and published to
GitHub / Kaggle.

Usage: python scripts/build_dataset.py

Requires: pandas (pip install pandas)
"""

import json
from pathlib import Path

import pandas as pd

IN_PATH = Path(__file__).parent.parent / "data" / "processed" / "postings_raw_parsed.json"
OUT_PATH = Path(__file__).parent.parent / "data" / "processed" / "postings_decoded.csv"


def main():
    with open(IN_PATH) as f:
        records = json.load(f)

    df = pd.DataFrame(records)

    # Flatten skills list into a comma-separated string + a count column
    df["skills"] = df["skills"].apply(lambda s: ",".join(s) if s else "")
    df["skill_count"] = df["skills"].apply(lambda s: len(s.split(",")) if s else 0)

    # Drop if any duplicates (same company + title + location posted twice)
    before = len(df)
    df = df.drop_duplicates(subset=["company", "title", "location"])
    print(f"Dropped {before - len(df)} duplicate postings.")

    # Reorder columns for readability
    df = df[[
        "company", "ats", "title", "department", "location", "seniority",
        "salary_low", "salary_high", "skills", "skill_count",
        "description_length", "posted_date",
    ]]

    df.to_csv(OUT_PATH, index=False)

    print(f"\nFinal dataset: {len(df)} postings across {df['company'].nunique()} companies")
    print(f"Saved to {OUT_PATH}")
    print("\nColumn summary:")
    print(df.describe(include="all").T[["count"]])

if __name__ == "__main__":
    main()
