import inspect
from typing import Tuple
from llm_query.adapters.kafka_event_publisher import AIOKafkaProducer, KafkaPublisher
from llm_query.adapters.ollama import AbstractLLMClient, OllamaQuery
from llm_query.service_layer import handlers, messagebus, query_handlers, query_dispatcher

def bootstrap(
    llm: AbstractLLMClient = None,
    publisher: AIOKafkaProducer = None,
) -> Tuple[messagebus.AsyncMessageBus, query_dispatcher.AsyncQueryDispatcher]:

    if llm is None:
        llm = OllamaQuery()

    if publisher is None:
        publisher = KafkaPublisher()

    dependencies = {"publisher": publisher, "llm": llm}
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
    
    param_names = list(params.keys())
    if param_names:
        main_param = param_names[0]
        dep_params = param_names[1:]
    else:
        dep_params = []
    
    deps = {}
    for dep_name in dep_params:
        if dep_name in dependencies:
            deps[dep_name] = dependencies[dep_name]
        else:
            raise Exception(f"Warning: Dependency '{dep_name}' not found for {handler.__name__}")
    
    if inspect.iscoroutinefunction(handler):
        async def injected_handler(message):
            return await handler(message, **deps)
    else:
        def injected_handler(message):
            return handler(message, **deps)
            
    return injected_handler