## This is temp file for playing with streamlit and langgraph

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
import json

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def multiply(a: int, b: int) -> int:
    """"
    Multiply a and b

    Args :
      a (int) : first int
      b (int) : second int

    Return :
      int : output int
    """
    return a * b


def square(a: int) -> int:
    """"
    square a value

    Args :
      a (int) : int

    Return :
      int : output int
    """
    return a ** 2


tools = [multiply, square]

llm_with_tools = llm.bind_tools(tools)


def chat_bot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_conditional_edges("chat_bot", tools_condition)
graph_builder.add_edge("tools", "chat_bot")

graph = graph_builder.compile()


def getBotResponse(prompt: str) -> str:
    # Create a message list with instructions
    messages_list = [
        SystemMessage(content=(
            "You are a helpful assistant. You have access to two tools: `multiply` and `square`. "
            "Use them if they are relevant to the user's request. "
            "Otherwise, answer the user's question from your general knowledge."
        )),
        HumanMessage(content=prompt)
    ]

    # Invoke the graph with this new list
    response = graph.invoke({"messages": messages_list})

    ## convert the response to json format and print it 
    serializable_response = {
        "messages": [
            msg.dict() if hasattr(msg, "dict") else msg for msg in response["messages"]
        ]
    }
    print(json.dumps(serializable_response, indent=2))
    
    # If response["messages"][-1].content is json array get string value like content[0]['text']
    # If it's not json array return content as it is
    try:
        content_json = json.loads(response["messages"][-1].content)
        if isinstance(content_json, list) and len(content_json) > 0 and 'text' in content_json[0]:
            return content_json[0]['text']
        else:
            return response["messages"][-1].content
    except json.JSONDecodeError:
        return response["messages"][-1].content

messages = st.container()


def showUserMesg(prompt: str):
    messages.chat_message("user").write(prompt)


def showBotMesg(res):
    messages.chat_message("assistant").write(res)


prompt = st.chat_input("Say something")

if prompt:
    showUserMesg(prompt)
    with st.spinner("Waiting for response..."):
        response = getBotResponse(prompt)
        showBotMesg(response)
