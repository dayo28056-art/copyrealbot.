import logging
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Import config
from config import BOT_TOKEN, IMAGE_FILE

# ---------- LOGGING ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------- CONFIGURATION ----------
WELCOME_TEXT = """✅ VIP has increased to 3.5% + 3📌

🪙 REGISTER HERE ⏩⏩
https://app-web.mobiuspe-app.com/regist?code=earnmoney426

✅ We offer team leader salaries and up to 0.6% team commission. Please contact us to apply for a team leader position. 🛒

Official channel link ⭐️
https://t.me/mobiuspayofficial1

Contact support ⭐️ @puya1521"""

# ---------- HELPER FUNCTIONS ----------
def clean_text(text: str) -> str:
    """Remove extra spaces, tabs, multiple newlines"""
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned

def strip_trackers(text: str) -> str:
    """Remove tracking parameters from URLs"""
    stripped = re.sub(r"[?&](utm_[^&]+|ref|code|source|campaign|term|medium|content|clickid|affid)=[^&]*", "", text)
    stripped = re.sub(r"[?&]$", "", stripped)
    stripped = re.sub(r"\?\?+", "?", stripped)
    stripped = re.sub(r"&&+", "&", stripped)
    return stripped

def count_ad_chars(text: str) -> dict:
    """Count characters with and without spaces"""
    return {
        "with_spaces": len(text),
        "without_spaces": len(text.replace(" ", ""))
    }

# ---------- CREATE BUTTONS ----------
def get_welcome_buttons():
    """Create the inline keyboard buttons"""
    keyboard = [
        [
            InlineKeyboardButton("🪙 Register", url="https://app-web.mobiuspe-app.com/regist?code=earnmoney426"),
            InlineKeyboardButton("⭐️ Join Channel", url="https://t.me/mobiuspayofficial1"),
        ],
        [
            InlineKeyboardButton("📞 Customer Care", url="https://t.me/puya1521"),
            InlineKeyboardButton("ℹ️ About Bot", callback_data="about"),
        ],
        [
            InlineKeyboardButton("📊 Check My Stats", callback_data="stats"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- /start COMMAND ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with image and buttons"""
    user = update.effective_user
    first_name = user.first_name or "Mate"
    
    # Build the professional welcome message
    caption = (
        f"🚀 *WELCOME TO COPYBOT!*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👋 G'day {first_name}!\n\n"
        f"📌 *VIP has increased to 3.5% + 3*\n\n"
        f"🪙 *REGISTER HERE* ⏩⏩\n"
        f"`https://app-web.mobiuspe-app.com/regist?code=earnmoney426`\n\n"
        f"✅ We offer team leader salaries and up to *0.6% team commission*.\n"
        f"Please contact us to apply for a team leader position. 🛒\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 *Bot Functions:*\n"
        f"• ✨ Clean text spaces\n"
        f"• 🔗 Strip link trackers\n"
        f"• 📊 Count ad characters\n\n"
        f"💡 *Send me any text or URL to process!*"
    )

    try:
        # Check if image exists
        if os.path.exists(IMAGE_FILE):
            with open(IMAGE_FILE, "rb") as img:
                await update.message.reply_photo(
                    photo=img,
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=get_welcome_buttons()
                )
            logger.info(f"Sent welcome with image and buttons to {user.id}")
        else:
            # Fallback if image is missing
            logger.warning(f"Image file {IMAGE_FILE} not found, sending text only")
            await update.message.reply_text(
                caption,
                parse_mode="Markdown",
                reply_markup=get_welcome_buttons()
            )
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        # Fallback to text only
        await update.message.reply_text(
            caption,
            parse_mode="Markdown",
            reply_markup=get_welcome_buttons()
        )

# ---------- CALLBACK QUERY HANDLER ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    
    data = query.data
    
    if data == "about":
        about_text = (
            f"🤖 *About CopyBot*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🧰 This bot helps you:\n"
            f"• Clean text spaces\n"
            f"• Strip link trackers\n"
            f"• Count ad characters\n\n"
            f"📌 *Version:* 2.0\n"
            f"⚡ *Built with:* python-telegram-bot\n"
            f"✅ *TOS Compliant:* Yes\n\n"
            f"💡 Send any text to get started!"
        )
        await query.edit_message_caption(
            caption=about_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
            ])
        )
    
    elif data == "stats":
        # Get user stats (simple example)
        user_id = query.from_user.id
        stats_text = (
            f"📊 *Your Stats*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 User ID: `{user_id}`\n"
            f"📅 First seen: Today\n"
            f"📝 Messages processed: {context.user_data.get('count', 0)}\n\n"
            f"💡 Keep using the bot to unlock more features!"
        )
        await query.edit_message_caption(
            caption=stats_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
            ])
        )
    
    elif data == "back":
        # Return to main menu
        user = query.from_user
        first_name = user.first_name or "Mate"
        
        caption = (
            f"🚀 *WELCOME TO COPYBOT!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👋 G'day {first_name}!\n\n"
            f"📌 *VIP has increased to 3.5% + 3*\n\n"
            f"🪙 *REGISTER HERE* ⏩⏩\n"
            f"`https://app-web.mobiuspe-app.com/regist?code=earnmoney426`\n\n"
            f"✅ We offer team leader salaries and up to *0.6% team commission*.\n"
            f"Please contact us to apply for a team leader position. 🛒\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 *Bot Functions:*\n"
            f"• ✨ Clean text spaces\n"
            f"• 🔗 Strip link trackers\n"
            f"• 📊 Count ad characters\n\n"
            f"💡 *Send me any text or URL to process!*"
        )
        
        try:
            # Try to restore with image if available
            if os.path.exists(IMAGE_FILE):
                with open(IMAGE_FILE, "rb") as img:
                    await query.edit_message_media(
                        media=InputMediaPhoto(media=img, caption=caption, parse_mode="Markdown"),
                        reply_markup=get_welcome_buttons()
                    )
            else:
                await query.edit_message_caption(
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=get_welcome_buttons()
                )
        except Exception as e:
            logger.error(f"Error returning to menu: {e}")
            await query.edit_message_caption(
                caption=caption,
                parse_mode="Markdown",
                reply_markup=get_welcome_buttons()
            )

# ---------- /help COMMAND ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    help_text = (
        f"🧰 *CopyBot Help*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"*Commands:*\n"
        f"/start - Show welcome menu\n"
        f"/help - Show this help\n\n"
        f"*What I can do:*\n"
        f"1️⃣ Clean text spaces\n"
        f"2️⃣ Strip tracking from URLs\n"
        f"3️⃣ Count characters for ads\n\n"
        f"*Example:*\n"
        f"Send me: `Check this out https://example.com?utm_source=test&ref=123`\n"
        f"I'll clean it up and count it for you!"
    )
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
        ])
    )

# ---------- TEXT PROCESSING ----------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process any text message"""
    raw = update.message.text
    
    # Track user activity
    user_id = update.effective_user.id
    context.user_data['count'] = context.user_data.get('count', 0) + 1
    
    # Log the request
    logger.info(f"Processing text from {user_id}: {raw[:50]}...")

    # Step 1: Clean text spaces
    cleaned = clean_text(raw)

    # Step 2: Strip trackers from URLs
    stripped = strip_trackers(cleaned)

    # Step 3: Count characters
    counts = count_ad_chars(stripped)

    # Build response with nice formatting
    response = (
        f"📝 *Cleaned & Stripped Result:*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"`{stripped}`\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📊 *Character Count:*\n"
        f"• With spaces: `{counts['with_spaces']}`\n"
        f"• Without spaces: `{counts['without_spaces']}`\n\n"
        f"💡 *Send another text or URL to process!*"
    )

    await update.message.reply_text(
        response,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")],
            [InlineKeyboardButton("📊 My Stats", callback_data="stats")]
        ])
    )

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

    print("🤖 Starting CopyBot with Buttons...")
    print(f"   Bot token: {BOT_TOKEN[:10]}...")
    print(f"   Image file: {IMAGE_FILE}")
    print("   Press Ctrl+C to stop")
    print("━━━━━━━━━━━━━━━━━━━━━")

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
