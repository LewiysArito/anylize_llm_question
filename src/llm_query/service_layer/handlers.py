from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Callable, Dict, List, Type
from llm_query.adapters.integration_events import UserQueryPublishedEvent
from llm_query.domain import events, commands

if TYPE_CHECKING:
    from llm_query.adapters import kafka_event_publisher

async def handle_publish_user_query(
    command: commands.UserQueryPublish,
    publisher: kafka_event_publisher.AbstractPublisher,
):
    integration_event = UserQueryPublishedEvent(
        str(uuid.uuid4()),
        command.model,
        command.ip_address,
        command.raw_text,
        str(command.created_at)
    )
    await publisher.publish_one(
        "llm_anylize",
        integration_event
    )

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
} 

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.UserQueryPublish: handle_publish_user_query
}
