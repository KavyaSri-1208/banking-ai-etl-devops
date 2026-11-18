
import os
import sys
import shutil
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_end_to_end_etl_reconciliation(tmp_path):
    # Prepare isolated test data
    source = ROOT / "data" / "raw" / "transactions.csv"
    assert source.exists(), "Source transactions.csv is missing"

    data_dir = tmp_path / "data"
    raw_dir = data_dir / "raw"
    raw_dir.mkdir(parents=True)

    shutil.copy2(source, raw_dir / "transactions.csv")

    # Configure Python and Spark environment
    env = os.environ.copy()
    env["DATA_DIR"] = str(data_dir)
    env["PYSPARK_PYTHON"] = sys.executable
    env["PYSPARK_DRIVER_PYTHON"] = sys.executable

    # Run the complete ETL workflow
    commands = [
        [sys.executable, "-m", "legacy_etl.legacy_etl"],
        [sys.executable, "-m", "pyspark_etl.main"],
        [sys.executable, "-m", "reconciliation.compare_results"],
    ]

    for command in commands:
        subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            check=True
        )

    # Validate reconciliation output
    result_file = data_dir / "reconciliation" / "reconciliation_result.csv"
    assert result_file.exists(), "Reconciliation result was not generated"

    result = pd.read_csv(result_file)

    assert len(result) == 1
    assert bool(result.loc[0, "reconciliation_passed"]), (
        f"ETL reconciliation failed: {result.to_dict(orient='records')}"
    )

    assert result.loc[0, "row_counts_match"]
    assert result.loc[0, "records_match"]

