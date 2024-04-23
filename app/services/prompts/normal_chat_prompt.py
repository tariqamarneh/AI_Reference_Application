from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


normal_chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a chatbot having a chat with a human, Be polite and respectful."),
        MessagesPlaceholder(variable_name="hist"),
        ("human", "{text}"),
    ]
)
