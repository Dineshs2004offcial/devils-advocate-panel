from app.tools.calculator import calculate_runway, calculate_ltv_cac_ratio
from app.tools.financial import benchmark_unit_economics

print("Runway:", calculate_runway(250000.0, 25000.0), "months")
print("LTV/CAC:", calculate_ltv_cac_ratio(5000.0, 1200.0))
print("Benchmark:", benchmark_unit_economics(1200.0, 5000.0, 85.0))
