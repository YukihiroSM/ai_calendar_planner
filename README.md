# Telegram Meeting Scheduler Bot
## [ TEST TASK FOR CostCareAI ]

This project is a **Telegram bot** that helps users schedule meetings by integrating with **Google Calendar**. The bot uses **LangGraph** for structured AI conversation handling and requires API credentials for Google Cloud.

## 🚀 Getting Started

### 1️⃣ Prerequisites
- Python **3.12** (Make sure you have it installed)
- [Poetry](https://python-poetry.org/docs/) for dependency management
- Google Cloud **OAuth 2.0 Credentials** (JSON file)
- A Telegram Bot API Token

### 2️⃣ Clone the Repository
```sh
git clone git@github.com:YukihiroSM/ai_calendar_planner.git
cd ai_calendar_planner
```

### 3️⃣ Set Up Environment Variables
1. Create a `.env` file by copying the provided example:
```sh
cp .env.example .env
```
2. Open `.env` and fill in the required API keys:
```env
TELEGRAM_TOKEN=your-telegram-bot-token
EXTERNAL_CALENDAR_ID=your-calendar-id
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### 4️⃣ Install Dependencies
Run the following command to install all required packages:
```sh
poetry install
```

### 5️⃣ Add Google OAuth Credentials
Place your **Google OAuth credentials** file (`credentials.json`) in the project root.

### 6️⃣ Run the Bot
Start the bot with:
```sh
poetry run python src/telegram_bot/bot.py
```

