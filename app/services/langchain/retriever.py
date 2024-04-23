import io

from PyPDF2 import PdfReader
from langchain.vectorstores.chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.config import AZURE_ENDPOINT, OPENAI_API_KEY
from app.common import connection


class RetrieverSingleton:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._initialized = True
        return cls._instance

    async def extract_text_from_pdf(self):
        files = connection["AI_Reference_Application"]["files"]
        cursor = files.find()
        extracted_files = []
        for file in await cursor.to_list(length=100):
            pdf = PdfReader(stream=io.BytesIO(file["data"]))
            extracted_text = ""
            for page_num in range(len(pdf.pages)):
                page = pdf.pages[page_num]
                extracted_text += page.extract_text()

            extracted_files.append(
                Document(
                    page_content=extracted_text, metadata={"filename": file["filename"]}
                )
            )
        return extracted_files

    async def split_text(self, extracted_files):
        spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        extracted_files_splittes = spliter.split_documents(extracted_files)
        return extracted_files_splittes

    async def get_vector_db(self, extracted_files_splittes):
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment="ada002",
            openai_api_version="2023-09-15-preview",
            api_key=OPENAI_API_KEY,
            azure_endpoint=AZURE_ENDPOINT,
        )
        vectordb = Chroma.from_documents(extracted_files_splittes, embedding=embeddings)
        return vectordb

    async def get_retriever(self):
        extracted_files = await self.extract_text_from_pdf()
        extracted_files_splittes = await self.split_text(extracted_files)
        vectordb = await self.get_vector_db(extracted_files_splittes)
        retriever = vectordb.as_retriever()
        self._instance.retriever = retriever
        self._initialized = True
        return retriever
