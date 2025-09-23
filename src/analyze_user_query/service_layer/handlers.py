from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, List, Type
from analyze_user_query.domain import events, commands
from analyze_user_query.adapters import repository 

def anylize_user_query(
    cmd: commands.AnylizeUserQuery,
    repo: repository.AbstractColumnRepository,
):
    pass
    

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
} 

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.AnylizeUserQuery: anylize_user_query  
}
