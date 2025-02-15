from langchain_openai import AzureChatOpenAI

from app.config import AZURE_ENDPOINT, OPENAI_API_KEY


def get_llm(callback):
    azure_llm = AzureChatOpenAI(
        deployment_name="gpt4",
        azure_endpoint=AZURE_ENDPOINT,
        openai_api_key=OPENAI_API_KEY,
        api_version="2024-02-15-preview",
        temperature=0,
        model="gpt-4",
        streaming=True,
        callbacks=[callback],
    )
    return azure_llm


def get_llm_app():
    azure_llm = AzureChatOpenAI(
        deployment_name="gpt4",
        azure_endpoint=AZURE_ENDPOINT,
        openai_api_key=OPENAI_API_KEY,
        api_version="2024-02-15-preview",
        temperature=0,
        model="gpt-4",
    )
    return azure_llm
