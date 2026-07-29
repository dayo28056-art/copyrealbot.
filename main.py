import os
import re
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from http import HTTPStatus

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_URL = os.getenv("RAILWAY_PUBLIC_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing.")

WELCOME_TEXT = """
👋 *Welcome to CopyBot*

Send any text and I'll help you with professional copy tools.

✨ Clean Formatting
🔗 Remove Tracking Links
📊 Count Characters & Words

Choose a tool after sending your text.
"""

bot = Application.builder().token(BOT_TOKEN).build()


@asynccontextmanager
async def lifespan(app: FastAPI):

    await bot.initialize()

    if PUBLIC_URL:

        webhook = f"{PUBLIC_URL.rstrip('/')}/webhook"

        await bot.bot.set_webhook(
            url=webhook,
            drop_pending_updates=True,
        )

        await bot.start()

    else:

        await bot.bot.delete_webhook(
            drop_pending_updates=True
        )

        await bot.start()

        await bot.updater.start_polling()

    yield

    if bot.updater and bot.updater.running:
        await bot.updater.stop()

    await bot.stop()
    await bot.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {
        "status": "running"
    }


@app.post("/webhook")
async def webhook(request: Request):

    update = Update.de_json(
        await request.json(),
        bot.bot,
    )

    await bot.process_update(update)

    return Response(status_code=HTTPStatus.OK)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    image = "images/welcome.jpg"

    if os.path.exists(image):

        with open(image, "rb") as photo:

            await update.message.reply_photo(
                photo=InputFile(photo),
                caption=WELCOME_TEXT,
                parse_mode="Markdown",
            )

    else:

        await update.message.reply_text(
            WELCOME_TEXT,
            parse_mode="Markdown",
        )


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["text"] = update.message.text

    keyboard = [

        [
            InlineKeyboardButton(
                "🧹 Clean Formatting",
                callback_data="clean",
            )
        ],

        [
            InlineKeyboardButton(
                "🔗 Remove Tracking Links",
                callback_data="links",
            )
        ],

        [
            InlineKeyboardButton(
                "📊 Copy Statistics",
                callback_data="stats",
            )
        ],

    ]

    await update.message.reply_text(
        "Choose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    text = context.user_data.get("text")

    if not text:

        await query.edit_message_text(
            "Please send some text first."
        )

        return

    if query.data == "clean":

        cleaned = re.sub(
            r"\n\s*\n",
            "\n\n",
            text.strip(),
        )

        cleaned = re.sub(
            r"[ \t]+",
            " ",
            cleaned,
        )

        await query.edit_message_text(
            f"✨ Cleaned Text\n\n{cleaned}"
        )

    elif query.data == "links":

        cleaned = re.sub(
            r"([?&])(utm_[^=&]+|fbclid|gclid)=[^&]+",
            "",
            text,
        )

        await query.edit_message_text(cleaned)

    elif query.data == "stats":

        chars = len(text)
        words = len(text.split())
        lines = len(text.splitlines())

        await query.edit_message_text(
            f"""📊 Copy Statistics

Characters: {chars}

Words: {words}

Lines: {lines}
"""
        )


bot.add_handler(CommandHandler("start", start))

bot.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        receive_text,
    )
)

bot.add_handler(
    CallbackQueryHandler(buttons)
)
