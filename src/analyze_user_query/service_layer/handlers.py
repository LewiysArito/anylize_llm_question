from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, List, Type

from analyze_user_query.domain import events, commands
from analyze_user_query.domain import model
from analyze_user_query.adapters import repository 

async def save_user_query(
    command: commands.SaveUserQuery,
    repo: repository.AbstractColumnRepository
):
    analyzed_user_query_orm = model.AnalyzedUserQueryOrm(
        event_id=str(command.event_id),
        text=command.text,
        date=command.date.strftime("%Y-%m-%d"),
        themes=command.themes,
        language_code=command.language_code,
        country_code=command.country_code,
        user_ip=str(command.user_ip),
        model_llm=command.model_llm
    )
    await repo.add(analytic=analyzed_user_query_orm)

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
} 

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.SaveUserQuery: save_user_query
}
