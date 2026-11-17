from pathlib import Path
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from legacy_etl.legacy_etl import run_legacy_etl
from ai_assistant.migration_agent import explain_migration

app = FastAPI(title="Banking ETL Migration API", version="1.0.0")

class ExplainRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "healthy", "service": "banking-api"}

@app.get("/summary")
def summary():
    data_dir = Path(os.getenv("DATA_DIR", Path(__file__).resolve().parents[1] / "data"))
    result_file = data_dir / "summary" / "daily_summary.csv"
    if not result_file.exists():
        return {"message": "No summary yet. Run POST /etl/run first."}
    import pandas as pd
    return {"records": pd.read_csv(result_file).to_dict(orient="records")}

@app.post("/etl/run")
def run_etl():
    try:
        return run_legacy_etl()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"ETL failed: {type(exc).__name__}")

@app.post("/ai/explain")
def ai_explain(request: ExplainRequest):
    return {"explanation": explain_migration(request.question)}
