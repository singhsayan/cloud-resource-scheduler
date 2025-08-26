from typing import Dict, List
from uuid import uuid4

# In-memory store for demo. Swap with DB in utils/db.py if desired.
_RULES: Dict[str, dict] = {}

def save_rule(rule: dict) -> str:
    rid = rule.get("id") or str(uuid4())[:8]
    rule["id"] = rid
    _RULES[rid] = rule
    return rid

def list_rules() -> List[dict]:
    return list(_RULES.values())

def toggle_rule(rule_id: str) -> None:
    r = _RULES.get(rule_id)
    if r:
        r["enabled"] = not r.get("enabled", True)

def delete_rule(rule_id: str) -> None:
    _RULES.pop(rule_id, None)

def run_rule_now(rule_id: str) -> None:
    # Here you’d call AWS/Azure stop/start based on r['action'] & tag filters.
    # For demo, just a no-op.
    pass