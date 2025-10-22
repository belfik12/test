import certifi
import httpx
import ssl
from telegram.request import HTTPXRequest
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your BotFather token
TOKEN = "8305319004:AAGcCuufwLtRUmQfPGLndWAijloFik-SIl0"

# The Telegram user ID of the recipient (you or whoever should receive messages)
TARGET_USER_ID = 372763614  # get it using @userinfobot in Telegram




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me any message, and I’ll forward it anonymously!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    sender_id = update.message.from_user.id

    # Send to target user anonymously
    await context.bot.send_message(
        chat_id=TARGET_USER_ID,
        text=f"📩 Anonymous message:\n\n{message_text}"
    )

    await update.message.reply_text("✅ Message sent anonymously!")

def main():
    
    
    
    app = Application.builder().token(TOKEN).build()
    #app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
