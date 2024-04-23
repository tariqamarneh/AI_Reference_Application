from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, Header

from app.common import mongo_logger
from app.routers.utils import send_message_to_chat_flow


router = APIRouter()


@router.post("/normal_chat_flow", tags=["openai"])
async def generate_output(text: str, uid: str = Header(None)) -> StreamingResponse:
    print(uid)
    try:
        return StreamingResponse(
            send_message_to_chat_flow(text, uid), media_type="text/event-stream"
        )
    except Exception as e:
        mongo_logger.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to generate output."
        )
