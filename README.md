# job-postings-decoded

**What job postings actually reveal: a skills & salary dataset built directly from employer-published ATS data.**

Most public salary/skills datasets (Glassdoor, Levels.fyi, etc.) are self-reported - noisy, unverifiable, and often stale. This project takes a different approach:
it pulls **live job postings directly from the applicant-tracking systems (ATS)
companies use to publish them** (Greenhouse and Lever) via their public JSON
APIs. No login, no scraping fragility, no self-reported bias. Just what
employers actually published.

## Why this matters

- Pay-transparency laws (CA, CO, NY, WA, and others) mean a growing share of
  postings now include real, employer-disclosed salary ranges - not
  estimates.
- Skill requirements extracted directly from live postings are a more current
  signal of market demand than survey-based sources.
- This is a technique, not just a one-time dataset - the pipeline can be
  re-run at any time to get a fresh snapshot of the hiring market.


## Methodology

1. **Company list** (`scripts/company_list.py`): curated list of
   companies known to use Greenhouse or Lever.
2. **Collection** (`scripts/collect_postings.py`): pulls raw JSON from
   each company's public board API. Failures are logged, not silently
   dropped (see `data/collection_report.json` after running).
3. **Parsing** (`scripts/parse_and_clean.py`): normalizes the two
   different API schemas into one structure, and extracts:
   - disclosed salary range (regex over common pay-transparency phrasing)
   - skill mentions (keyword match against a curated skill list)
   - inferred seniority level (from job title)
4. **Final dataset** (`scripts/build_dataset.py`): dedupes and exports
   the clean, published CSV.

## Dataset card

| Field | Description |
|---|---|
| `company` | Company name (lowercase, from ATS token) |
| `ats` | Source system: `greenhouse` or `lever` |
| `title` | Job title as posted |
| `department` | Department/team, if provided |
| `location` | Location as posted (unnormalized — may include "Remote", city names, etc.) |
| `seniority` | Inferred from title keywords: intern / junior / mid / senior / lead / director / executive / unspecified |
| `salary_low`, `salary_high` | Disclosed salary range in USD, if found in the description. `null` if not disclosed. |
| `skills` | Comma-separated list of matched skill keywords found in the description |
| `skill_count` | Number of matched skills |
| `description_length` | Character length of the full description (rough proxy for posting detail/effort) |
| `posted_date` | Date posted or last updated, per source API |

### Known limitations

- **Not all postings disclose salary.** Only companies/roles subject to
  pay-transparency laws (or voluntarily disclosing) will have
  `salary_low`/`salary_high` populated. Treat missingness as
  non-random, it correlates with company location and size.
- **Skill extraction is keyword-based**, not semantic - it will miss
  skills phrased unusually and can't distinguish "5 years of Python" from
  "nice to have: Python."
- **Company list is a snapshot**, not exhaustive - it reflects a curated
  set of well-known companies at time of collection, not the full
  population of Greenhouse/Lever users.
- **Seniority inference is title-based heuristic**, not verified - titles are inconsistent across companies (a "Senior" at one company may be "Staff" at another).

## Reproducing this dataset

```bash
pip install -r requirements.txt
python scripts/collect_postings.py    # pulls raw postings -> data/raw/
python scripts/parse_and_clean.py     # extracts structured fields
python scripts/build_dataset.py       # builds final CSV -> data/processed/postings_decoded.csv
```

## License

Data is derived from publicly accessible job board APIs. This dataset is
shared for research and educational purposes. If you use it, please credit
this repository.
