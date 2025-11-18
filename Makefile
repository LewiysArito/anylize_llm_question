export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

docker-infras-up:
	docker compose -f docker-compose.yml --env-file=.env up --remove-orphans --build

docker-analyze-user-query-up:
	docker compose -f ./src/analyze_user_query/docker-compose.yml --env-file=./src/analyze_user_query/.env up --remove-orphans --build

docker-create-table:
	docker exec -it api-analyze-llm-query python -m analyze_user_query.adapters.init_db

docker-llm-query-up:
	docker compose -f ./src/llm_query/docker-compose.yml --env-file=./src/llm_query/.env up --remove-orphans --build

docker-all-up: docker-infras-up docker-analyze-user-query-up docker-llm-query-up

docker-all-down:
	docker compose -f docker-compose.yml down
	docker compose -f ./src/analyze_user_query/docker-compose.yml down
	docker compose -f ./src/llm_query/docker-compose.yml down

status:
	docker compose -f docker-compose.yml ps
	docker compose -f ./src/analyze_user_query/docker-compose.yml ps
	docker compose -f ./src/llm_query/docker-compose.yml ps