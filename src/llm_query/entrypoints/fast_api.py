from datetime import datetime
import uuid
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK
)
from fastapi import FastAPI, HTTPException, Request

from llm_query.domain.model import UserQuery
from llm_query import bootstrap, views
from llm_query.adapters.ollama import LLMQueryError
from llm_query.domain import commands

app = FastAPI()
router = app.router
bus = bootstrap.bootstrap()

@router.post(
    "/query", 
    status_code=HTTP_200_OK,
    summary="Query",
    description="Send request",
)
async def generate_response(request: Request, body: UserQuery):
    if len(body.prompt) == 0:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(""))

    try:
        result = await views.generate_response(
            body,
            
        )
    except LLMQueryError:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str("Error query for llm"))
    
    cmd = commands.PublishDataToAnylize(
        uuid.uuid4(),
        body.model,
        request.client.host,
        body.prompt,
        datetime.datetime.now()
    )

    await bus.handle(cmd)

    return {"response": result}