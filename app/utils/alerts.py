from typing import Dict, List

def check_thresholds(costs: Dict[str, float], thresholds: Dict[str, float]) -> List[str]:
    alerts = []
    for provider, cost in costs.items():
        th = thresholds.get(provider)
        if th is not None and cost > th:
            alerts.append(f"{provider.upper()} monthly cost ${cost:,.2f} exceeds threshold ${th:,.2f}")
    return alerts