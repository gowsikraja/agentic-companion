import json
from typing import TypedDict, Annotated, Optional

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from tools import all_tools
import config
from pydantic import BaseModel


class State(TypedDict):
    """
    This TypedDict defines the state of our graph.
    The 'messages' key will hold a list of messages,
    and 'add_messages' ensures new messages are appended.
    """
    messages: Annotated[list, add_messages]
    response: Optional[str] = None  # type: ignore


class OutputState(TypedDict):
    response: str


class ChatAgent:
    """
    This class encapsulates the LangGraph agent, including the LLM,
    tools, and the compiled graph.
    """

    def __init__(self):
        # 1. Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model=config.MODEL_NAME,
            # google_api_key=config.GOOGLE_API_KEY,
            # Add this to get more predictable, structured JSON-like tool calls
            convert_system_message_to_human=True
        )

        # 2. Bind the tools to the LLM
        self.tools = all_tools
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # 3. Define the graph
        self.graph = self._build_graph()

    def _chat_bot_node(self, state: State):
        """
        This node invokes the LLM with the current state's messages.
        The LLM decides whether to call a tool or respond directly.
        """
        response = self.llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def _build_graph(self):
        """
        Builds and compiles the LangGraph.
        """
        graph_builder = StateGraph(State, output_schema=OutputState)

        graph_builder.add_node("chat_bot", self._chat_bot_node)
        graph_builder.add_node("tools", ToolNode(self.tools))
        graph_builder.add_node("prepare_output", self._prepare_output)

        graph_builder.add_edge(START, "chat_bot")
        graph_builder.add_conditional_edges(
            "chat_bot",
            tools_condition,
            # Route to our new output node instead of END
            {"tools": "tools", END: "prepare_output"} 
        )
        graph_builder.add_edge("tools", "chat_bot")
        graph_builder.add_edge("prepare_output", END)

        # Compile the graph
        return graph_builder.compile()

    def _get_system_prompt(self):
        """Returns the static system prompt."""
        return SystemMessage(content=(
            "You are a helpful assistant. You have access to two tools: `multiply` and `square`. "
            "Use them if they are relevant to the user's request. "
            "Otherwise, answer the user's question from your general knowledge."
        ))

    def _prepare_output(self, state: State) -> dict:
        """
        Extracts the final message content and maps it 
        to the 'response' key in the State.
        """
        final_content = state["messages"][-1].content
        return {"response": final_content}

    def invoke(self, prompt: str) -> str:
        """
        Public method to invoke the agent.
        It handles message formatting, graph invocation, and response parsing.
        """
        # 1. Create the message list
        messages_list = [
            self._get_system_prompt(),
            HumanMessage(content=prompt)
        ]

        # 2. Invoke the graph
        response = self.graph.invoke({"messages": messages_list})  # type: ignore

        # This will fail, but that's okay, we'll print the dict
        try:
            print(json.dumps(response, indent=2))
        except TypeError:
            print(f"Could not JSON dump: {response}")

        # Return the content from the 'response' key
        return response["response"]
