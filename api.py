import os
from flask import Flask

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Thread


BOT_TOKEN = "8305319004:AAGcCuufwLtRUmQfPGLndWAijloFik-SIl0"


# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Anonymous Bot is running!"

# Telegram bot logic
users = {}  # simple in-memory storage: username -> chat_id

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user.username:
        await update.message.reply_text("❌ You must have a Telegram username to use this bot.")
        return

    users[user.username.lower()] = update.effective_chat.id
    await update.message.reply_text("👋 Welcome! Use /send @username message to send anonymously.")

async def send_anonymous(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /send @username message")
        return

    target_username = context.args[0].replace("@", "").lower()
    message_text = " ".join(context.args[1:])

    target_chat_id = users.get(target_username)
    if not target_chat_id:
        await update.message.reply_text("❌ That user hasn’t started the bot yet.")
        return

    await context.bot.send_message(chat_id=target_chat_id, text=f"📩 Anonymous message:\n{message_text}")
    await update.message.reply_text("✅ Message sent anonymously!")

def run_bot():
    app_telegram = Application.builder().token(BOT_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("send", send_anonymous))
    app_telegram.run_polling()

# Run Telegram bot in background thread
bot_thread = Thread(target=run_bot)
bot_thread.start()

# Run Flask web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
