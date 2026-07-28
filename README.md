# job-postings-decoded

**What job postings actually reveal: a skills & salary dataset built directly from employer-published ATS data — filtered to US-based tech roles.**

Most public salary/skills datasets (Glassdoor, Levels.fyi, etc.) are self-reported,
noisy, unverifiable, and often stale. This project takes a different approach:
it pulls **live job postings directly from the applicant-tracking systems (ATS)
companies use to publish them** (Greenhouse and Lever) via their public JSON
APIs. No login, no scraping fragility, no self-reported bias. Just what
employers actually published.

**[X,XXX] postings across [X]+ US-based tech companies.**

## Why this matters

- Pay-transparency laws (CA, CO, NY, WA, and others) mean a growing share of
  US postings now include real, employer-disclosed salary ranges; not
  estimates. This dataset is scoped to US postings specifically so that
  disclosure-rate findings are measuring the right thing.
- Skill requirements extracted directly from live postings are a more current
  signal of market demand than survey-based sources.
- This is a technique, not just a one-time dataset, the pipeline can be
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
4. **Final dataset** (`scripts/build_dataset.py`): dedupes, classifies
   each posting as US/non-US and CS-role/non-CS-role, and exports two files:
   - `postings_decoded.csv`: **US-only, CS/tech roles only** (the published dataset)
   - `postings_decoded_all.csv`: full unfiltered dataset with `is_us` /
     `is_cs_role` flags, kept for transparency

## Dataset card

| Field | Description |
|---|---|
| `company` | Company name (lowercase, from ATS token) |
| `ats` | Source system: `greenhouse` or `lever` |
| `title` | Job title as posted |
| `department` | Department/team, if provided |
| `location` | Location as posted (unnormalized) |
| `seniority` | Inferred from title keywords: intern / junior / mid / senior / lead / director / executive / unspecified |
| `salary_low`, `salary_high` | Disclosed salary range in USD, if found in the description. `null` if not disclosed. |
| `skills` | Comma-separated list of matched skill keywords found in the description |
| `skill_count` | Number of matched skills |
| `description_length` | Character length of the full description |
| `posted_date` | Date posted or last updated, per source API |

`postings_decoded_all.csv` additionally includes `is_us` and `is_cs_role` boolean columns.

### Scope: US + tech/CS roles only

The published dataset (`postings_decoded.csv`) is filtered to:
- **US-based postings**, classified from the location string (state
  abbreviations, state names, and explicit country markers)
- **CS/tech roles**, classified from job title and department keywords
  (software engineer, data scientist, DevOps, ML engineer, etc.)

This scoping exists because the salary-disclosure finding is specifically
about US pay-transparency law compliance, mixing in international
postings or non-technical roles would dilute and mislabel that signal.

### Known limitations

- **Not all postings disclose salary.** Only companies/roles subject to
  pay-transparency laws (or voluntarily disclosing) will have
  `salary_low`/`salary_high` populated. Treat missingness as
  non-random; it correlates with company location and size.
- **US/non-US classification is heuristic, not exact.** Location strings
  are inconsistent across companies; postings labeled just "Remote" with
  no country are excluded even if likely US-based, so the true US count
  is probably a slight undercount, not overcount.
- **CS-role classification is keyword-based**, not a verified taxonomy;
  it will miss unusually-phrased titles and may include some borderline
  technical-adjacent roles (e.g. technical program managers).
- **Skill extraction is keyword-based**, not semantic.
- **Company list is a curated sample**, not exhaustive.
- **Seniority inference is title-based heuristic**, not verified.

## Reproducing this dataset

```bash
pip install -r requirements.txt
python scripts/collect_postings.py    # pulls raw postings -> data/raw/
python scripts/parse_and_clean.py     # extracts structured fields
python scripts/build_dataset.py       # builds final CSVs -> data/processed/
```

## Project roadmap

- [x] Dataset collection, parsing, US/CS-role filtering, and publication
- [ ] Exploratory analysis
- [ ] Model (salary prediction / seniority classification / skill clustering)
- [ ] Findings writeup

## License

CC BY 4.0: free to use, share, and adapt, with attribution to this
repository. Data is derived from publicly accessible job board APIs;
this project is not affiliated with or endorsed by Greenhouse or Lever.