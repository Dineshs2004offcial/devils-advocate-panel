import pytest
from app.tools.calculator import calculate_runway, calculate_ltv_cac_ratio
from app.tools.financial import benchmark_unit_economics
from app.tools.scraper import scrape_pitch_url
from app.utils.helpers import clean_json_response, sanitize_filename
from app.utils.validators import validate_pitch_payload


def test_calculator_tools():
    # Runway calculations
    assert calculate_runway(100000.0, 20000.0) == 5.0
    assert calculate_runway(50000.0, 0.0) == 999.0

    # LTV / CAC calculations
    assert calculate_ltv_cac_ratio(3000.0, 1000.0) == 3.0
    assert calculate_ltv_cac_ratio(1500.0, 0.0) == 0.0


def test_financial_benchmarking():
    healthy = benchmark_unit_economics(cac=1000.0, ltv=4000.0, gross_margin_pct=80.0)
    assert healthy["status"] == "HEALTHY"
    assert healthy["adjusted_ltv_cac"] == 3.2

    critical = benchmark_unit_economics(cac=2000.0, ltv=1000.0, gross_margin_pct=70.0)
    assert critical["status"] == "CRITICAL"


def test_clean_json_helper():
    raw_markdown = "```json\n{\"score\": 85, \"verdict\": \"INVEST\"}\n```"
    cleaned = clean_json_response(raw_markdown, fallback={})
    assert isinstance(cleaned, dict)
    assert cleaned.get("score") == 85
    assert cleaned.get("verdict") == "INVEST"

    invalid_raw = "Not json content"
    fallback_dict = {"fallback": True}
    res = clean_json_response(invalid_raw, fallback=fallback_dict)
    assert res == fallback_dict


def test_sanitize_filename():
    assert sanitize_filename("HealthSync AI: Radiologist Co-Pilot") == "HealthSync_AI__Radiologist_Co_Pilot"
    assert sanitize_filename("Safe-Name 123") == "Safe_Name_123"


def test_validate_pitch_payload():
    valid = {
        "startup_name": "TestCo",
        "problem": "High cost",
        "solution": "Cheap software"
    }
    assert len(validate_pitch_payload(valid)) == 0

    invalid = {
        "startup_name": "",
        "problem": "",
        "solution": ""
    }
    errors = validate_pitch_payload(invalid)
    assert len(errors) == 3
