# Demo runbook

1. Confirm synthetic input exists at `data/raw/transactions.csv`.
2. Install requirements and run `pytest -q`.
3. Run legacy ETL: `python -m legacy_etl.legacy_etl`.
4. Run PySpark ETL: `python -m pyspark_etl.main`.
5. Reconcile: `python -m reconciliation.compare_results`.
6. Start API and dashboard with Docker Compose.
7. Build/push images to ECR through Jenkins.
8. Deploy reviewed manifests to DEV, then UAT and demo PROD after approval.

If PySpark fails, verify Java is installed and `JAVA_HOME` is configured. The ETL container installs a headless JRE.
