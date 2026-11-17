import os
from ai_assistant.prompts import SYSTEM_PROMPT

def explain_migration(question: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "Local demo response: compare the legacy and PySpark implementations for "
            "input schema, null handling, numeric casting, business filters, date "
            "normalization, grouping and totals. Run pytest and reconciliation before "
            "accepting any migration. Configure OPENAI_API_KEY securely to enable an LLM."
        )
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question[:6000]},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or "No explanation returned."
    except Exception as exc:
        return f"AI service unavailable; use local review and tests. Details: {type(exc).__name__}"
