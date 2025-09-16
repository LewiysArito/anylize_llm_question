from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, List, Type
from llm_query.domain import events, commands

if TYPE_CHECKING:
    from llm_query.adapters import kafka_event_publisher

async def published_data_for_anylize_handlers(
    command: commands.PublishData,
    publisher: kafka_event_publisher.AbstractPublisher,
):
    await publisher.publish_one(
        "llm_anylize",
        command
    )

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
} 

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.PublishData: published_data_for_anylize_handlers
}
