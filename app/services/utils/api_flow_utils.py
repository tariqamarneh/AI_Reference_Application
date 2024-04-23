from app.services.langchain.chains import api_flow_chain


async def generate_api_output(text, callback, uid):
    config = {"configurable": {"session_id": f"{uid}"}}
    chain = api_flow_chain(callback, uid)
    output = await chain.ainvoke({"question": text}, config=config)
    return output["output"]
