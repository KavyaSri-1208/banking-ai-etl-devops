from pathlib import Path
import os
from pyspark_etl.extract import create_spark, extract_transactions
from pyspark_etl.transform import transform_transactions
from pyspark_etl.load import write_csv

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("DATA_DIR", ROOT / "data"))

def main():
    spark = create_spark()
    try:
        source = DATA_DIR / "raw" / "transactions.csv"
        df = extract_transactions(spark, source)
        clean, excluded, summary = transform_transactions(df)
        write_csv(clean, DATA_DIR / "pyspark_output" / "processed")
        write_csv(excluded, DATA_DIR / "pyspark_output" / "excluded")
        write_csv(summary, DATA_DIR / "pyspark_output" / "summary")
        print({
            "input_count": df.count(),
            "processed_count": clean.count(),
            "excluded_count": excluded.count(),
        })
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
