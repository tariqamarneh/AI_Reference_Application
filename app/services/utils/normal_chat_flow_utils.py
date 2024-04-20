from app.services.langchain.chains import chat_flow_chain


async def generate_normal_output(text, callback):
    chain = chat_flow_chain(callback)
    output = await chain.ainvoke({"text": text})
    return output["output"]
