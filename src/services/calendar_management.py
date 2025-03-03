import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from src import config
from langchain_core.tools import tool


def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=config.GOOGLE_API_CREDENTIALS_PATH, scopes=config.SCOPES
    )
    credentials = flow.run_local_server(port=0)
    return build("calendar", "v3", credentials=credentials)


service = get_calendar_service()


@tool
def fetch_external_calendar_slots():
    """Retrieves busy slots from external calendar"""
    now = datetime.datetime.now().isoformat() + "Z"
    events_result = (
        service.events()
        .list(
            calendarId=config.EXTERNAL_CALENDAR_ID,
            timeMin=now,
            maxResults=25,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    busy_slots = [
        {"start": event["start"].get("dateTime"), "end": event["end"].get("dateTime")}
        for event in events_result.get("items", [])
    ]
    return {"busy_slots": busy_slots}


def create_google_calendar_event(chosen_slot, end_time, meeting_name):
    event = {
        "summary": meeting_name,
        "start": {"dateTime": chosen_slot, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
        "attendees": [
            {"email": config.EXTERNAL_CALENDAR_ID}
        ],
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event
