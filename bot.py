import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import config
from config import BOT_TOKEN, IMAGE_FILE, WELCOME_TEXT, BOT_DESCRIPTION

# ---------- LOGGING ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------- HELPER FUNCTIONS ----------
def clean_text(text: str) -> str:
    """Remove extra spaces, tabs, multiple newlines"""
    # Replace all whitespace (spaces, tabs, newlines) with single space
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned

def strip_trackers(text: str) -> str:
    """Remove tracking parameters from URLs"""
    # Remove UTM parameters, ref, code, source, campaign, etc.
    stripped = re.sub(r"[?&](utm_[^&]+|ref|code|source|campaign|term|medium|content)=[^&]*", "", text)
    # Clean up any leftover ? or & at the end
    stripped = re.sub(r"[?&]$", "", stripped)
    return stripped

def count_ad_chars(text: str) -> dict:
    """Count characters with and without spaces"""
    return {
        "with_spaces": len(text),
        "without_spaces": len(text.replace(" ", ""))
    }

# ---------- /start COMMAND ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with image"""
    user = update.effective_user
    first_name = user.first_name or "Mate"
    
    # Build the caption
    caption = (
        f"👋 G'day {first_name}!\n\n"
        f"{WELCOME_TEXT}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🧰 *Bot Functions:*\n"
        f"• Clean text spaces\n"
        f"• Strip link trackers\n"
        f"• Count ad characters\n\n"
        f"📩 Send me any text or URL to process!"
    )

    try:
        # Try to send with image
        with open(IMAGE_FILE, "rb") as img:
            await update.message.reply_photo(
                photo=img,
                caption=caption,
                parse_mode="Markdown"
            )
        logger.info(f"Sent welcome with image to {user.id}")
    except FileNotFoundError:
        # Fallback if image is missing
        logger.warning(f"Image file {IMAGE_FILE} not found, sending text only")
        await update.message.reply_text(
            caption,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error sending image: {e}")
        # Fallback to text only
        await update.message.reply_text(
            caption,
            parse_mode="Markdown"
        )

# ---------- /help COMMAND ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    help_text = (
        f"🧰 *CopyBot Help*\n\n"
        f"*Commands:*\n"
        f"/start - Show welcome message\n"
        f"/help - Show this help\n\n"
        f"*What I can do:*\n"
        f"1️⃣ Clean text spaces\n"
        f"2️⃣ Strip tracking from URLs\n"
        f"3️⃣ Count characters for ads\n\n"
        f"*Example:*\n"
        f"Send me: `Check this out https://example.com?utm_source=test&ref=123`\n"
        f"I'll clean it up and count it for you!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# ---------- /about COMMAND ----------
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send about info"""
    about_text = (
        f"📌 *About CopyBot*\n\n"
        f"{BOT_DESCRIPTION}\n\n"
        f"⚡ Built with python-telegram-bot\n"
        f"✅ Fully compliant with Telegram TOS"
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

# ---------- TEXT PROCESSING ----------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process any text message"""
    raw = update.message.text
    
    # Log the request
    logger.info(f"Processing text from {update.effective_user.id}: {raw[:50]}...")

    # Step 1: Clean text spaces
    cleaned = clean_text(raw)

    # Step 2: Strip trackers from URLs
    stripped = strip_trackers(cleaned)

    # Step 3: Count characters
    counts = count_ad_chars(stripped)

    # Build response
    response = (
        f"📝 *Cleaned & Stripped Result:*\n"
        f"┌─────────────────────\n"
        f"│ `{stripped}`\n"
        f"└─────────────────────\n\n"
        f"📊 *Character Count:*\n"
        f"• With spaces: `{counts['with_spaces']}`\n"
        f"• Without spaces: `{counts['without_spaces']}`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 Send another text or URL to process!"
    )

    await update.message.reply_text(response, parse_mode="Markdown")

# ---------- ERROR HANDLER ----------
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

# ---------- MAIN ----------
def main():
    """Start the bot"""
    # Check if token exists
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set your BOT_TOKEN in the .env file!")
        print("   Get your token from @BotFather on Telegram.")
        return

    print("🤖 Starting CopyBot...")
    print(f"   Bot token: {BOT_TOKEN[:10]}...")
    print(f"   Image file: {IMAGE_FILE}")
    print("   Press Ctrl+C to stop")
    print("━━━━━━━━━━━━━━━━━━━━━")

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()