from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
load_dotenv()

model = ChatOpenAI(model = "gpt-5-nano", temperature = 1)



chat_templete = ChatPromptTemplate([
    ("system", "You are a chatbot"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")]
)


chat_history = []



while True:
    user = input("User: ")
    chat_templete.invoke({"chat_history": chat_history, "input": user})
    chat_history.append(HumanMessage(content = user))
    res = model.invoke(chat_history)
    chat_history.append(AIMessage(content = res.content))
    print("chatbot: ", res.content)