"""
Phase 1: Company List
----------------------
Curated candidate list of companies known (as of research date 7/27/2026) to use Greenhouse or Lever as their applicant tracking system (ATS).

IMPORTANT: Board tokens can go stale - companies switch ATS providers, rebrand career pages, or change their token slug over time. 

Token format:
  Greenhouse: https://boards-api.greenhouse.io/v1/boards/{token}/jobs
  Lever:      https://api.lever.co/v0/postings/{token}?mode=json

For people using this dataset: 
- To find a company's token: visit their careers page, verify they are using Greenhouse/Lever.
- Look at the URL - boards.greenhouse.io/{token} or jobs.lever.co/{token}.
- And edit this list with the companies you wish to add.
"""
GREENHOUSE_CANDIDATES = [
    "stripe", "airbnb", "coinbase", "robinhood", "doordash", "pinterest",
    "reddit", "discord", "figma", "notion", "asana", "dropbox", "gitlab",
    "elastic", "datadog", "twilio", "hashicorp", "databricks", "snowflake",
    "confluent", "mongodb", "cloudflare", "okta", "segment", "affirm",
    "plaid", "brex", "instacart", "squarespace", "peloton", "warbyparker",
    "etsy", "lyft", "pagerduty", "gusto", "flexport", "openai", "turing",
    "samsara", "webflow", "grammarly", "canva", "airtable", "vercel",
    "retool", "scaleai", "anduril", "benchling", "ramp", "deel", "algolia",
    "betterment", "calendly", "seatgeek", "sendbird", "salesloft", "sofi",
    "tailscale", "taskrabbit", "thumbtack", "toast", "twitch", "udemy",
    "wikimedia", "ziprecruiter", "relativity", "ripple", "anthropic",
    "faire", "1password", "armory", "axon", "bitwarden", "modal", "hex",
    "blockdaemon", "cerebras", "chainguard", "chronosphere", "warp",
    "circleci", "code42", "cohere", "cribl", "dailypay", "deepgram",
    "dremio", "flywire", "formlabs", "groq", "hightouch", "replit",
    "immuta", "karat", "labelbox", "launchdarkly", "mux", "clay",
    "neondatabase", "newfront", "newsela", "nexhealth", "oyster",
    "personio", "planet", "ponder", "pulumi", "linear", "perplexity",
    "shippo", "sigstore", "skydio", "snyk", "starburst", "stytch",
    "supabase", "temporal", "triplelift", "udacity", "unity",
    "whatnot", "workato", "zapier", "clickhouse", "dbtlabs",
]

LEVER_CANDIDATES = [
    "netflix", "palantir", "eventbrite", "yelp", "sourcegraph", "postman",
    "netlify", "attentive", "ro", "carta", "clever", "kraken", "ironclad",
    "checkr", "lattice", "nuro", "loom", "amplitude", "weaviate", "wefox",
    "branch", "chime", "fivetran", "handshake", "imgur", "apolloio",
    "kickstarter", "mixpanel", "opendoor", "patreon", "quora", "spotify",
    "gopuff", "swordhealth", "aiven", "alltrails", "benchsci", "bugsnag",
    "clearco", "codecov", "convertkit", "doximity", "exabeam", "hackerone",
    "healthverity", "influxdata", "kong", "mural", "outreach",
    "pilot", "productboard", "redis", "semrush", "shipbob", "soloio",
]

ALL_COMPANIES = (
    [{"name": c, "ats": "greenhouse"} for c in GREENHOUSE_CANDIDATES]
    + [{"name": c, "ats": "lever"} for c in LEVER_CANDIDATES]
)

if __name__ == "__main__":
    print(f"Total candidate companies: {len(ALL_COMPANIES)}")
    print(f"  Greenhouse: {len(GREENHOUSE_CANDIDATES)}")
    print(f"  Lever: {len(LEVER_CANDIDATES)}")
