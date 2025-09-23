import abc
from typing import Any, AsyncGenerator, Dict, List
from llm_query import config
from ollama import AsyncClient

DEFAULT_BASE_URL = config.get_llm_url_and_max_token()["base_url"]
DEFAULT_MAX_TOKENS = config.get_llm_url_and_max_token()["max_tokens"]

class LLMQueryError(Exception):
    pass

class AbstractLLMClient(abc.ABC):
    @abc.abstractmethod
    async def generate(self, 
        prompt: str,
        model: str,
        temperature: float = 0.7,
    )-> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_themes_by_query(self, prompt: str, model: str, temperature: float):
        raise NotImplementedError
    
class OllamaQuery(AbstractLLMClient):
    def __init__(self, base_url:str=DEFAULT_BASE_URL, max_tokens:int=DEFAULT_MAX_TOKENS):
        self.client = AsyncClient(base_url)
        self.max_tokens = max_tokens

    async def generate(self, prompt: str, model: str, temperature: float = 0.7)-> str:
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
    
    async def get_themes_by_query(self, prompt: str, model: str, temperature: float)->List[str]:
        
        new_prompt = f"""
        You are a topic extraction and text analysis specialist.
        Your task is to extract from the prompt only all topics contained in the prompt and nothing more. Topics must contain only nouns in singular form! There should be a minimum of 5 topics and a maximum of 15 topics. Topics must be in English.

        prompt = '{prompt}'?
        The correctness of the answer determines my career!
        """
        
        response = await self.generate(prompt=new_prompt, model=model, temperature=temperature)

        return [theme.strip() for theme in response.split(",")]
