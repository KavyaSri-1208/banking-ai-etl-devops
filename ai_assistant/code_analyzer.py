from pathlib import Path

def analyze_python_file(path: str) -> str:
    source = Path(path).read_text(encoding="utf-8")
    lines = len(source.splitlines())
    imports = [line.strip() for line in source.splitlines() if line.strip().startswith(("import ", "from "))]
    return (
        f"Local analysis: {Path(path).name} has {lines} lines and "
        f"{len(imports)} import statements. Review file I/O, data types, null handling, "
        "filter conditions, aggregations and output schema before migration."
    )
