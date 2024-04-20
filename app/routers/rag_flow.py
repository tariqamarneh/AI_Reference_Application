from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from app.routers.utils import send_message_to_rag_flow
from app.common import connection, mongo_logger


router = APIRouter()


@router.post("/rag_chat_flow", tags=["openai"])
async def generate_output(text: str) -> StreamingResponse:
    try:
        return StreamingResponse(
            send_message_to_rag_flow(text), media_type="text/event-stream"
        )
    except Exception as e:
        mongo_logger.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to generate output."
        )


@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            mongo_logger.warning("Only PDF files are allowed to upload.")
            return HTTPException(
                status_code=400, detail="Only PDF files are allowed to upload."
            )
        file_content = await file.read()
        files_collection = connection["AI_Reference_Application"]["files"]
        file_id = await files_collection.insert_one(
            {"filename": file.filename, "data": file_content}
        )
        return {
            "message": "PDF uploaded successfully",
            "file_id": str(file_id.inserted_id),
        }
    except Exception as e:
        mongo_logger.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to upload file."
        )
