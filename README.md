# postings-decoded

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
