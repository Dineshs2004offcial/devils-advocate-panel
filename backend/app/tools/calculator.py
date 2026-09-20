import math
from typing import Union


def calculate_runway(cash_balance: float, monthly_burn: float) -> float:
    """Calculate startup runway in months."""
    if monthly_burn <= 0:
        return 999.0
    return round(cash_balance / monthly_burn, 1)


def calculate_ltv_cac_ratio(ltv: float, cac: float) -> float:
    """Calculate LTV/CAC ratio."""
    if cac <= 0:
        return 0.0
    return round(ltv / cac, 2)
