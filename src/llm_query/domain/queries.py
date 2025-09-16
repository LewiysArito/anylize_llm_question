from dataclasses import dataclass

class Query:
    pass

@dataclass
class GenerateResponse(Query):
    prompt: str
    temperature: float
    model: str
