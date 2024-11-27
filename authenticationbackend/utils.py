from typing import Dict, List


def validate_incoming_data(
    data: Dict[str, any],
    required_keys: List[str],
    allowed_keys: List[str] = [],
    partial: bool = False,
) -> List[Dict[str, str]]:

    errors: List[Dict[str, str]] = []

    if not partial:
        for key in required_keys:
            if key not in data:
                errors.append({key: "This is a required key."})

    for key in data:
        if key not in required_keys + allowed_keys:
            errors.append({"unexpected_key": key})

    return errors
