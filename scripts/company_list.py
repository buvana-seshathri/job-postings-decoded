"""
Phase 1: Company List
----------------------
Curated candidate list of companies known (as of research date 7/27/2026) to use Greenhouse or Lever or Ashby as their applicant tracking system (ATS).

IMPORTANT: Board tokens can go stale - companies switch ATS providers, rebrand career pages, or change their token slug over time. 

Token format:
  Greenhouse: https://boards-api.greenhouse.io/v1/boards/{token}/jobs
  Lever:      https://api.lever.co/v0/postings/{token}?mode=json
  Ashby:      https://api.ashbyhq.com/posting-api/job-board/{token}?includeCompensation=true

For people using this dataset: 
- To find a company's token: visit their careers page, verify they are using Greenhouse/Lever.Ashby.
- Look at the URL - boards.greenhouse.io/{token} or jobs.lever.co/{token}.
- And edit this list with the companies you wish to add.
"""
GREENHOUSE_CANDIDATES = [
    "stripe", "airbnb", "coinbase", "robinhood", "pinterest", "reddit",
    "discord", "figma", "asana", "dropbox", "gitlab", "elastic",
    "datadog", "twilio", "databricks", "mongodb", "cloudflare", "okta",
    "affirm", "brex", "instacart", "squarespace", "peloton", "lyft",
    "pagerduty", "gusto", "flexport", "checkr", "samsara", "webflow",
    "airtable", "vercel", "scaleai", "doximity", "calendly", "duolingo",
    "chime", "betterment", "sofi", "marqeta", "toast", "faire", "papaya",
    "amplitude", "mixpanel", "pendo", "postscript", "attentive",
    "klaviyo", "braze", "iterable", "customerio", "intercom", "sendbird",
    "algolia", "contentful", "storyblok", "lattice", "planetscale",
    "cockroachlabs", "launchdarkly", "nuro", "dataiku", "postman",
    "netlify", "carta", "clever", "branch", "fivetran", "imgur",
    "salesloft", "kickstarter", "linkedin", "planetlabs", "showpad",
    "dialpad", "pulley", "mercury", "found", "alloy", "project44",
    "hubspot", "anthropic", "tripadvisor", "forbes", "turing",
    "seatgeek", "tailscale", "taskrabbit", "twitch", "udemy",
    "wikimedia", "ziprecruiter", "relativity", "ripple", "axon",
    "bitwarden", "chainguard", "warp", "circleci", "cribl",
    "dremio", "formlabs", "hightouch", "karat", "labelbox",
    "newsela", "nexhealth", "starburst", "triplelift", "udacity",
    "workato", "clickhouse", "couchbase", 
]

LEVER_CANDIDATES = [
    "netflix", "palantir", "ro", "kraken", "gettyimages",
    "outreach", "clari", "highspot", "aircall", "angellist",
    "zeta", "rackspace", "meesho", "kpmg", "spotify",
    "gopuff", "swordhealth", "alltrails", "benchsci",
]

ASHBY_CANDIDATES = [
    "cursor", "supabase", "mercury", "vercel", "substack", "docker",
    "cointracker", "coder", "helpscout", "altura", "alan", "amo",
    "aurorasolar", "avid4", "boomi", "brightline", "deliveroo", "hiya",
    "kong", "oyster", "clay", "confluent", "cerebral", "check", "finch",
    "luma", "mintlify", "orb", "paradigm", "ponder", "render", "resend",
    "stackblitz", "turso", "windsurf", "captions", "factory", "baseten",
    "decagon", "physicsx", "harmonic", "camber", "fern", "arcadia",
]

ALL_COMPANIES = (
    [{"name": c, "ats": "greenhouse"} for c in GREENHOUSE_CANDIDATES]
    + [{"name": c, "ats": "lever"} for c in LEVER_CANDIDATES]
    + [{"name": c, "ats": "ashby"} for c in ASHBY_CANDIDATES]
)

if __name__ == "__main__":
    print(f"Total candidate companies: {len(ALL_COMPANIES)}")
    print(f"  Greenhouse: {len(GREENHOUSE_CANDIDATES)}")
    print(f"  Lever: {len(LEVER_CANDIDATES)}")
    print(f"  Ashby: {len(ASHBY_CANDIDATES)}")