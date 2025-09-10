# pylint: disable=too-few-public-methods
import abc
import aiohttp
import config
from llm_query import config

DEFAULT_BASE_URL = config.get_llm_config()["base_url"]
DEFAULT_MAX_TOKENS = config.get_llm_config()["max_tokens"]

class AbstractLLMQuery(abc.ABC):
    @abc.abstractmethod
    def generate_text(self, 
        model: str,
        prompt: str,
        temperature: float,
        stream: bool
    ):
        raise NotImplementedError
    
class LlamaQuery(AbstractLLMQuery):
    def __init__(self,base_url:str=DEFAULT_BASE_URL, max_tokens:float=DEFAULT_MAX_TOKENS):
        self.base_url = base_url
        self.client = aiohttp.ClientSession()

    def generate_text(self, model, prompt, temperature, stream):
        return super().generate_text(model, prompt, temperature, stream)