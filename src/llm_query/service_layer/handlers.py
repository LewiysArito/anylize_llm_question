from typing import TYPE_CHECKING, Callable, Dict, List, Type
from llm_query.domain import events, commands

if TYPE_CHECKING:
    from llm_query.adapters import ollama, kafka_event_publisher

async def generate_response(
    llm: ollama.AbstractLLMClient,
    cmd: commands.LLMResponseGenerate
)->str:
    response = await llm.generate(
       model=cmd.model,
       prompt=cmd.prompt,
       temperature=cmd.temperature 
    )
    return response

async def published_data_for_anylize(
    publisher: kafka_event_publisher.AIOKafkaProducer,
    event: events.LLMResponseGenerated,
):
    pass

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.LLMResponseGenerated: [published_data_for_anylize],
} 

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.LLMResponseGenerate: generate_response,
}
