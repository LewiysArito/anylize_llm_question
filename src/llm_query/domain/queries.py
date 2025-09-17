from dataclasses import dataclass

class Query:
    pass

@dataclass(frozen=True)
class GenerateLLMQuery(Query):
    prompt: str
    temperature: float
    model: str
