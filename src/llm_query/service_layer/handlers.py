from typing import Callable, Dict, List, Type
from llm_query.domain import events, commands

def generate_response():
    pass

def public_data_for_anylize():
    pass

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.LLMResponseGenerated: [public_data_for_anylize],
} 

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.LLMResponseGenerate: generate_response,
}
