from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

from app.services.prompts.normal_chat_prompt import normal_chat_prompt
from app.services.prompts.rag_chat_prompt import rag_chat_prompt
from app.services.langchain.retriever import RetrieverSingleton
from app.services.langchain.llm import get_llm

memory_normal = ConversationBufferMemory(memory_key="hist")


def chat_flow_chain(callback):
    llm = get_llm(callback)
    chain = LLMChain(
        llm=llm,
        prompt=normal_chat_prompt,
        output_parser=StrOutputParser(),
        output_key="output",
        verbose=True,
        memory=memory_normal,
    )
    return chain


memory_rag = ConversationBufferMemory(memory_key="history")
retriever_singleton = RetrieverSingleton()


async def get_retriever():
    return await retriever_singleton.get_retriever()


async def rag_flow_chain(callback, text):
    llm = get_llm(callback)
    retriever = await get_retriever()
    context = retriever.invoke(input=text)
    context = "\n".join([doc.page_content for doc in context])
    chain = LLMChain(
        llm=llm,
        prompt=rag_chat_prompt.partial(context=context),
        output_parser=StrOutputParser(),
        output_key="output",
        verbose=True,
        memory=memory_rag,
    )
    return chain
