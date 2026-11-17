from pathlib import Path
import pandas as pd
from legacy_etl.legacy_etl import run_legacy_etl

def test_legacy_etl_counts(tmp_path):
    source = tmp_path / "transactions.csv"
    pd.DataFrame([
        ["T1", "C1", "2026-11-01", "CREDIT", 100, "INR", "SUCCESS"],
        ["T2", "C2", "2026-11-01", "DEBIT", 50, "INR", "FAILED"],
        ["T3", "C3", "2026-11-02", "CREDIT", -5, "INR", "SUCCESS"],
    ], columns=["transaction_id","customer_id","transaction_date","transaction_type","amount","currency","status"]).to_csv(source, index=False)
    result = run_legacy_etl(source, tmp_path / "out")
    assert result == {"input_count": 3, "processed_count": 1, "excluded_count": 2}
    clean = pd.read_csv(tmp_path / "out" / "processed" / "clean_transactions.csv")
    assert clean.iloc[0]["transaction_id"] == "T1"
