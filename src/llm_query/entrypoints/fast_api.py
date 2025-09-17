from datetime import datetime
import uuid
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK
)
from fastapi import FastAPI, HTTPException, Request
import dataclasses

from llm_query.domain.model import UserQuery
from llm_query import bootstrap
from llm_query.adapters.ollama import LLMQueryError
from llm_query.domain import commands, queries

app = FastAPI()
router = app.router
bus, dispatcher = bootstrap.bootstrap()

@router.post(
    "/query", 
    status_code=HTTP_200_OK,
    summary="Query",
    description="Send request",
)
async def generate_response(request: Request, body: UserQuery):
    if len(body.prompt) == 0:
        raise HTTPException(HTTP_400_BAD_REQUEST, str("Prompt is empty"))
    
    try:
        query = queries.GenerateLLMQuery(**dataclasses.asdict(body))
        result = await dispatcher.dispatch(query)
        
        cmd = commands.UserQueryPublish(
            body.model,
            request.client.host,
            body.prompt,
            datetime.now()
        )
        await bus.handle(cmd)

        return {"response": result}
    except LLMQueryError:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str("Error query for llm"))