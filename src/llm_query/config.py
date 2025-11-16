import logging
import os

from dotenv import load_dotenv
from llm_query.helpers import convert_env_value_to_bool

load_dotenv()

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
    
    return f"{host}:{port}" 

def get_llm_url_and_max_token():
    host = os.environ.get("LLAMA_HOST", "localhost")
    port = os.environ.get("LLAMA_PORT", 11434)
    max_tokens = int(os.environ.get("LLM_MAX_TOKENS", 1000))

    value = os.environ.get("LLM_SECURE", False)
    try:
        secure = convert_env_value_to_bool(value)
    except Exception as e:  
        raise ConfigError(str(e))

    base_url = f"{"https" if secure else "http"}://{host}:{port}"
    return dict(base_url=base_url, max_tokens=max_tokens)

def get_logger()->logging.Logger:
    
    def off_loggers() -> None: 
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING) 
        logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    LOG_LEVEL_NAME = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, LOG_LEVEL_NAME, logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('./llm_query.log', encoding='utf-8')
        ]
    )

    off_loggers()
    logger = logging.getLogger(__name__)
    
    logger.info(f"Logger initialized with level: {LOG_LEVEL_NAME}")
    return logger

logger = get_logger()