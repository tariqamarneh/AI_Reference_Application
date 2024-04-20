import io

from langchain.vectorstores.chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.config import AZURE_ENDPOINT, OPENAI_API_KEY
from app.common import connection


class RetrieverSingleton:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def extract_text_from_pdf(self):
        files = connection["AI_Reference_Application"]["files"]
        file = await files.find_one()
        pdf = PdfReader(stream=io.BytesIO(file["data"]))
        extracted_text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            extracted_text += page.extract_text()
        return extracted_text

    async def split_text(self):
        extracted_text = await self.extract_text_from_pdf()
        spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        docs = spliter.split_text(extracted_text)
        return docs

    async def get_vector_db(self):
        docs = await self.split_text()
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment="ada002",
            openai_api_version="2023-09-15-preview",
            api_key=OPENAI_API_KEY,
            azure_endpoint=AZURE_ENDPOINT,
        )
        vectordb = Chroma.from_texts(docs, embedding=embeddings)
        return vectordb

    async def get_retriever(self):
        vectordb = await self.get_vector_db()
        retriever = vectordb.as_retriever()
        return retriever
