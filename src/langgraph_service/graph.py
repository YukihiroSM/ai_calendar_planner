from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from langgraph.prebuilt import ToolNode, tools_condition
from src.services.calendar_management import fetch_external_calendar_slots

from src import config
from src.langgraph_service.models import State
from src.langgraph_service.tools import human_assistance, confirm_meeting, analyze_slots_with_ai
from src.langgraph_service.llm_config import llm
logger = config.logger

graph_builder = StateGraph(State)

tools = [human_assistance, confirm_meeting, fetch_external_calendar_slots, analyze_slots_with_ai]
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    """Processes user inputs and ensures meetings are confirmed when the user agrees."""
    system_prompt = {
        "role": "system",
        "content": (
            "You are a scheduling assistant. Extract the following details from the user's message:\n"
            "- Meeting name (if mentioned)\n"
            "- Meeting date & time (infer from natural language, e.g., 'tomorrow at 3 PM')\n"
            "- Meeting duration - integer (infer units like '30 minutes', '1 hour') should amount of minutes\n"
            "If the user confirms all details and wants to schedule, trigger the `confirm_meeting` tool."
            "Do NOT ask for details again if everything is already provided."
        ),
    }

    response = llm_with_tools.invoke([system_prompt, *state["messages"]])

    if response.tool_calls:
        return {"messages": [response], "next": "tools"}

    return {"messages": [response]}

tool_node = ToolNode(tools=tools)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)
graph_builder.add_edge("tools", "chatbot")


memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
