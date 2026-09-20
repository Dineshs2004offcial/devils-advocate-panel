from typing import Dict, Any


def benchmark_unit_economics(cac: float, ltv: float, gross_margin_pct: float) -> Dict[str, Any]:
    """Benchmark unit economics against venture standards."""
    ratio = (ltv * (gross_margin_pct / 100.0)) / cac if cac > 0 else 0.0
    status = "HEALTHY" if ratio >= 3.0 else ("WARNING" if ratio >= 1.5 else "CRITICAL")
    return {
        "cac": cac,
        "ltv": ltv,
        "gross_margin_pct": gross_margin_pct,
        "adjusted_ltv_cac": round(ratio, 2),
        "status": status,
        "recommendation": "Maintain expansion" if status == "HEALTHY" else "Optimize customer acquisition and onboarding"
    }
