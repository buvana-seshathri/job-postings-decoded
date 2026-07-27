"""
Phase 2: Collect Postings
---------------------------
Pulls live job postings from Greenhouse and Lever public APIs for every company in the list. 
Saves raw JSON per company to data/raw/, and logs which companies succeeded/failed to a run report.

Usage: python scripts/collect_postings.py

Requires: requests (pip install requests)
"""

import json
import time
import os
import sys
from pathlib import Path

import requests
import company_list

ALL_COMPANIES = company_list.ALL_COMPANIES

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

GREENHOUSE_URL = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
LEVER_URL = "https://api.lever.co/v0/postings/{token}?mode=json"

HEADERS = {"User-Agent": "jobs-postings-decoded-project/1.0"}
TIMEOUT = 15
SLEEP_BETWEEN_REQUESTS = 0.5  # be polite to public APIs


def fetch_greenhouse(token: str):
    url = GREENHOUSE_URL.format(token=token)
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json().get("jobs", [])


def fetch_lever(token: str):
    url = LEVER_URL.format(token=token)
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def main():
    results_log = []

    for company in ALL_COMPANIES:
        name, ats = company["name"], company["ats"]
        out_path = RAW_DIR / f"{ats}_{name}.json"

        try:
            if ats == "greenhouse":
                jobs = fetch_greenhouse(name)
            else:
                jobs = fetch_lever(name)

            with open(out_path, "w") as f:
                json.dump(jobs, f)

            print(f"[OK]   {ats:11s} {name:20s} -> {len(jobs)} postings")
            results_log.append({"company": name, "ats": ats, "status": "ok", "count": len(jobs)})

        except requests.exceptions.HTTPError as e:
            print(f"[FAIL] {ats:11s} {name:20s} -> HTTP {e.response.status_code}")
            results_log.append({"company": name, "ats": ats, "status": "failed", "error": str(e)})

        except Exception as e:
            print(f"[FAIL] {ats:11s} {name:20s} -> {e}")
            results_log.append({"company": name, "ats": ats, "status": "failed", "error": str(e)})

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    # Save a run report so failures are documented, not silently dropped
    report_path = RAW_DIR.parent / "collection_report.json"
    with open(report_path, "w") as f:
        json.dump(results_log, f, indent=2)

    ok = sum(1 for r in results_log if r["status"] == "ok")
    total_jobs = sum(r.get("count", 0) for r in results_log if r["status"] == "ok")
    print(f"\nDone. {ok}/{len(results_log)} companies succeeded, {total_jobs} total postings collected.")
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
