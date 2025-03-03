from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    busy_slots: list
    meeting_datetime: str
    meeting_name: str
    meeting_duration: int
