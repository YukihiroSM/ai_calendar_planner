from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, InjectedToolCallId
import datetime
from typing import Annotated, Optional

from langgraph.types import interrupt, Command
from src.services.calendar_management import (
    fetch_external_calendar_slots,
    create_google_calendar_event,
)
from src import config
from src.langgraph_service.models import State
from src.langgraph_service.llm_config import llm
logger = config.logger

@tool
def confirm_meeting(
    tool_call_id: Annotated[str, InjectedToolCallId],
    meeting_duration: int,
    meeting_datetime: str,
    meeting_name: str
):
    """Executes function to create a Google meeting based on user results. Should be just triggered with state object"""
    logger.debug(f"Done successfully: {meeting_duration}, {meeting_datetime}, {meeting_name}")
    end_time = (
            datetime.datetime.fromisoformat(meeting_datetime)
            + datetime.timedelta(minutes=float(meeting_duration))
    ).isoformat()

    created_event = create_google_calendar_event(
        chosen_slot=meeting_datetime, end_time=end_time, meeting_name=meeting_name
    )

    response = f"Done! Here is a meeting link: {created_event['htmlLink']}"
    return {
        "messages": [[ToolMessage(response, tool_call_id=tool_call_id)]]
    }


@tool
def human_assistance(
    tool_call_id: Annotated[str, InjectedToolCallId],
    meeting_duration: Optional[int] = None,
    meeting_datetime: Optional[str] = None,
    meeting_name: Optional[str] = None
) -> str | Command:
    """Request meeting details confirmation from a human."""
    human_response = interrupt(
        {
            "question": "Is this correct?",
            "meeting_duration": meeting_duration,
            "meeting_datetime": meeting_datetime,
            "meeting_name": meeting_name,
        },
    )

    if human_response.get("correct", "").lower().startswith("y"):
        verified_meeting_duration = meeting_duration
        verified_meeting_datetime = meeting_datetime
        verified_meeting_name = meeting_name
        response = "Correct"

    else:
        verified_meeting_duration = human_response.get("meeting_duration", meeting_duration)
        verified_meeting_datetime = human_response.get("meeting_datetime", meeting_datetime)
        verified_meeting_name = human_response.get("meeting_name", meeting_name)
        response = f"Made a correction: {human_response}"

    state_update = {
        "meeting_duration": verified_meeting_duration,
        "meeting_datetime": verified_meeting_datetime,
        "meeting_name": verified_meeting_name,
        "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
    }

    return Command(update=state_update)


@tool
def analyze_slots_with_ai(state: State):
    """Retrieve meeting datetime, name, duration of user's meeting"""
    prompt = f"""
        You are an assistant for defining parameters to schedule a meeting in future. Here are the busy slots from the external calendar:
        {state["busy_slots"]}
        Consider, that busy slots are from external calendar. After getting slots - just ask user to give you the appropriate info
        Ask the user for the date, time, and duration of the meeting if they haven't provided it yet.
        Check if the selected slot is available. If not, ask for an alternative option.
        You must answer only regarding this task, you are just a small tool to find available slots. 
        For any other options - just repeat the questions, which you still need to have answers. 
    """

    if not state.get("messages"):
        response = {
            "role": "assistant",
            "content": "Hello! To schedule a meeting, please provide your name, preferred date, time, and duration.",
        }
    else:
        response = llm.invoke(
            [
                {"role": "system", "content": prompt},
                *state["messages"],
            ]
        )

    return {"messages": [response]}
