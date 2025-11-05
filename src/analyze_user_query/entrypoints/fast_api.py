from datetime import datetime
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK
)
from fastapi import FastAPI

from analyze_user_query import bootstrap

app = FastAPI()
router = app.router
bus, dispatcher = bootstrap.bootstrap()