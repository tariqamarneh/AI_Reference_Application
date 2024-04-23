from app.services.langchain.chains import rag_flow_chain


async def generate_rag_output(text, callback, uid):
    config = {"configurable": {"session_id": f"{uid}"}}
    chain = await rag_flow_chain(callback, text)
    output = await chain.ainvoke({"question": text}, config=config)
    return output["output"]
