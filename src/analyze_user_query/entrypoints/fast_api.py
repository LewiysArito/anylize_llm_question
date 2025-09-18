from datetime import datetime
import uuid
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK
)
from fastapi import FastAPI, HTTPException, Request
import dataclasses


app = FastAPI()
router = app.router
bus, dispatcher = bootstrap.bootstrap()