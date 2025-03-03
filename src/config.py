from dotenv import load_dotenv
import os
from pathlib import Path
import logging

load_dotenv()
CONFIG_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = Path(CONFIG_PATH, "..")
GOOGLE_API_CREDENTIALS_PATH = Path(BASE_PATH, "credentials.json")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SCOPES = ["https://www.googleapis.com/auth/calendar"]
EXTERNAL_CALENDAR_ID = os.environ.get("EXTERNAL_CALENDAR_ID")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)