import pytest
pyspark = pytest.importorskip("pyspark")
from pyspark_etl.extract import create_spark
from pyspark_etl.transform import transform_transactions

def test_pyspark_filter_and_summary():
    spark = create_spark("pytest")
    try:
        rows = [
            ("T1", "C1", "2026-11-01", "CREDIT", "100", "INR", "SUCCESS"),
            ("T2", "C2", "2026-11-01", "DEBIT", "50", "INR", "FAILED"),
        ]
        cols = ["transaction_id","customer_id","transaction_date","transaction_type","amount","currency","status"]
        df = spark.createDataFrame(rows, cols)
        clean, excluded, summary = transform_transactions(df)
        assert clean.count() == 1
        assert excluded.count() == 1
        assert summary.collect()[0]["transaction_count"] == 1
    finally:
        spark.stop()
