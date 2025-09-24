import inspect
from typing import Tuple
from analyze_user_query.service_layer import handlers, messagebus, query_handlers, query_dispatcher
from analyze_user_query.adapters.http_ip_geolocation import AbstractIpGeolocation, IpInfoService 
from analyze_user_query.adapters.ollama import AbstractLLMClient, OllamaQuery
from analyze_user_query.adapters.repository import AbstractColumnRepository, ClickhouseRepository
from analyze_user_query.adapters.language_detect import AbstractFtlangDetect, FtlangDetect

def bootstrap(
    ip_geolocation: AbstractIpGeolocation = None,
    llm: AbstractLLMClient = None,
    repo: AbstractColumnRepository = None,
    language_detect: AbstractFtlangDetect = None
) -> Tuple[messagebus.AsyncMessageBus, query_dispatcher.AsyncQueryDispatcher]:

    if ip_geolocation is None:
        ip_geolocation = IpInfoService()
    
    if llm is None:
        llm = OllamaQuery()
    
    if repo is None:
        repo = ClickhouseRepository()
    
    if language_detect is None:
        language_detect = FtlangDetect()

    dependencies = {
        "repo": repo,
        "ip_geolocation": ip_geolocation,
        "llm": llm,
        "language_detect": language_detect
    }
    
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    inject_query_handlers = {
        query_type: inject_dependencies(handler, dependencies)
        for query_type, handler in query_handlers.QUERY_HANDLERS.items()     
    }

    bus = messagebus.AsyncMessageBus(
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

    dispatcher = query_dispatcher.AsyncQueryDispatcher(inject_query_handlers) 

    return bus, dispatcher

def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
