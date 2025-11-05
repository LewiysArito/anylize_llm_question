from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, List, Type
from analyze_user_query.domain import events, commands
from analyze_user_query.adapters import repository 

def analyze_user_query(
    cmd: commands.AnalyzeUserQuery
):
    pass

def save_user_query(
    event: events.AnalyzeUserQuery,
):
    pass

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.ProcessedUserQuery: save_user_query
} 

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.AnalyzeUserQuery: analyze_user_query  
}
