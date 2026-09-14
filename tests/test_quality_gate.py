from dd_engine.quality_gate import evaluate_quality_gate


def base():
    return {
        "ticker": "ITUB4",
        "company_name": "Banco Itaú",
        "last_data_quality_status": "READY",
        "latest_metrics": {"close": 30, "lpa": 3, "vpa": 20, "dpa": 1.5},
    }


def test_approved_when_core_inputs_are_valid():
    r = evaluate_quality_gate(base())
    assert r.status == "APPROVED"
    assert r.ranking_eligible is True


def test_review_when_vpa_missing():
    c = base(); c["latest_metrics"]["vpa"] = None
    r = evaluate_quality_gate(c)
    assert r.status == "REVIEW"
    assert r.ranking_eligible is False
    assert "VPA_MISSING" in r.warnings


def test_blocked_when_quote_missing():
    c = base(); c["latest_metrics"]["close"] = None
    r = evaluate_quality_gate(c)
    assert r.status == "BLOCKED"
    assert r.ranking_eligible is False
    assert "QUOTE_MISSING" in r.critical_flags
