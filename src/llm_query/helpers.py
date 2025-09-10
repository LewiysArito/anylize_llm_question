def convert_env_value_to_bool(value: str | bool):
    if not isinstance(value, bool) and not value.lower() in ["false", "true", "0", "1"]:
        raise Exception("value should be boolean or find inf list ['false', 'true', '0', '1'")
    
    return value if isinstance(value, bool) else (True if value in ["true", "1"] else False)