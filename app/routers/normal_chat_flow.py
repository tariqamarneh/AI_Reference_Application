from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.routers.utils import send_message_to_chat_flow
from app.common import mongo_logger


router = APIRouter()


@router.post("/normal_chat_flow", tags=["openai"])
async def generate_output(text: str) -> StreamingResponse:
    try:
        return StreamingResponse(
            send_message_to_chat_flow(text), media_type="text/event-stream"
        )
    except Exception as e:
        mongo_logger.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to generate output."
        )
