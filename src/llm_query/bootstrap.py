import inspect
from llm_query.adapters.kafka_event_publisher import AIOKafkaProducer, KafkaPublisher
from llm_query.adapters.ollama import AbstractLLMClient, OllamaQuery
from llm_query.service_layer import handlers, messagebus

def bootstrap(
    ollama: AbstractLLMClient = None,
    publisher: AIOKafkaProducer = None,
) -> messagebus.AsyncMessageBus:

    if ollama is None:
        ollama = OllamaQuery()

    if publisher is None:
        publisher = KafkaPublisher()

    dependencies = {"publisher": publisher, "ollama": ollama}
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

    return messagebus.MessageBus(
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
