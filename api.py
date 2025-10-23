# db.py
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from db import init_db, add_user, get_user_by_username
from keep_alive import keep_alive
keep_alive()


TOKEN = "8305319004:AAGcCuufwLtRUmQfPGLndWAijloFik-SIl0"
init_db()

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, update.effective_chat.id)
    await update.message.reply_text("👋 Welcome to Anonymous Messenger!\nUse:\n/send @username message")

async def send_anonymous(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /send @username your message")
        return

    target_username = context.args[0].replace("@", "")
    message_text = " ".join(context.args[1:])
    target_chat_id = get_user_by_username(target_username)

    if target_chat_id:
        await context.bot.send_message(target_chat_id, f"📩 Anonymous message:\n{message_text}")
        await update.message.reply_text("✅ Message sent anonymously!")
    else:
        await update.message.reply_text("❌ That user hasn’t started the bot yet.\n contact us at @anonymousTexterM")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("send", send_anonymous))

app.run_polling()


