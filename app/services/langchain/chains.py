from langchain.chains.llm import LLMChain
from langchain.chains.api.base import APIChain
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities.requests import TextRequestsWrapper
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

from app.config import connection_string
from app.services.langchain.llm import get_llm, get_llm_app
from app.services.langchain.retriever import RetrieverSingleton
from app.services.prompts.normal_chat_prompt import normal_chat_prompt
from app.services.prompts.rag_chat_prompt import rag_chat_prompt
from app.services.prompts.api_chat_prompt import (
    api_docs,
    API_URL_PROMPT,
    API_RESPONSE_PROMPT,
)


def chat_flow_chain(callback):
    llm = get_llm(callback)
    chain = LLMChain(
        llm=llm,
        prompt=normal_chat_prompt,
        output_parser=StrOutputParser(),
        output_key="output",
        verbose=True,
    )
    chain = RunnableWithMessageHistory(
        chain,
        lambda session_id: MongoDBChatMessageHistory(
            connection_string=connection_string,
            session_id=session_id,
            database_name="AI_Reference_Application",
            collection_name="chat_message_histories",
        ),
        input_messages_key="text",
        output_messages_key="output",
        history_messages_key="hist",
    )
    return chain


retriever_singleton = RetrieverSingleton()


async def rag_flow_chain(callback, text):
    llm = get_llm(callback)
    retriever = retriever_singleton.retriever
    context = retriever.invoke(input=text)
    context = "\n".join([doc.page_content for doc in context])
    chain = LLMChain(
        llm=llm,
        prompt=rag_chat_prompt.partial(context=context),
        output_parser=StrOutputParser(),
        output_key="output",
        verbose=True,
    )
    chain = RunnableWithMessageHistory(
        chain,
        lambda session_id: MongoDBChatMessageHistory(
            connection_string=connection_string,
            session_id=session_id,
            database_name="AI_Reference_Application",
            collection_name="chat_message_histories",
        ),
        input_messages_key="question",
        output_messages_key="output",
        history_messages_key="hist",
    )
    return chain


def api_flow_chain(callback, uid):
    fetch_messages = lambda session_id: MongoDBChatMessageHistory(
        connection_string=connection_string,
        session_id=session_id,
        database_name="AI_Reference_Application",
        collection_name="chat_message_histories",
    ).messages

    chain = APIChain(
        name="api_flow",
        verbose=True,
        api_request_chain=LLMChain(
            prompt=API_URL_PROMPT,
            llm=get_llm_app(),
            output_key="output",
            output_parser=StrOutputParser(),
        ),
        api_answer_chain=LLMChain(
            prompt=API_RESPONSE_PROMPT.partial(hist=fetch_messages(uid)),
            llm=get_llm(callback=callback),
            output_key="output",
            output_parser=StrOutputParser(),
        ),
        api_docs=api_docs,
        question_key="question",
        output_key="output",
        limit_to_domains=None,
        requests_wrapper=TextRequestsWrapper(),
    )
    chain = RunnableWithMessageHistory(
        chain,
        lambda session_id: MongoDBChatMessageHistory(
            connection_string=connection_string,
            session_id=session_id,
            database_name="AI_Reference_Application",
            collection_name="chat_message_histories",
        ),
        input_messages_key="question",
        output_messages_key="output",
    )
    return chain
