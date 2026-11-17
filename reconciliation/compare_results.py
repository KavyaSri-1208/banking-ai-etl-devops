from pathlib import Path
import pandas as pd
import os

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("DATA_DIR", ROOT / "data"))

def reconcile(legacy_path=None, spark_path=None) -> dict:
    legacy_path = Path(legacy_path or DATA_DIR / "processed" / "clean_transactions.csv")
    spark_path = Path(spark_path or DATA_DIR / "pyspark_output" / "processed")
    spark_files = list(spark_path.glob("part-*.csv"))
    if not legacy_path.exists() or not spark_files:
        raise FileNotFoundError("Run both legacy ETL and PySpark ETL before reconciliation.")
    left = pd.read_csv(legacy_path).sort_values("transaction_id").reset_index(drop=True)
    right = pd.read_csv(spark_files[0]).sort_values("transaction_id").reset_index(drop=True)
    # Normalize date / numeric representations before comparing.
    left["transaction_date"] = pd.to_datetime(left["transaction_date"]).dt.strftime("%Y-%m-%d")
    right["transaction_date"] = pd.to_datetime(right["transaction_date"]).dt.strftime("%Y-%m-%d")
    left["amount"] = left["amount"].astype(float)
    right["amount"] = right["amount"].astype(float)
    same = left.equals(right)
    result = {
        "legacy_rows": len(left),
        "pyspark_rows": len(right),
        "row_counts_match": len(left) == len(right),
        "records_match": same,
        "legacy_total": round(float(left["amount"].sum()), 2),
        "pyspark_total": round(float(right["amount"].sum()), 2),
    }
    result["reconciliation_passed"] = (
        result["row_counts_match"]
        and result["records_match"]
        and result["legacy_total"] == result["pyspark_total"]
    )
    out = DATA_DIR / "reconciliation"
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([result]).to_csv(out / "reconciliation_result.csv", index=False)
    return result

if __name__ == "__main__":
    print(reconcile())
