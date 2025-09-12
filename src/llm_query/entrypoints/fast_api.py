from datetime import datetime
from fastapi import FastAPI
from llm_query.domain import commands
from llm_query.domain.model import UserQuery
from llm_query.service_layer.handlers import InvalidSku
from llm_query import bootstrap

app = FastAPI()
bus = bootstrap.bootstrap()

@app.route("/query", methods=["POST"])
async def generate_response(request: UserQuery):
    pass

@app.route("/query-stream")
async def generate_response_stream(request: UserQuery):
    pass