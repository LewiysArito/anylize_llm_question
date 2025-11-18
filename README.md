# analyze-user-query

Small monorepo for processing and analyzing user queries.
Architecture follows layered/hexagonal principles (domain / service_layer / adapters / entrypoints) and uses CQRS-style queries/commands + message bus.

## Quick overview

- Purpose: receive user queries, define the language for the text, extract themes via LLM, enrich (IP → region), persist results (ClickHouse), and publish domain events for downstream consumers.
- Main folders:
  - `src/analyze_user_query` — primary bounded context (ingestion, analysis, ClickHouse persistence).
  - `src/llm_query` — LLM-adapter service / helper context (LLM-specific logic or separate LLM service).
  - `src/*/adapters` — infra code (ClickHouse, TaskIQ/Kafka/Redis, Ollama, geolocation, langdetect).
  - `src/*/service_layer` — application services / handlers / dispatcher.
  - `src/*/domain` — domain models, commands, queries, events.

## Technology Stack

### Core Framework & Language
- **Python 3.12** - primary programming language
- **FastAPI** - modern web framework for building REST APIs
- **Custom DI Container** - dependency injection implementation (`bootstrap.py`)
- **Poetry** - dependency management and packaging

### Message Processing & Events
- **TaskIQ** - distributed task queue for background job processing
- **Redis** - message broker backend for TaskIQ (handles delayed tasks and worker coordination)
- **Kafka** - event streaming platform for domain event distribution
- **Custom Task Manager** - abstraction layer for task lifecycle management (`TaskIqRedisTaskManager`)

### Data Storage & Caching
- **ClickHouse** - column-oriented analytical database for query results and analytics
- **Redis** - in-memory data structure store used for caching

### AI & Machine Learning
- **Ollama** - local LLM server running language models for text analysis
- **fast-langdetect** - fast and efficient language detection library
- **countryinfo** - geographical data library for IP-based location enrichment

### Architectural Patterns
- **Hexagonal Architecture** - clean separation of concerns with domain, application, and infrastructure layers
- **CQRS** - command query responsibility segregation for separate read/write models
- **Event-Driven Architecture** - asynchronous communication through domain events
- **Repository Pattern** - abstraction layer between domain and data mapping layers
- **Custom ORM Pattern** - proprietary data access abstraction

## Bounded contexts (short)

- analyze_user_query
  - Responsibility: ingestion, orchestration of the analysis pipeline, enrichment, persistence, and analytics API.
  - Key responsibilities:
    - Accept events/requests (HTTP, Kafka).
    - Use `DefineLanguage` query (via dispatcher) and the LLM adapter to extract themes.
    - Save analyzed results into ClickHouse via repository adapter (idempotent by `event_id` recommended).
    - Provide analytics endpoints for query results and publish domain events (via EventPublisher / outbox pattern) for downstream consumers.
  - Typical entrypoints: FastAPI, Kafka consumer, TaskIQ worker.

- llm_query
  - Responsibility: wrapper around Ollama (or other LLMs) that receives client requests and forwards/normalizes them for analysis by other services.
  - Key responsibilities:
    - Provide a stable API for theme extraction, summarization, and related text analysis.
    - Handle LLM-specific concerns: retries, rate limits, timeouts, and response normalization.
    - Expose a simple adapter interface consumed by application services or other bounded contexts.
  - Deployment: can be a separate microservice (recommended when LLM usage, scaling, or isolation is required) or an adapter library.

Each context should have its own documentation (this file gives global overview).

## Getting started (dev)

Prerequisites:
- Python 3.12
- Poetry (recommended) or venv + pip
- Docker & Docker Compose (for infra: ClickHouse, Redis,Kafka,Ollama)

Install (Poetry):
```bash
poetry install
poetry shell
```
Or create venv and install editable package:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run infra (example with repo top-level compose):
```bash
docker compose -f docker-compose.yml --env-file .env up --build -d
```

Create ClickHouse tables:
```bash
# inside container or local env where ClickHouse client configured
python -m analyze_user_query.adapters.init_db
# or via Makefile target (adjust container name)
make docker-create-table
```

Run services:
```bash
# Analyze API
uvicorn analyze_user_query.entrypoints.fast_api:app --reload --host 0.0.0.0 --port ${API_PORT_ANALYZE_USER_QUERY:-8000}

# LLM service (if applicable)
uvicorn llm_query.entrypoints.fast_api:app --reload --host 0.0.0.0 --port ${API_PORT_LLM_QUERY:-8001}

# Task worker
python -m analyze_user_query.entrypoints.taskiq_consumer

# Kafka consumer
python -m analyze_user_query.entrypoints.kafka_eventconsumer
```

```
Run tests:
```bash
pytest -q
```

## Run via Makefile

You can start infra and services using the repository Makefile targets (use tabs for Makefile commands):

- `make docker-infras-up` — start infra (ClickHouse, Redis, Kafka, etc.) via top-level docker-compose.
- `make docker-analyze-user-query-up` — start the analyze_user_query service compose.
- `make docker-llm-query-up` — start the llm_query service compose.
- `make docker-create-table` — run the ClickHouse table creation/init script (adjust target to your environment).

Examples:
```bash
# start infra
make docker-infras-up

# start analyze service
make docker-analyze-user-query-up

# start llm service
make docker-llm-query-up

# create ClickHouse tables (inside the container or via the target)
make docker-create-table
```

## Notes & recommendations

- Prefer wiring dependencies via `bootstrap.py` (composition root). Do not import entrypoint task functions into service layer — use dispatcher/adapters for DI and testability.
- Keep domain logic pure: no direct I/O in domain models. Use adapters for infra.
- When splitting bounded contexts into microservices, create separate package/pyproject per service and expose shared code via `libs/common` or path-dependencies.

## Contributing

If anything feels off or if you feel that some functionality is missing, please check out the [contributing page](.github/CONTRIBUTING.md). There you will find instructions for sharing your feedback, building the tool locally, and submitting pull requests to the project.

## Contact / License

- Author: LewiysArito (nikita.kasimov.1044@gmail.com)  
- License: add `LICENSE` file (e.g. MIT) if desired.