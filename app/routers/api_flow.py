from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import StreamingResponse

from app.routers.utils import send_message_to_api_flow
from app.common import mongo_logger


router = APIRouter()


@router.post("/api_chat_flow", tags=["openai"])
async def generate_output(text: str, uid: str = Header(None)) -> StreamingResponse:
    try:
        return StreamingResponse(
            send_message_to_api_flow(text, uid), media_type="text/event-stream"
        )
    except Exception as e:
        mongo_logger.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to generate output."
        )


@router.get("/handle_normal_user_query")
def handle_normal_user_query():
    return None
