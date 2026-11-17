from pathlib import Path

def write_csv(df, output_path: str | Path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Spark writes a directory containing part-*.csv; this is intentional for scale.
    df.coalesce(1).write.mode("overwrite").option("header", True).csv(str(path))
