from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Callable, Dict, List, Type
from anylize_user_query.domain import events, commands

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
} 

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
}
