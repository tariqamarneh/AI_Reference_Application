from app.services.langchain.chains import rag_flow_chain


async def generate_rag_output(text, callback):
    chain = await rag_flow_chain(callback, text)
    output = await chain.ainvoke({"question": text})
    return output["output"]
