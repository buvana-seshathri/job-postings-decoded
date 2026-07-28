"""
Phase 4: Build Final Dataset
-------------------------------
Converts the parsed JSON into a clean, published-ready CSV. Adds a US
location flag and filters the published dataset to US-only postings,
since the salary-disclosure story is specifically about US pay-
transparency laws (CA, CO, NY, WA, etc.) — mixing in non-US postings
understates how often US companies actually disclose.

Outputs two files:
  - postings_decoded.csv       -> US-only postings (this is the one to publish)
  - postings_decoded_all.csv   -> full dataset, all locations, with an
                                   is_us column, kept for transparency

Usage: python scripts/build_dataset.py

Requires: pandas (pip install pandas)
"""

import json
import re
from pathlib import Path

import pandas as pd

IN_PATH = Path(__file__).parent.parent / "data" / "processed" / "postings_raw_parsed.json"
OUT_PATH_US = Path(__file__).parent.parent / "data" / "processed" / "postings_decoded.csv"
OUT_PATH_ALL = Path(__file__).parent.parent / "data" / "processed" / "postings_decoded_all.csv"

US_STATE_ABBR = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC",
}

US_STATE_NAMES = {
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
    "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
    "maine", "maryland", "massachusetts", "michigan", "minnesota",
    "mississippi", "missouri", "montana", "nebraska", "nevada",
    "new hampshire", "new jersey", "new mexico", "new york",
    "north carolina", "north dakota", "ohio", "oklahoma", "oregon",
    "pennsylvania", "rhode island", "south carolina", "south dakota",
    "tennessee", "texas", "utah", "vermont", "virginia", "washington",
    "west virginia", "wisconsin", "wyoming",
}

# Common phrasing for US-based remote roles, which won't match a state name
US_EXPLICIT_MARKERS = [
    "united states", "usa", "u.s.a", "u.s.", "(us)", " us)", "- us",
    "us -", "remote - us", "remote, us", "remote (us)", "remote-us",
    "us remote", "united states of america",
]

# Common non-US giveaways — catches things like "Remote - Canada",
# "United Kingdom", "Bengaluru, India" so they don't accidentally match
# a US state name substring (e.g. "Georgia" the country).
NON_US_MARKERS = [
    "canada", "united kingdom", "uk", "india", "germany", "france",
    "spain", "netherlands", "ireland", "australia", "singapore",
    "brazil", "mexico", "poland", "portugal", "philippines", "japan",
    "china", "israel", "sweden", "switzerland", "italy", "georgia,",
    # trailing comma above avoids matching US state "Georgia" alone
]

# Keywords that indicate a software/tech/CS-adjacent role. Checked against
# both job title and department — a role only needs to match one field.
CS_ROLE_KEYWORDS = [
    "software engineer", "swe", "backend", "back-end", "back end",
    "frontend", "front-end", "front end", "full stack", "fullstack",
    "full-stack", "developer", "programmer", "devops", "sre",
    "site reliability", "platform engineer", "infrastructure engineer",
    "cloud engineer", "systems engineer", "network engineer",
    "security engineer", "cybersecurity", "qa engineer", "test engineer",
    "quality engineer", "data engineer", "data scientist",
    "data science", "machine learning", "ml engineer", "ai engineer",
    "applied scientist", "research scientist", "research engineer",
    "computer vision", "nlp engineer", "mobile engineer",
    "ios engineer", "android engineer", "embedded engineer",
    "firmware engineer", "database administrator", "dba",
    "solutions engineer", "engineering manager", "tech lead",
    "technical lead", "software architect", "principal engineer",
    "staff engineer", "product engineer",
]

CS_DEPARTMENT_KEYWORDS = [
    "engineering", "software", "computer", "computing", "informatics",
    "information systems", "information technology", "it", "technology",
    "tech", "data", "artificial intelligence", "ai", "machine learning",
    "cybersecurity", "security", "cloud", "infrastructure", "platform",
    "devops", "systems", "research", "quality assurance", "qa", "testing", 
    "mobile", "embedded", "firmware", "database", "solutions", "product",
]

def is_us_location(location: str) -> bool:
    if not location:
        return False
    loc = location.strip()
    loc_lower = loc.lower()

    # Explicit non-US country mentions take priority
    if any(marker in loc_lower for marker in NON_US_MARKERS):
        return False

    # Explicit US mentions
    if any(marker in loc_lower for marker in US_EXPLICIT_MARKERS):
        return True

    # Pattern: "City, XX" where XX is a US state abbreviation
    match = re.search(r",\s*([A-Za-z]{2})\b", loc)
    if match and match.group(1).upper() in US_STATE_ABBR:
        return True

    # Full state name mentioned anywhere in the string
    if any(state in loc_lower for state in US_STATE_NAMES):
        return True

    return False


def is_cs_role(title: str, department: str) -> bool:
    title_lower = (title or "").lower()
    dept_lower = (department or "").lower()

    if any(kw in title_lower for kw in CS_ROLE_KEYWORDS):
        return True
    if any(kw in dept_lower for kw in CS_DEPARTMENT_KEYWORDS):
        return True
    return False


def main():
    with open(IN_PATH) as f:
        records = json.load(f)

    df = pd.DataFrame(records)

    # Flatten skills list into a comma-separated string + a count column
    df["skills"] = df["skills"].apply(lambda s: ",".join(s) if s else "")
    df["skill_count"] = df["skills"].apply(lambda s: len(s.split(",")) if s else 0)

    # Drop duplicates (same company + title + location posted twice)
    before = len(df)
    df = df.drop_duplicates(subset=["company", "title", "location"])
    print(f"Dropped {before - len(df)} duplicate postings.")

    # Classify US vs non-US based on the location string
    df["is_us"] = df["location"].apply(is_us_location)

    # Classify tech/CS roles based on title + department
    df["is_cs_role"] = df.apply(
        lambda row: is_cs_role(row["title"], row["department"]), axis=1
    )

    # Reorder columns for readability
    df = df[[
        "company", "ats", "title", "department", "location", "is_us",
        "is_cs_role", "seniority", "salary_low", "salary_high", "skills",
        "skill_count", "description_length", "posted_date",
    ]]

    # Save the full dataset (all locations, all roles) for transparency
    df.to_csv(OUT_PATH_ALL, index=False)

    # Save US-only, CS-roles-only — this is the one to publish
    df_us_cs = df[df["is_us"] & df["is_cs_role"]].drop(columns=["is_us", "is_cs_role"])
    df_us_cs.to_csv(OUT_PATH_US, index=False)

    us_count = df["is_us"].sum()
    cs_count = df["is_cs_role"].sum()
    total = len(df)
    print(f"\nLocation breakdown: {us_count}/{total} ({us_count/total*100:.1f}%) US-based")
    print(f"Role breakdown: {cs_count}/{total} ({cs_count/total*100:.1f}%) CS/tech roles")

    print(f"\nFull dataset (all locations, all roles): {len(df)} postings across {df['company'].nunique()} companies")
    print(f"  -> saved to {OUT_PATH_ALL}")

    print(f"\nUS + CS-role dataset: {len(df_us_cs)} postings across {df_us_cs['company'].nunique()} companies")
    print(f"  -> saved to {OUT_PATH_US}")

    with_salary_final = df_us_cs["salary_low"].notna().sum()
    print(f"\nUS + CS-role salary disclosure rate: {with_salary_final}/{len(df_us_cs)} "
          f"({with_salary_final/len(df_us_cs)*100:.1f}%)")

    with_salary_all = df["salary_low"].notna().sum()
    print(f"All-locations/all-roles salary disclosure rate: {with_salary_all}/{len(df)} "
          f"({with_salary_all/len(df)*100:.1f}%)")


if __name__ == "__main__":
    main()