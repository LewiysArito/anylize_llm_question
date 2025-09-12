# pylint: disable=too-few-public-methods
import abc
from typing import Any, AsyncGenerator, Dict
import config
from llm_query import config
from ollama import AsyncClient

DEFAULT_BASE_URL = config.get_llm_config()["base_url"]
DEFAULT_MAX_TOKENS = config.get_llm_config()["max_tokens"]

class LLMQueryError(Exception):
    pass

class AbstractLLMClient(abc.ABC):
    @abc.abstractmethod
    def generate(self, 
        model: str,
        prompt: str,
        temperature: float = 0.7,
    )-> Dict[str, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def generate_with_stream(self, 
        model: str,
        prompt: str,
        temperature: float,
    )->AsyncGenerator[Dict[str, Any] | None]:
        raise NotImplementedError
    
class OllamaQuery(AbstractLLMClient):
    def __init__(self,base_url:str=DEFAULT_BASE_URL, max_tokens:float=DEFAULT_MAX_TOKENS):
        self.client = AsyncClient(base_url)
        self.max_tokens = max_tokens

    async def generate(self, prompt: str, temperature:float, model: str):
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
        
    async def generate_with_stream(self, prompt: str, temperature: float, model: str):
        try:
            async for chunk in await self.client.generate(
                model=model,
                    prompt=prompt,
                    options={
                        "temperature": temperature,
                        "num_predict": self.max_tokens
                    },
                    stream=True
                ):
                    yield chunk["response"]
        except Exception as e:
            raise LLMQueryError(f"Failed to stream completion: {e}") from e
        