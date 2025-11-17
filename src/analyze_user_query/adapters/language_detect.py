import asyncio
import abc
from fast_langdetect import detect_language

class AbstractFtlangDetect(abc.ABC):
    @abc.abstractmethod
    async def definition_language(self, text: str) -> str:
        raise NotImplementedError

class FtlangDetect(AbstractFtlangDetect):
    def __init__(self):
        pass
    
    async def definition_language(self, text: str)->str:
        code_country = await asyncio.to_thread(detect_language, text)
        return code_country