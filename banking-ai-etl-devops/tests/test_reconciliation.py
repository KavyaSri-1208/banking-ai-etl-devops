from reconciliation.compare_results import reconcile

def test_reconciliation_requires_outputs(tmp_path):
    try:
        reconcile(tmp_path / "missing.csv", tmp_path / "missing_dir")
    except FileNotFoundError:
        assert True
    else:
        assert False, "Expected missing output error"
