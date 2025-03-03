from src import config
from langchain_anthropic import ChatAnthropic


llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", api_key=config.ANTHROPIC_API_KEY
)
