from app.services.langchain.chains import chat_flow_chain


async def generate_normal_output(text, callback, uid):
    config = {"configurable": {"session_id": f"{uid}"}}
    chain = chat_flow_chain(callback)
    output = await chain.ainvoke({"text": text}, config=config)
    return output["output"]
