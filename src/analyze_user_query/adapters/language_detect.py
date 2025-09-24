import asyncio
import abc
from ftlangdetect import detect

class AbstractFtlangDetect(abc.ABC):
    @abc.abstractmethod
    async def detect_language(self, text: str) -> str:
        raise NotImplementedError

class FtlangDetect(AbstractFtlangDetect):
    def __init__(self):
        pass
    
    async def definition_language(self, text: str)->str:
        code_country = await asyncio.to_thread(detect, text)["lang"]
        return code_country.upper()
        
