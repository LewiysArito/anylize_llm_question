import os
from llm_query.helpers import convert_env_value_to_bool

class ConfigError(Exception):
    pass

def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = os.environ.get("API_PORT", 80)
    
    value = os.environ.get("API_SECURE", False)
    try:
        secure = convert_env_value_to_bool(value)
    except Exception as e:  
        raise ConfigError(str(e))
    
    return f"{"https" if secure else "http"}://{host}:{port}"

def get_kafka_url():
    host = os.environ.get("KAFKA_HOST", "localhost")
    port = os.environ.get("KAFKA_PORT",  9092)
    value = os.environ.get("KAFKA_SECURE", False)
    
    try:
        secure = convert_env_value_to_bool(value)
    except Exception as e:  
        raise ConfigError(str(e))
    
    return f"{"https" if secure else "http"}://{host}:{port}" 

def get_llm_url_and_max_token():
    host = os.environ.get("LLAMA_HOST", "localshost")
    port = os.environ.get("LLAMA_PORT", 11434)
    max_tokens = os.environ.get("LLM_MAX_TOKENS", 1000)

    value = os.environ.get("LLM_SECURE", False)
    try:
        secure = convert_env_value_to_bool(value)
    except Exception as e:  
        raise ConfigError(str(e))

    base_url = f"{"https" if secure else "http"}://{host}:{port}"
    return dict(base_url=base_url, max_tokens=max_tokens)