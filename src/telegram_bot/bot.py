from langchain_core.tools import tool
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ApplicationBuilder,
)
from src import config
from src.langgraph_service.graph import graph


async def send_telegram_message(context, user_id, text, buttons=None):
    """Sends a message to user in telegram"""
    await context.bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )


async def start(update, context):
    await update.message.reply_text("Hey there! Print /schedule to start planning.")


async def schedule(update, context):
    user_id = update.message.chat_id
    await send_telegram_message(context, user_id, "Checking available slots...")
    graph_config = {
        "configurable": {
            "thread_id": str(user_id),
        }
    }
    result = graph.invoke(
        {
            "messages": [{"role": "user", "content": "Start meeting planning"}],
        },
        config=graph_config,
    )
    await send_telegram_message(context, user_id, result["messages"][-1].content)


async def handle_response(update, context):
    user_input = update.message.text
    user_id = update.message.chat_id
    graph_config = {
        "configurable": {
            "thread_id": str(user_id),
        }
    }
    result = graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]}, config=graph_config
    )
    await send_telegram_message(context, user_id, result["messages"][-1].content)


def main():
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schedule", schedule))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))

    app.run_polling()


if __name__ == "__main__":
    main()
