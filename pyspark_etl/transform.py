from pyspark.sql import functions as F

def transform_transactions(df):
    typed = df.withColumn("amount", F.col("amount").cast("double"))
    valid_condition = (
        F.col("transaction_id").isNotNull()
        & F.col("customer_id").isNotNull()
        & F.col("amount").isNotNull()
        & (F.col("amount") > 0)
        & (F.upper(F.col("status")) == "SUCCESS")
    )
    clean = (
        typed.filter(valid_condition)
        .withColumn("transaction_date", F.to_date("transaction_date"))
    )
    excluded = typed.filter(~valid_condition)
    summary = (
        clean.groupBy("transaction_date", "currency")
        .agg(
            F.count("transaction_id").alias("transaction_count"),
            F.round(F.sum("amount"), 2).alias("total_amount"),
        )
    )
    return clean, excluded, summary
