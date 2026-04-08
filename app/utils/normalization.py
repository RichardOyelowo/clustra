def normalize_payloads(data):
    """ this coverts dicts values to lowercase"""
    if isinstance(data, dict):
        return {k: normalize_payloads(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_payloads(item) for item in data]
    elif isinstance(data, str):
        return data.lower()
    else:
        return data  # explicitly leave ints, bools,  etc.
