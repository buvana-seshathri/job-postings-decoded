"""
Phase 3: Parse & Clean
------------------------
Reads raw JSON files from data/raw/, normalizes fields across the two different API schemas (Greenhouse vs Lever).
Extracts structured signal from free-text job descriptions:
  - disclosed salary range (regex on common pay-transparency patterns)
  - skill mentions (keyword match against a curated skill list)
  - seniority level (inferred from title)

Usage: python scripts/parse_and_clean.py
"""

import json
import re
from pathlib import Path
from html import unescape

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
OUT_PATH = Path(__file__).parent.parent / "data" / "processed" / "postings_raw_parsed.json"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# skills list can be expanded as needed
SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go",
    "golang", "rust", "kotlin", "scala", "swift", "objective-c", "php",
    "ruby", "perl", "r", "matlab", "bash", "shell", "powershell",
    "html", "css", "sql", "nosql",

    # Frontend
    "react", "react.js", "next.js", "angular", "vue", "vue.js", "svelte",
    "redux", "tailwind", "bootstrap", "material ui", "mui",
    "webpack", "vite", "jquery",

    # Backend
    "node", "node.js", "express", "nestjs", "spring", "spring boot",
    "django", "flask", "fastapi", "laravel", "asp.net", ".net",
    "gin", "fiber", "hibernate", "graphql", "rest", "rest api",
    "grpc", "microservices",

    # Databases
    "mysql", "postgresql", "postgres", "sqlite", "mongodb", "redis",
    "cassandra", "dynamodb", "oracle", "mssql", "sql server",
    "cockroachdb", "elasticsearch", "opensearch", "firebase",

    # Cloud
    "aws", "amazon web services", "gcp", "google cloud", "azure",
    "cloudformation", "terraform", "pulumi",

    # Containers & Orchestration
    "docker", "kubernetes", "helm", "istio", "openshift",
    "containerd", "podman",

    # DevOps / CI-CD
    "git", "github", "gitlab", "bitbucket",
    "github actions", "gitlab ci", "jenkins", "circleci",
    "travis ci", "azure devops", "argo cd",
    "ci/cd", "devops",

    # Linux / Systems
    "linux", "unix", "ubuntu", "redhat", "centos",
    "systemd", "networking", "tcp/ip", "dns", "http", "https",
    "ssl", "tls", "nginx", "apache", "load balancing",
    "distributed systems", "operating systems", "multithreading",
    "concurrency", "parallel programming",

    # Message Queues / Streaming
    "kafka", "rabbitmq", "activemq", "sqs", "sns",
    "pub/sub", "pulsar", "eventbridge",

    # Data Engineering
    "spark", "pyspark", "hadoop", "hive", "airflow",
    "dbt", "snowflake", "databricks", "etl", "elt",
    "bigquery", "redshift", "data lake", "lakehouse",

    # AI / Machine Learning
    "machine learning", "deep learning", "artificial intelligence",
    "computer vision", "nlp", "generative ai", "llm",
    "transformers", "rag", "fine tuning", "prompt engineering",
    "langchain", "llamaindex", "hugging face",
    "tensorflow", "keras", "pytorch", "xgboost",
    "lightgbm", "scikit-learn", "sklearn",
    "numpy", "pandas", "opencv", "onnx",

    # MLOps
    "mlflow", "kubeflow", "sagemaker", "vertex ai",
    "azure ml", "weights & biases", "wandb",
    "feature store", "model serving", "triton",
    "ray", "vllm",

    # APIs
    "rest api", "graphql", "grpc", "openapi", "swagger",
    "postman", "soap",

    # Testing
    "pytest", "junit", "mockito", "jest", "mocha",
    "cypress", "playwright", "selenium", "testing",

    # Monitoring / Observability
    "prometheus", "grafana", "datadog", "new relic",
    "splunk", "elk", "elastic stack", "kibana",
    "cloudwatch", "opentelemetry",

    # Security
    "oauth", "oauth2", "openid", "jwt", "iam",
    "authentication", "authorization", "cybersecurity",
    "encryption", "cryptography", "secrets management",
    "vault",

    # Mobile
    "android", "ios", "react native", "flutter",
    "xamarin",

    # Embedded / Low Level
    "embedded", "firmware", "arm", "fpga",
    "cuda", "opencl", "mpi", "openmp",

    # HPC
    "slurm", "high performance computing", "hpc",
    "parallel computing", "distributed computing",

    # Architecture
    "design patterns", "system design",
    "object-oriented programming", "oop",
    "functional programming",

    # Agile
    "agile", "scrum", "kanban", "jira", "confluence",

    # Version Control
    "git", "github", "gitlab",

    # UI/UX
    "figma", "adobe xd",

    # CRM / Enterprise
    "salesforce", "sap", "servicenow",

    # Miscellaneous
    "json", "xml", "yaml", "protobuf",
    "oauth", "jwt", "websocket", "grpc",
    "api gateway", "reverse proxy",
]

SALARY_PATTERN = re.compile(
    r"\$([\d,]{2,7})(?:\.\d{2})?\s*[-–—to]{1,4}\s*\$?([\d,]{2,7})(?:\.\d{2})?\s*(?:per year|/year|/yr|annually|usd)?",
    re.IGNORECASE,
)

SENIORITY_KEYWORDS = {
    "intern": "intern",
    "junior": "junior",
    "entry": "junior",
    "associate": "junior",
    "ii": "mid",
    "senior": "senior",
    "sr.": "senior",
    "sr ": "senior",
    "staff": "senior",
    "principal": "lead",
    "lead": "lead",
    "director": "director",
    "vp": "executive",
    "head of": "executive",
}


def strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return unescape(re.sub(r"\s+", " ", text)).strip()


def extract_salary(text: str):
    match = SALARY_PATTERN.search(text)
    if not match:
        return None, None
    low = int(match.group(1).replace(",", ""))
    high = int(match.group(2).replace(",", ""))
    # sanity check - filter out obviously wrong matches (e.g. phone numbers)
    if low < 15000 or high > 2000000 or low > high:
        return None, None
    return low, high


def extract_skills(text: str):
    text_lower = text.lower()
    return [s for s in SKILLS if s in text_lower]


def infer_seniority(title: str):
    title_lower = title.lower()
    for kw, level in SENIORITY_KEYWORDS.items():
        if kw in title_lower:
            return level
    return "unspecified"


def parse_greenhouse(company: str, jobs: list):
    records = []
    for job in jobs:
        title = job.get("title", "")
        content = strip_html(job.get("content", ""))
        location = (job.get("location") or {}).get("name", "")
        departments = [d.get("name", "") for d in job.get("departments", [])]

        salary_low, salary_high = extract_salary(content)

        records.append({
            "company": company,
            "ats": "greenhouse",
            "title": title,
            "location": location,
            "department": departments[0] if departments else "",
            "seniority": infer_seniority(title),
            "salary_low": salary_low,
            "salary_high": salary_high,
            "skills": extract_skills(content),
            "posted_date": job.get("updated_at", ""),
            "description_length": len(content),
        })
    return records


def parse_lever(company: str, jobs: list):
    records = []
    for job in jobs:
        title = job.get("text", "")
        desc_parts = [
            job.get("descriptionPlain", ""),
            " ".join(l.get("plainText", "") for l in job.get("lists", []) if l.get("plainText")),
        ]
        content = strip_html(" ".join(p for p in desc_parts if p))
        categories = job.get("categories", {})

        salary_low, salary_high = extract_salary(content)

        records.append({
            "company": company,
            "ats": "lever",
            "title": title,
            "location": categories.get("location", ""),
            "department": categories.get("team", ""),
            "seniority": infer_seniority(title),
            "salary_low": salary_low,
            "salary_high": salary_high,
            "skills": extract_skills(content),
            "posted_date": job.get("createdAt", ""),
            "description_length": len(content),
        })
    return records


def main():
    all_records = []
    raw_files = sorted(RAW_DIR.glob("*.json"))

    if not raw_files:
        print(f"No raw files found in {RAW_DIR}. Run collect_postings.py first.")
        return

    for path in raw_files:
        ats, company = path.stem.split("_", 1)
        with open(path) as f:
            jobs = json.load(f)

        if ats == "greenhouse":
            all_records.extend(parse_greenhouse(company, jobs))
        else:
            all_records.extend(parse_lever(company, jobs))

    with open(OUT_PATH, "w") as f:
        json.dump(all_records, f, indent=2)

    with_salary = sum(1 for r in all_records if r["salary_low"] is not None)
    print(f"Parsed {len(all_records)} postings from {len(raw_files)} companies.")
    print(f"  {with_salary} postings ({with_salary/len(all_records)*100:.1f}%) have disclosed salary.")
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
