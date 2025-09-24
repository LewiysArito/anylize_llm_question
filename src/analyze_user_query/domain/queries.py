from dataclasses import dataclass

class Query:
    pass

@dataclass
class DefineLanguage(Query):
    text: str