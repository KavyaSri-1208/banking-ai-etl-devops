from pathlib import Path
from pyspark.sql import SparkSession

def create_spark(app_name: str = "BankingETLMigration") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

def extract_transactions(spark: SparkSession, input_path: str | Path):
    return spark.read.option("header", True).option("inferSchema", True).csv(str(input_path))
