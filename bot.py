import os
import asyncio
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ============================================================
# 🔧 YOUR CONFIGURATION
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_LINK = "https://t.me/projectbuild1"

if not BOT_TOKEN:
    raise Exception("❌ Missing BOT_TOKEN! Please add it in Render Environment Variables.")

# ============================================================
# 🌐 FLASK WEB SERVER
# ============================================================
flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    return "🤖 Telegram Bot is running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# ============================================================
# 🤖 TELEGRAM BOT
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to our bot!\n\n"
        "Click the button below to join our official channel:\n"
        "👇👇👇",
        reply_markup=reply_markup
    )

# ============================================================
# 🚀 START THE BOT
# ============================================================
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("✅ Bot is ready! Send /start to your bot on Telegram.")
    app.run_polling()

if __name__ == "__main__":
    print("🤖 Starting Telegram Bot...")
    print(f"📢 Channel Link: {CHANNEL_LINK}")
    print(f"🔑 Bot Token: {'✅ Set' if BOT_TOKEN else '❌ Missing'}")

    # Start bot in background thread with its own event loop
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Flask runs on main thread (Render needs this)
    run_flask()
