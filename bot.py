import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ============================================================
# 🔧 YOUR CONFIGURATION - Channel link is already added!
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Get token from Render
CHANNEL_LINK = "https://t.me/projectbuild1"  # YOUR CHANNEL LINK - Already set!
# ============================================================

# Check if token is set
if not BOT_TOKEN:
    raise Exception("❌ Missing BOT_TOKEN! Please add it in Render Environment Variables.")

# ============================================================
# 🌐 FLASK WEB SERVER - Keeps Render happy (don't touch this)
# ============================================================
flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    return "🤖 Telegram Bot is running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# ============================================================
# 🤖 TELEGRAM BOT - Shows the join button!
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    When users send /start, they get a button to join your channel.
    Channel: https://t.me/projectbuild1
    """
    
    # Create a button that users can click to join your channel
    keyboard = [
        [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the welcome message with the button
    await update.message.reply_text(
        "👋 Welcome to our bot!\n\n"
        "Click the button below to join our official channel:\n"
        "👇👇👇",
        reply_markup=reply_markup
    )

# ============================================================
# 🚀 START THE BOT
# ============================================================

if __name__ == "__main__":
    print("🤖 Starting Telegram Bot...")
    print(f"📢 Channel Link: {CHANNEL_LINK}")
    print(f"🔑 Bot Token: {'✅ Set' if BOT_TOKEN else '❌ Missing'}")
    
    # Setup the Telegram bot
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add the /start command handler
    app.add_handler(CommandHandler("start", start))
    
    # Start Flask in the background (so Render doesn't shut us down)
    threading.Thread(target=run_flask).start()
    
    # Start the bot and listen for messages
    print("✅ Bot is ready! Send /start to your bot on Telegram.")
    app.run_polling()
