# pylint: disable=too-few-public-methods
import abc
from typing import AsyncGenerator
from llm_query import config
from ollama import AsyncClient

DEFAULT_BASE_URL = config.get_llm_url_and_max_token()["base_url"]
DEFAULT_MAX_TOKENS = config.get_llm_url_and_max_token()["max_tokens"]

class LLMQueryError(Exception):
    pass

class AbstractLLMClient(abc.ABC):
    @abc.abstractmethod
    async def generate(self, 
        model: str,
        prompt: str,
        temperature: float = 0.7,
    )-> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def generate_with_stream(self, 
        model: str,
        prompt: str,
        temperature: float = 0.7,
    )->AsyncGenerator[str, None]:
        raise NotImplementedError
    
class OllamaQuery(AbstractLLMClient):
    def __init__(self,base_url:str=DEFAULT_BASE_URL, max_tokens:int=DEFAULT_MAX_TOKENS):
        self.client = AsyncClient(base_url)
        self.max_tokens = max_tokens

    async def generate(self, model: str, prompt: str, temperature: float = 0.7)-> str:
        try:
            response = await self.client.generate(
                model=model,
                prompt=prompt,
                options={
                    "temperature": temperature,
                    "num_predict": self.max_tokens
                },
                stream=False
            )
            return response["response"]
        except Exception as e:
            raise LLMQueryError(f"Failed to generate completion: {e}") from e
        
    async def generate_with_stream(self, prompt: str, model: str, temperature: float = 0.7)->AsyncGenerator[str, None]:
        try:
            async for chunk in await self.client.generate(
                model=model,
                    prompt=prompt,ß
                    options={
                        "temperature": temperature,
                        "num_predict": self.max_tokens
                    },
                    stream=True
                ):
                    yield chunk["response"]
        except Exception as e:
            raise LLMQueryError(f"Failed to stream completion: {e}") from e
        