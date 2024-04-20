from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common import mongo_logger
from app.common.database import get_connection
from app.routers.normal_chat_flow import router as normal_chat_flow_router
from app.routers.rag_flow import router as rag_flow_router

import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        connection = get_connection()
        db = connection["AI_Reference_Application"]
        await db.logs.find_one()
        yield
    except:
        logging.error("Failed to connect to the database")
        exit(0)


app = FastAPI(
    title="AI Reference Application",
    description="API for AI Reference Application",
    version="0.1",
    openapi_tags=[
        {
            "name": "openai",
            "description": "OpenAI API's",
        },
    ],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(normal_chat_flow_router)
app.include_router(rag_flow_router)


@app.get("/")
async def root():
    return {"Message": "Welcome to AI Reference Application API's"}


@app.get("/check_health")
def check_health():
    return {"Message": True}
