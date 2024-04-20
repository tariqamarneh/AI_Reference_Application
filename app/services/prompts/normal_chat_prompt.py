from langchain.prompts import PromptTemplate


system_message = """
You are a Model having a chat with a human

{hist}
Human: {text}
Chatbot:
"""


normal_chat_prompt = PromptTemplate(
    template=system_message, input_variables=["hist", "text"]
)
