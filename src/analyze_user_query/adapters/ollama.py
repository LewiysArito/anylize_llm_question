import abc
from typing import List
from analyze_user_query import config
from ollama import AsyncClient

DEFAULT_BASE_URL = config.get_llm_url_and_max_token()["base_url"]
DEFAULT_MAX_TOKENS = config.get_llm_url_and_max_token()["max_tokens"]
logger = config.logger

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
    async def get_themes_by_query(self, prompt: str, model: str, temperature: float = 0.7)->List[str]:
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
            error = f"Failed to generate completion: {e}"
            logger.error(error)
            raise LLMQueryError(error)
    
    async def get_themes_by_query(self, prompt: str, model: str, temperature: float = 0.7)->List[str]:
        
        new_prompt = f"""
        You are a topic extraction and text analysis specialist.
        Your task is to extract from the prompt only all topics contained in the prompt and nothing more. Topics must contain only nouns in singular form! There should be a minimum of 5 topics and a maximum of 10 topics. Topics must be in English and listed separated by commas.

        prompt = '{prompt}'
        The correctness of the answer determines my career!

        Respond only with the list of topics separated by commas, without any additional text, explanations or formatting.
        """        
        
        response = await self.generate(prompt=new_prompt, model=model, temperature=temperature)

        return [theme.strip() for theme in response.split(",")]
