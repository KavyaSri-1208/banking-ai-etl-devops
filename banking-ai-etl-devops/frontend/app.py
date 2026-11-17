import os
import requests
import streamlit as st

st.set_page_config(page_title="Banking ETL Migration", page_icon="🏦", layout="wide")
st.title("🏦 Banking AI ETL Migration Dashboard")
st.caption("Synthetic-data demonstration — not for real banking data.")

api = os.getenv("API_BASE_URL", "http://localhost:8000")

col1, col2 = st.columns(2)
with col1:
    if st.button("Run legacy ETL", type="primary"):
        try:
            response = requests.post(f"{api}/etl/run", timeout=120)
            response.raise_for_status()
            st.success("ETL completed")
            st.json(response.json())
        except requests.RequestException as exc:
            st.error(f"API request failed: {exc}")

with col2:
    if st.button("Refresh summary"):
        try:
            response = requests.get(f"{api}/summary", timeout=30)
            response.raise_for_status()
            st.json(response.json())
        except requests.RequestException as exc:
            st.error(f"API request failed: {exc}")

st.subheader("AI-assisted migration explanation")
question = st.text_area("Ask about the migration", "Explain how the legacy ETL filtering maps to the PySpark transformation.")
if st.button("Explain"):
    try:
        response = requests.post(f"{api}/ai/explain", json={"question": question}, timeout=60)
        response.raise_for_status()
        st.write(response.json()["explanation"])
    except requests.RequestException as exc:
        st.error(f"AI request failed: {exc}")
