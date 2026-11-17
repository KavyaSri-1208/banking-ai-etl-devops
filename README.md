# Banking AI ETL Migration & DevOps Automation

A portfolio-ready, synthetic-data project demonstrating migration of a legacy Python banking ETL to PySpark, reconciliation, automated tests, an AI-assisted migration explainer, FastAPI, Streamlit, Docker, Jenkins, SonarQube, AWS ECR/S3, Terraform and Kubernetes managed by KOPS.

> **Important:** This is a learning/demo system. It contains synthetic data only. It is not production banking software and must not be connected to real customer data or production banking systems.

## Architecture

- **EC2 Server 1 – DevOps Master:** Jenkins, Git, Docker/Compose, SonarQube, Terraform, KOPS and kubectl.
- **KOPS control plane:** Kubernetes API/control components.
- **KOPS worker 1:** ETL/API workloads.
- **KOPS worker 2:** Streamlit and other application workloads.
- **AWS ECR:** Docker image registry.
- **AWS S3:** raw and processed demo data / KOPS state store (use separate buckets).
- **Kubernetes namespaces:** `banking-dev`, `banking-uat`, `banking-prod`.

The namespace manifests provide logical environment separation only. A real production banking platform needs stronger isolation, HA control plane, security reviews, backups, monitoring and operational controls.

## Repository layout

```text
banking-ai-etl-devops/
├── ai_assistant/       # AI migration explanation helper (optional LLM)
├── backend/            # FastAPI API
├── data/               # Synthetic sample input and output folders
├── docker/             # API, ETL and frontend Dockerfiles
├── docs/               # Architecture and operating notes
├── environments/       # Environment-specific examples
├── frontend/           # Streamlit dashboard
├── jenkins/            # Jenkins pipeline
├── kubernetes/         # Namespaces, deployments, services and ETL Job
├── legacy_etl/         # Baseline Python ETL
├── monitoring/         # Prometheus configuration
├── pyspark_etl/        # PySpark migration
├── reconciliation/     # Legacy-vs-PySpark comparison
├── scripts/            # Local/container helper scripts
├── terraform/          # ECR/S3 starter infrastructure
└── tests/              # Pytest tests
```

## Run locally with Docker Compose

Prerequisites: Docker Engine and Docker Compose plugin.

```bash
cp .env.example .env
docker compose build
docker compose up -d api frontend
```

- API health: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Streamlit: http://localhost:8501

Run ETL in a one-off container:

```bash
docker compose run --rm etl
```

Outputs are written under `data/processed/`, `data/excluded/` and `data/summary/`.

## Run tests locally

Python 3.11 is recommended.

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
pytest -q
python -m legacy_etl.legacy_etl
python -m pyspark_etl.main
python -m reconciliation.compare_results
```

The sample CSV is synthetic. The tests verify filtering, totals and reconciliation.

## Environment variables

Copy `.env.example` to `.env`. Do not commit `.env`.

- `DATA_DIR`: data directory inside the container (default `/app/data`).
- `OPENAI_API_KEY`: optional. If omitted, the AI helper returns a safe local explanation instead of calling an LLM.
- `OPENAI_MODEL`: optional model name.
- `AWS_REGION`, `AWS_ACCOUNT_ID`, `ECR_REPOSITORY`: Jenkins deployment parameters.

## Jenkins pipeline

Configure these Jenkins credentials / settings before running the pipeline:

1. GitHub repository credential or configure the EC2 instance's Git SSH key.
2. AWS IAM role attached to the Jenkins EC2 instance (preferred) with least-privilege ECR push and deployment permissions.
3. Jenkins tools/plugins: Pipeline, Git, SonarQube Scanner, Credentials Binding, Pipeline: AWS Steps (optional).
4. SonarQube server named `sonarqube` in Jenkins global configuration.
5. Configure `AWS_REGION`, `AWS_ACCOUNT_ID`, `ECR_REPOSITORY`, `KOPS_CLUSTER_NAME` and `KOPS_STATE_STORE` as Jenkins environment variables.
6. Configure cluster access for the Jenkins service account/user. Do not store long-lived AWS keys in the Jenkinsfile.

The Nexus stage is intentionally commented out as a future placeholder. Nexus is not installed or used. Docker images are pushed to AWS ECR.

The pipeline includes manual approval gates before UAT and PROD. The PROD namespace in this demo is not a real production environment.

## Kubernetes / KOPS

Update the image placeholders in `kubernetes/` or use Jenkins image substitution. Apply namespaces first, then application manifests:

```bash
kubectl apply -f kubernetes/namespaces/
kubectl apply -f kubernetes/api/
kubectl apply -f kubernetes/frontend/
kubectl apply -f kubernetes/etl/
```

The ETL manifest is a Job template. Review resource requests, limits, storage and image paths before applying.

`kops/cluster-config.yaml` is an example configuration reference, not a command-ready cluster definition. KOPS cluster creation requires a unique cluster name, S3 state store, IAM permissions, DNS setup, subnet design and cost review. Never run `kops update cluster --yes` until the generated plan has been reviewed.

## Terraform

The Terraform starter creates an ECR repository and S3 bucket. It deliberately does not create a VPC, public IPs, NAT Gateway or KOPS cluster automatically. Add reviewed networking and IAM modules after confirming AWS Free Tier/credit eligibility and costs.

```bash
cd terraform
terraform init
terraform fmt -check
terraform validate
```

Do not commit Terraform state, plan files or credentials.

## Security checklist

- Use synthetic data only.
- Keep `.env`, credentials, private keys and Terraform state out of Git.
- Prefer EC2 instance profiles / IAM roles over static AWS keys.
- Restrict SSH and admin ports to your own IP / VPN.
- Do not expose Jenkins, SonarQube, Kubernetes API or database/admin ports publicly.
- Use Kubernetes Secrets or AWS Secrets Manager/SSM for runtime secrets.
- Review IAM, security groups, ECR policies and Kubernetes RBAC before deployment.
