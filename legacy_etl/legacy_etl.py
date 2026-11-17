from pathlib import Path
import os
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("DATA_DIR", ROOT / "data"))
INPUT = DATA_DIR / "raw" / "transactions.csv"

def run_legacy_etl(input_path: Path = INPUT, output_dir: Path | None = None) -> dict:
    output_dir = output_dir or DATA_DIR
    processed_dir = output_dir / "processed"
    excluded_dir = output_dir / "excluded"
    summary_dir = output_dir / "summary"
    for folder in (processed_dir, excluded_dir, summary_dir):
        folder.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    valid = df[
        df["transaction_id"].notna()
        & df["customer_id"].notna()
        & df["amount"].notna()
        & (df["amount"] > 0)
        & (df["status"].str.upper() == "SUCCESS")
    ].copy()
    excluded = df.drop(valid.index).copy()
    valid["transaction_date"] = pd.to_datetime(valid["transaction_date"]).dt.strftime("%Y-%m-%d")
    summary = (
        valid.groupby(["transaction_date", "currency"], as_index=False)
        .agg(transaction_count=("transaction_id", "count"), total_amount=("amount", "sum"))
    )
    valid.to_csv(processed_dir / "clean_transactions.csv", index=False)
    excluded.to_csv(excluded_dir / "excluded_transactions.csv", index=False)
    summary.to_csv(summary_dir / "daily_summary.csv", index=False)
    return {"input_count": len(df), "processed_count": len(valid), "excluded_count": len(excluded)}

if __name__ == "__main__":
    print(run_legacy_etl())
