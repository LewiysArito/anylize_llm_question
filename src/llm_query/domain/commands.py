from dataclasses import dataclass

class Command:
    pass

@dataclass
class LLMResponseGenerate(Command):
    prompt: str
    temperature: float
    model: str