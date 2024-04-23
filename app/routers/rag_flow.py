from typing import List

from fastapi import APIRouter, File, Header, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse

from app.common import connection, mongo_logger
from app.routers.utils import send_message_to_rag_flow


router = APIRouter()


@router.post("/rag_chat_flow", tags=["openai"])
async def generate_output(text: str, uid: str = Header(None)) -> StreamingResponse:
    try:
        return StreamingResponse(
            send_message_to_rag_flow(text, uid), media_type="text/event-stream"
        )
    except Exception as e:
        mongo_logger.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to generate output."
        )


@router.post("/_uploadfiles")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        connection["AI_Reference_Application"].drop_collection("files")
        files_collection = connection["AI_Reference_Application"]["files"]
        other_files = []
        file_ids = []
        for file in files:
            if file.content_type != "application/pdf":
                mongo_logger.warning(f"File '{file.filename}' is not a PDF. Skipping.")
                other_files.append(file.filename)
                continue
            file_content = await file.read()
            file_id = await files_collection.insert_one(
                {"filename": file.filename, "data": file_content}
            )
            file_ids.append(str(file_id.inserted_id))
        if not file_ids:
            return HTTPException(status_code=400, detail="No PDF files were uploaded.")
        if other_files:
            return JSONResponse(
                content={
                    "message": "PDFs uploaded successfully, but these files were ignored because they are not PDFs: "
                    + ", ".join(other_files)
                    + "."
                }
            )
        return JSONResponse(content={"message": "PDFs uploaded successfully"})
    except Exception as e:
        mongo_logger.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to upload files."
        )


@router.get("/upload_files", tags=["Upload files"])
async def main():
    content = """
        <body>
            <form action="/_uploadfiles/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)
