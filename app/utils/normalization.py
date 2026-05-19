from typing import Any

def normalize_payloads(data: dict[str, Any]) -> dict[str, Any]:
    """Converts string values in nested dicts/lists to lowercase."""
    return {
        key: _normalize_value(value)
        for key, value in data.items()
    }

def _normalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(k): _normalize_value(v)
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    if isinstance(value, str):
        return value.lower()
    return value
