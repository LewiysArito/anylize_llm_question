from dataclasses import dataclass

class Event:
    pass

@dataclass
class LLMResponseGenerated(Event):
    pass
